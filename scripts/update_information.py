#!/usr/bin/env python3
from __future__ import annotations
import json, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config'/'approved-sources.json'
DATA=ROOT/'data'/'current'/'grants.json'
HISTORY=ROOT/'data'/'history'

def main()->int:
    cfg=json.loads(CONFIG.read_text(encoding='utf-8'))
    data=json.loads(DATA.read_text(encoding='utf-8'))
    checked=datetime.now(timezone.utc).isoformat()
    results=[]
    for src in cfg['sources']:
        if not src.get('enabled',True): continue
        ok=False; code=None; error=None
        req=urllib.request.Request(src['url'],headers={'User-Agent':'LawEnforcementGrantFinder/1.0'})
        try:
            with urllib.request.urlopen(req,timeout=cfg.get('timeout_seconds',25)) as r:
                code=getattr(r,'status',200); r.read(1024); ok=200<=code<400
        except Exception as exc:
            error=str(exc)
        results.append({**src,'available':ok,'status_code':code,'checked_at':checked,'error':error})
    data['last_updated']=checked
    data['sources']=results
    DATA.write_text(json.dumps(data,indent=2)+"\n",encoding='utf-8')
    HISTORY.mkdir(parents=True,exist_ok=True)
    (HISTORY/(checked.replace(':','-')+'.json')).write_text(json.dumps({'checked_at':checked,'sources':results},indent=2)+"\n",encoding='utf-8')
    print(f'Checked {len(results)} approved sources.')
    return 0 if any(r['available'] for r in results) else 1
if __name__=='__main__': raise SystemExit(main())
