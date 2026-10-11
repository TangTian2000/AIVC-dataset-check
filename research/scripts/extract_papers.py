#!/usr/bin/env python3
"""Regenerate text from cached, hash-verified author-hosted PDFs."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if not shutil.which('pdftotext'):
    raise SystemExit('Install system package poppler-utils to extract cached PDFs.')
count = 0
for item in json.loads((root / 'resources.json').read_text()):
    if item['kind'] != 'paper' or item.get('enabled') is False:
        continue
    path = root / item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], path
    subprocess.run(['pdftotext', '-layout', str(path), str(path.with_suffix('.txt'))], check=True)
    count += 1
print(f'Extracted {count} frozen PDFs; no expression matrices read')
