"""Report filenames only for potential secrets; never print matching values."""
import json
from pathlib import Path
import re
import subprocess

paths=set(subprocess.check_output(['git','ls-files','-z']).decode().split('\0'))
paths.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0'))
patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{20,}',r'sk-[A-Za-z0-9_-]{20,}',r'postgres(?:ql)?://[^\s]+:[^\s]+@',r'AKIA[A-Z0-9]{16}']
findings=[]
blocked=[]
for name in sorted(filter(None,paths)):
    p=Path(name)
    if (p.name.startswith('.env') and p.name!='.env.example') or p.suffix.lower()=='.pdf' or name.startswith(('data/raw/','data/extracted/','tmp/')):
        blocked.append(name)
    if p.suffix.lower() not in ['.jpg','.png']:
        text=p.read_text(encoding='utf-8')
        findings.extend({'file':name,'pattern':i} for i,pattern in enumerate(patterns) if re.search(pattern,text))
print(json.dumps({'files':len(paths)-1,'forbidden_artifacts':blocked,'potential_secrets':findings,'intentional_binary':'preview/mobile-briefing.jpg: reviewed screenshot'},indent=2))
raise SystemExit(1 if blocked or findings else 0)
