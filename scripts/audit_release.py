#!/usr/bin/env python3
"""Audit the release allowlist and, when present, tracked Git paths."""
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
def audit():
    files=json.loads((ROOT/'release-files.json').read_text())['files']+['release-files.json']
    if len(files)!=len(set(files)): raise ValueError('Duplicate allowlist path')
    checks=[r'gh[pousr]_[A-Za-z0-9]{30,}',r'sk-[A-Za-z0-9_-]{24,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'/(?:Users|home)/[A-Za-z0-9_.-]+/',r'[A-Z]:\\Users\\[^\\]+\\']
    for name in files:
        p=ROOT/name
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(ROOT): raise ValueError('Invalid path: '+name)
        if p.suffix in ('.sqlite','.db','.pdf','.xlsx','.csv') or p.name in ('profile.json','demographics.json','permissions.json'):
            raise ValueError('Private/generated file: '+name)
        text=p.read_text()
        if any(re.search(pattern,text) for pattern in checks): raise ValueError('Possible secret or local identity path in '+name)
    if (ROOT/'.git').exists():
        tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
        extra=set(filter(None,tracked))-set(files)
        if extra: raise ValueError('Tracked files outside release allowlist: '+', '.join(sorted(extra)))
    return files

if __name__=='__main__':print('Release audit passed: '+str(len(audit()))+' allowed files. Review free-text content for personal data before publishing.')
