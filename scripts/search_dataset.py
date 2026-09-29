import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description='Search bundled policy records offline; status is unverified source metadata')
    p.add_argument('query')
    p.add_argument('--status', help='Exact dataset status; not a current validity guarantee')
    p.add_argument('--full-text', action='store_true')
    p.add_argument('--limit', type=int, default=20)
    a = p.parse_args()
    if a.limit < 1:
        p.error('--limit must be positive')
    root = Path(__file__).resolve().parents[1] / 'references' / 'dataset'
    m = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    hits = []
    for r in m['records']:
        if a.status is not None and (r['aging'] or '未标注') != a.status:
            continue
        text = ' '.join(r[k] or '' for k in ['title','document_number','tax_type','labels'])
        if a.full_text:
            text += (root/'markdown'/f'{r["id"]}.md').read_text(encoding='utf-8')
        if a.query.casefold() in text.casefold():
            hit = {k:r[k] for k in ['id','title','document_number','written_date','aging','channel','url']}
            hit['markdown_path'] = f'references/dataset/markdown/{r["id"]}.md'
            hits.append(hit)
    print(json.dumps({'matched':len(hits),'shown':min(a.limit,len(hits)),
                      'validity_verified':False,'results':hits[:a.limit]},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
