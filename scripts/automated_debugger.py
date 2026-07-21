#!/usr/bin/env python3
from __future__ import annotations
import compileall,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)
required=['index.html','style.css','app.js','README.md','config/approved-sources.json','data/current/grants.json','scripts/update_information.py']
checks=[]
for rel in required: checks.append({'name':f'Required file: {rel}','passed':(ROOT/rel).exists()})
for p in ROOT.rglob('*.json'):
    try: json.loads(p.read_text(encoding='utf-8')); checks.append({'name':f'Valid JSON: {p.relative_to(ROOT)}','passed':True})
    except Exception as e: checks.append({'name':f'Valid JSON: {p.relative_to(ROOT)}','passed':False,'error':str(e)})
checks.append({'name':'Python syntax','passed':compileall.compile_dir(str(ROOT/'scripts'),quiet=1,force=True)})
try:
    r=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests'],cwd=ROOT,text=True,capture_output=True,timeout=180)
    checks.append({'name':'Unit tests','passed':r.returncode==0,'stdout':r.stdout[-4000:],'stderr':r.stderr[-4000:]})
except Exception as e: checks.append({'name':'Unit tests','passed':False,'error':str(e)})
status='PASSED' if all(c['passed'] for c in checks) else 'FAILED'
report={'generated_at':datetime.now(timezone.utc).isoformat(),'status':status,'checks':checks}
(REPORTS/'latest-debug-report.json').write_text(json.dumps(report,indent=2)+"\n",encoding='utf-8')
lines=['# Automated Debug Report','',f"Status: **{status}**",'']+[f"- {'PASS' if c['passed'] else 'FAIL'} — {c['name']}" for c in checks]
(REPORTS/'latest-debug-report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(status); raise SystemExit(0 if status=='PASSED' else 1)
