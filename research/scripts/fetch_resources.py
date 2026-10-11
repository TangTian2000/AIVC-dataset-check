#!/usr/bin/env python3
"""Fetch only reviewed small sources/metadata; never expression matrices.
Run from repository root. A 25 MiB limit applies to each body, including unknown sizes.
"""
import argparse, datetime, hashlib, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'resources.json'
LOG = ROOT / 'download_log.jsonl'
LIMIT = 25 * 1024 * 1024

def fetch(item, refresh=False):
    path = ROOT / item['path']
    record = dict(id=item['id'], url=item['url'], path=item['path'], attempted_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    if path.exists() and not refresh:
        data = path.read_bytes()
        record.update(status='cached', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if item.get('sha256') and item['sha256'] != record['sha256']:
            record.update(status='failed', error='Cached checksum mismatch; use --refresh to retrieve the pinned source')
    else:
        try:
            request = urllib.request.Request(item['url'], headers={'User-Agent': 'AIVC-dataset-audit/1.0'})
            with urllib.request.urlopen(request, timeout=30) as response:
                length = response.headers.get('Content-Length')
                record.update(http_status=response.status, content_length=length, final_url=response.url)
                if length and int(length) > LIMIT:
                    raise ValueError(f'Body exceeds 25 MiB limit: {length} bytes')
                data = response.read(LIMIT + 1)
                if len(data) > LIMIT:
                    raise ValueError('Body exceeds 25 MiB limit (unknown advertised length)')
            if item.get('sha256') and hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError('Checksum mismatch; existing artifact retained')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            record.update(status='downloaded', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        except Exception as exc:
            record.update(status='failed', error=str(exc))
    with LOG.open('a') as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(item['id'], record['status'], record.get('bytes', record.get('error')))
    return record

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='*')
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    items = json.loads(MANIFEST.read_text())
    failed = False
    for item in items:
        if args.ids is None and item.get('enabled') is False:
            continue
        if args.ids is None or item['id'] in args.ids:
            failed = fetch(item, args.refresh)['status'] == 'failed' or failed
    if failed:
        raise SystemExit(1)
