#!/usr/bin/env python3
"""Index cached sources, render notebook source cells, and verify pinned artifacts."""
import hashlib,json,csv,argparse
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--freeze-checksums',action='store_true');a=p.parse_args()
manifest=R/'resources.json';items=json.loads(manifest.read_text());index=[];failed=False
for x in items:
 path=R/x['path'];rec=dict(resource_id=x['id'],url=x['url'],path=x['path'],kind=x['kind'],source_commit=x.get('source_commit',''),status='disabled' if x.get('enabled') is False else 'missing',bytes='',sha256='')
 if path.exists():
  b=path.read_bytes();h=hashlib.sha256(b).hexdigest();rec.update(status='verified' if x.get('sha256')==h else 'present_unfrozen' if not x.get('sha256') else 'checksum_mismatch',bytes=len(b),sha256=h)
  if x.get('sha256') and h!=x['sha256']:failed=True
  if a.freeze_checksums:
   if rec['status']=='checksum_mismatch':raise ValueError('Do not freeze changed source: '+x['id'])
   x['sha256']=h;rec['status']='verified'
  if path.suffix=='.ipynb':
   notebook=json.loads(b)
   text='\n\n'.join(f"CELL {i} [{c['cell_type']}]\n"+''.join(c.get('source',[])) for i,c in enumerate(notebook['cells']))
   path.with_suffix('.cells.txt').write_text(text)
 if rec['status']=='missing':failed=True
 index.append(rec)
if a.freeze_checksums:manifest.write_text(json.dumps(items,ensure_ascii=False,indent=2))
with (R/'sources/source_index.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,list(index[0]));w.writeheader();w.writerows(index)
print('Indexed',len(index),'reviewed resources; enabled missing/checksum failures:',failed)
if failed:raise SystemExit(1)
