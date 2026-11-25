#!/usr/bin/env python3
"""Package only reviewed source files. Never package private workspaces."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile
from audit_release import audit

root=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('destination');args=ap.parse_args()
manifest=json.loads((root/'release-files.json').read_text())
files=audit()
if len(files)!=len(set(files)):raise SystemExit('Duplicate release file')
for rel in files:
    p=root/rel
    if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):raise SystemExit('Invalid release source: '+rel)
    if p.suffix in ('.sqlite','.pdf','.csv') or 'private' in p.name:raise SystemExit('Private/generated file in release: '+rel)
    # Content check complements, not replaces, the reviewed explicit allowlist.
    content=p.read_text(encoding='utf-8')
    if '/'+ 'Users/' in content or 'C:'+ '\\Users\\' in content:raise SystemExit('Machine-specific path in release: '+rel)
out=Path(args.destination).resolve();out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    archive=Path(tmp)/'job-search-kit.plugin'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(files):z.write(root/rel,rel)
    outputs = {
        'job-search-kit.plugin': archive,
        'job-search-kit.zip': archive,
        'CHAT_STARTER.txt': root / 'CHAT_STARTER.txt',
    }
    checksums = []
    for name, source in outputs.items():
        target = out / name
        shutil.copyfile(source, target)
        checksum = hashlib.sha256(target.read_bytes()).hexdigest()
        checksums.append(f'{checksum}  {name}\n')
    (out / 'SHA256SUMS.txt').write_text(''.join(checksums))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
print(json.dumps({'files':len(files),'destination':str(out),'sha256':digest}))
