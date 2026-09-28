from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an installed finance-advisor skill")
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    root = args.skill_dir.resolve()
    manifest_path = root / "references" / "manifest.json"
    errors: list[str] = []
    if not manifest_path.is_file():
        print(f"FAIL: missing {manifest_path}")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest.get("records", [])
    expected = manifest.get("unique_pdf_documents")
    if not isinstance(expected, int) or expected != len(records):
        fail(errors, "manifest unique_pdf_documents does not match records")
    text_paths = {record.get("extracted_text_path") for record in records}
    pdf_paths = {record.get("pdf_copy_path") for record in records}
    if len(text_paths) != len(records) or len(pdf_paths) != len(records):
        fail(errors, "manifest contains duplicate corpus paths")
    for record in records:
        text_path = root / record["extracted_text_path"]
        pdf_path = root / record["pdf_copy_path"]
        if not text_path.is_file():
            fail(errors, f"missing text: {record['source_id']}")
            continue
        if not pdf_path.is_file():
            fail(errors, f"missing PDF: {record['source_id']}")
            continue
        if digest(pdf_path) != record["pdf_sha256"]:
            fail(errors, f"PDF hash mismatch: {record['source_id']}")
        text = text_path.read_text(encoding="utf-8")
        if "----- BEGIN EXTRACTED PDF TEXT -----" not in text:
            fail(errors, f"missing extraction start marker: {record['source_id']}")
        if "----- END EXTRACTED PDF TEXT -----" not in text:
            fail(errors, f"missing extraction end marker: {record['source_id']}")
        if record["pdf_sha256"] not in text:
            fail(errors, f"text metadata missing PDF hash: {record['source_id']}")
        if record["authority_layer"] == "future_or_pending" and "尚未施行" not in record["status_hint"]:
            fail(errors, f"pending source lacks explicit status: {record['source_id']}")

    all_files = [path for path in root.rglob("*") if path.is_file()]
    absolute_path_pattern = re.compile(r"/(?:Users|Volumes|private/tmp)/")
    for path in all_files:
        if path.suffix.lower() not in {".md", ".json", ".txt", ".py", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if absolute_path_pattern.search(text):
            fail(errors, f"absolute local path found: {path.relative_to(root)}")
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    if "references/" not in skill_text:
        fail(errors, "SKILL.md does not route to references/")
    if len(list((root / "references" / "text").glob("*.txt"))) != expected:
        fail(errors, "text file count does not match manifest")
    if len(list((root / "references" / "pdf").glob("*.pdf"))) != expected:
        fail(errors, "PDF file count does not match manifest")

    if errors:
        print("FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(
        json.dumps(
            {
                "status": "ok",
                "unique_pdf_documents": expected,
                "total_pdf_copies_found": manifest.get("total_pdf_copies_found"),
                "duplicate_pdf_copies_collapsed": manifest.get(
                    "duplicate_pdf_copies_collapsed"
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
