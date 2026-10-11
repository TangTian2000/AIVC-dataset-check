#!/usr/bin/env python3
"""HEAD-only access/size checks; never downloads expression, never bypasses proxy/TLS."""
import datetime,json,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def probe(item):
    rec=dict(item,attempted_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        with urllib.request.urlopen(urllib.request.Request(item['url'],method='HEAD'),timeout=20) as response:
            rec.update(status=response.status,content_length=response.headers.get('Content-Length'),content_type=response.headers.get('Content-Type'),final_url=response.url)
    except Exception as exc:rec.update(status='failed',error=str(exc),content_length=None)
    return rec
items=json.loads((R/'access_targets.json').read_text());failed=0
with ThreadPoolExecutor(max_workers=6) as executor, (R/'access_log.jsonl').open('a') as file:
    for rec in executor.map(probe,items):
        file.write(json.dumps(rec,ensure_ascii=False)+'\n')
        print(rec['id'],rec['status'],rec.get('content_length'),rec.get('error',''))
        failed+=rec['status']=='failed'
print(f'{failed}/{len(items)} checks failed; see access_log.jsonl')
if failed:raise SystemExit(1)
