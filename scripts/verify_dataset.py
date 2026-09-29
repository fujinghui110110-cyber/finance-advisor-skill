import argparse
import json
from pathlib import Path
from import_parquet import render_record, sha


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    root = args.root / 'references' / 'dataset'
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    assert manifest['distribution_format'] == 'markdown'
    ids = []
    for r in manifest['records']:
        sid = r['id']
        raw = (root / 'records' / f'{sid}.json').read_bytes()
        md = (root / 'markdown' / f'{sid}.md').read_bytes()
        row = json.loads(raw)
        assert sha(raw) == r['record_sha256'], sid
        assert sha(md) == r['markdown_sha256'], sid
        assert sha((row['content'] or '').encode()) == r['content_sha256'], sid
        assert md.decode() == render_record(row, sid), sid
        assert md.decode().split('\n## 正文\n\n', 1)[1] == (row['content'] or '') + '\n', sid
        assert r['validity_verified'] is False, sid
        ids.append(sid)
    assert len(ids) == len(set(ids)) == manifest['record_count']
    for part, suffix in [('records', 'json'), ('markdown', 'md')]:
        assert len(list((root / part).glob('*.' + suffix))) == len(ids)
    original = json.loads((args.root / 'references' / 'manifest.json').read_text(encoding='utf-8'))
    for r in original['records']:
        md = (args.root / 'references' / 'markdown' / (r['source_id'] + '.md')).read_text(encoding='utf-8')
        assert md.split('\n## 原始提取正文\n\n', 1)[1] == (args.root / r['extracted_text_path']).read_text(encoding='utf-8')
    assert len(list((args.root / 'references' / 'markdown').glob('*.md'))) == len(original['records'])
    print(json.dumps({'status': 'ok', 'records': len(ids), 'original_markdown': len(original['records'])}))


if __name__ == '__main__':
    main()
