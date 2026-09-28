from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path


CATEGORY_INFO = {
    "01_增值税": ("税法与增值税", "primary_or_formal"),
    "01_增值税及2026配套政策": ("税法与增值税", "primary_or_formal"),
    "02_所得税及税收征管": ("所得税与税收征管", "primary_or_formal"),
    "03_企业所得税": ("所得税与税收征管", "primary_or_formal"),
    "03_会计法律及基础管理": ("会计法律与基础管理", "primary_or_formal"),
    "04_个人所得税": ("所得税与税收征管", "primary_or_formal"),
    "04_企业会计准则正文": ("企业会计准则正文", "primary_or_formal"),
    "05_企业会计准则解释": ("企业会计准则解释", "formal_interpretation"),
    "05_印花税": ("印花税与相关税费政策", "primary_or_formal"),
    "06_会计司实施问答": ("会计司实施问答", "supplementary_qa"),
    "07_税务机关解读及地方口径": ("税务机关解读与地方口径", "local_guidance"),
    "17_关税": ("小微企业与融资税费政策（原目录：17_关税）", "primary_or_formal"),
    "24_会计法律与基础管理": ("会计法律与基础管理", "primary_or_formal"),
    "25_会计准则与实施材料": ("企业会计准则实施材料", "supplementary_qa"),
    "90_已发布尚未施行": ("已发布尚未施行", "future_or_pending"),
    "90_已发布未施行": ("已发布尚未施行", "future_or_pending"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_pages(path: Path) -> int | None:
    result = subprocess.run(
        ["pdfinfo", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if result.returncode:
        return None
    for line in result.stdout.decode("utf-8", errors="replace").splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def extract_pdf(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"pdftotext failed for {path}: {error}")
    text = result.stdout.decode("utf-8", errors="replace")
    return text if text.endswith("\n") else text + "\n"


def document_key(stem: str, used: set[str], digest: str) -> str:
    match = re.match(r"^([A-Za-z]+\d{2,3})(?:_|$)", stem)
    base = match.group(1).upper() if match else "DOC"
    if base not in used:
        used.add(base)
        return base
    key = f"{base}-{digest[:8]}"
    used.add(key)
    return key


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def status_hint(folder: str, authority: str) -> str:
    if authority == "future_or_pending":
        return "来源目录标为已发布尚未施行；必须回到正文核对施行日和过渡条款"
    if authority == "local_guidance":
        return "地方解读或地方口径；只在主体、地点和期间匹配时参考"
    if authority == "supplementary_qa":
        return "实施问答或实施材料；须与对应法律、准则正文联读"
    if authority == "formal_interpretation":
        return "正式准则解释；须与对应准则正文及生效安排联读"
    return "正式制度文本候选来源；仍须核对发布、施行、修正和适用范围"


def build(source_dir: Path, output_dir: Path, snapshot_date: str) -> dict:
    if shutil.which("pdftotext") is None or shutil.which("pdfinfo") is None:
        raise RuntimeError("需要 pdftotext 和 pdfinfo；请安装 poppler 后重试")
    pdfs = sorted(source_dir.rglob("*.pdf"))
    if not pdfs:
        raise RuntimeError(f"没有在 {source_dir} 找到 PDF")

    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in pdfs:
        by_hash[sha256(path)].append(path)
    unique = sorted(by_hash.items(), key=lambda item: str(sorted(item[1])[0]))

    text_dir = output_dir / "references" / "text"
    pdf_dir = output_dir / "references" / "pdf"
    text_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    used_keys: set[str] = set()
    total_pages = 0
    total_chars = 0
    for digest, paths in unique:
        paths = sorted(paths)
        canonical = paths[0]
        relative_paths = [p.relative_to(source_dir).as_posix() for p in paths]
        folder = canonical.parent.name
        category, authority = CATEGORY_INFO.get(
            folder, (folder, "unclassified_source")
        )
        stem = canonical.stem
        key = document_key(stem, used_keys, digest)
        raw_text = extract_pdf(canonical)
        pages = pdf_pages(canonical)
        if pages:
            total_pages += pages
        total_chars += len(raw_text)

        header = (
            f"SOURCE_ID: {key}\n"
            f"TITLE: {stem}\n"
            f"CATEGORY: {category}\n"
            f"AUTHORITY_LAYER: {authority}\n"
            f"STATUS_HINT: {status_hint(folder, authority)}\n"
            f"ORIGINAL_PATHS:\n"
            + "".join(f"- {p}\n" for p in relative_paths)
            + f"PDF_SHA256: {digest}\n"
            + f"PDF_PAGE_COUNT: {pages if pages is not None else 'unknown'}\n"
            + "EXTRACTION: pdftotext -layout; see the PDF copy for page-level layout\n"
            + "----- BEGIN EXTRACTED PDF TEXT -----\n"
        )
        body = header + raw_text + "----- END EXTRACTED PDF TEXT -----\n"
        text_path = text_dir / f"{key}.txt"
        pdf_path = pdf_dir / f"{key}.pdf"
        text_path.write_text(body, encoding="utf-8")
        shutil.copy2(canonical, pdf_path)
        record = {
            "source_id": key,
            "title": stem,
            "category": category,
            "authority_layer": authority,
            "status_hint": status_hint(folder, authority),
            "canonical_original_path": relative_paths[0],
            "original_paths": relative_paths,
            "duplicate_copy_count": len(relative_paths),
            "pdf_sha256": digest,
            "pdf_bytes": canonical.stat().st_size,
            "pdf_page_count": pages,
            "extracted_text_path": f"references/text/{key}.txt",
            "pdf_copy_path": f"references/pdf/{key}.pdf",
            "extracted_text_sha256": hashlib.sha256(raw_text.encode("utf-8")).hexdigest(),
            "extracted_text_chars": len(raw_text),
        }
        records.append(record)

    records.sort(key=lambda item: item["source_id"])
    manifest = {
        "schema_version": 1,
        "snapshot_date": snapshot_date,
        "source_directory_name": source_dir.name,
        "total_pdf_copies_found": len(pdfs),
        "unique_pdf_documents": len(records),
        "duplicate_pdf_copies_collapsed": len(pdfs) - len(records),
        "total_pages": total_pages,
        "total_extracted_text_chars": total_chars,
        "extraction_tool": "pdftotext -layout",
        "records": records,
    }
    (output_dir / "references" / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    category_counts: dict[str, int] = defaultdict(int)
    for record in records:
        category_counts[record["category"]] += 1
    lines = [
        "# 财务顾问内置政策语料清单",
        "",
        f"快照日期：{snapshot_date}。本清单对应 `references/`，不依赖任何本地绝对路径。",
        "",
        f"共发现 {len(pdfs)} 份 PDF，按 SHA-256 去重后保留 {len(records)} 份唯一文件，合并重复副本 {len(pdfs) - len(records)} 份；共 {total_pages} 页，提取文本约 {total_chars:,} 字符。",
        "",
        "状态提示来自原始资料目录或资料类型，不等同于当前法律效力认定。回答前必须核对发布日、施行日、修正和地域适用性。",
        "",
        "| 来源编号 | 文件标题 | 类别 | 页数 | 重复副本 | 状态/使用边界 |",
        "|---|---|---|---:|---:|---|",
    ]
    for record in records:
        links = (
            f"[{record['source_id']}:文本]({record['extracted_text_path']}) / "
            f"[PDF]({record['pdf_copy_path']})"
        )
        lines.append(
            "| "
            + links
            + " | "
            + markdown_cell(record["title"])
            + " | "
            + markdown_cell(record["category"])
            + " | "
            + str(record["pdf_page_count"] or "?")
            + " | "
            + str(record["duplicate_copy_count"])
            + " | "
            + markdown_cell(record["status_hint"])
            + " |"
        )
    lines.extend(
        [
            "",
            "## 类别统计",
            "",
            "| 类别 | 唯一文件数 |",
            "|---|---:|",
        ]
    )
    for category, count in sorted(category_counts.items()):
        lines.append(f"| {markdown_cell(category)} | {count} |")
    (output_dir / "references" / "sources.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    duplicate_lines = [
        "# 重复文件整理映射",
        "",
        "原始资料目录保留不动。本文件记录按 SHA-256 判定的重复副本，技能语料只保留每组的一个规范副本。",
        "",
    ]
    for record in records:
        if record["duplicate_copy_count"] <= 1:
            continue
        duplicate_lines.extend(
            [
                f"## {record['source_id']}：{record['title']}",
                "",
                f"- SHA-256：`{record['pdf_sha256']}`",
                f"- 技能规范副本：`{record['pdf_copy_path']}`",
                "- 原始路径：",
                *[f"  - `{path}`" for path in record["original_paths"]],
                "",
            ]
        )
    (output_dir / "references" / "duplicates.md").write_text(
        "\n".join(duplicate_lines), encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the finance policy corpus")
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--snapshot-date", default=date.today().isoformat(), help="YYYY-MM-DD"
    )
    args = parser.parse_args()
    if not args.source_dir.is_dir():
        parser.error(f"source_dir is not a directory: {args.source_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = build(args.source_dir, args.output_dir, args.snapshot_date)
    print(
        json.dumps(
            {
                "total_pdf_copies_found": manifest["total_pdf_copies_found"],
                "unique_pdf_documents": manifest["unique_pdf_documents"],
                "duplicate_pdf_copies_collapsed": manifest[
                    "duplicate_pdf_copies_collapsed"
                ],
                "total_pages": manifest["total_pages"],
                "total_extracted_text_chars": manifest["total_extracted_text_chars"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
