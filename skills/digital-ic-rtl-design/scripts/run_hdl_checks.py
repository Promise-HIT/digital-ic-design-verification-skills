#!/usr/bin/env python3
"""Execute explicitly configured project checks, preserving logs and actual results.

JSON: {"checks":[{"name":"smoke","argv":["make","smoke"],
"timeout_seconds":120,"required":true}]}
Commands are trusted project commands selected by the caller, never inferred from PDFs.
"""
import argparse
import datetime
import json
import os
import re
import signal
import subprocess
import time
from pathlib import Path

def run(manifest,repo,out):
    data=json.loads(manifest.read_text(encoding='utf-8-sig'))
    checks=data.get('checks')
    if not isinstance(checks,list) or not checks:raise ValueError('checks must be a nonempty list')
    names=set()
    for c in checks:
        if not isinstance(c,dict):raise ValueError('check must be an object')
        name=c.get('name','');argv=c.get('argv');timeout=c.get('timeout_seconds',120)
        if not re.fullmatch(r'[A-Za-z0-9_-]+',name) or name in names:raise ValueError('check names must be unique safe names')
        names.add(name)
        if not isinstance(argv,list) or not argv or any(not isinstance(a,str) or not a for a in argv):raise ValueError('argv must be a nonempty list of nonempty strings')
        if not isinstance(timeout,(int,float)) or isinstance(timeout,bool) or not 0<timeout<=86400:raise ValueError('timeout_seconds must be in (0,86400]')
        if 'required' in c and not isinstance(c['required'],bool):raise ValueError('required must be a boolean')
    # A new run directory prevents stale logs being mistaken for current evidence.
    out.mkdir(parents=True,exist_ok=False)
    results=[]; failed=False
    for c in checks:
        row={'name':c['name'],'argv':c['argv'],'cwd':str(repo),'required':c.get('required',True),
             'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        log=out/(c['name']+'.log');row['log']=str(log);start=time.monotonic()
        try:
            with log.open('wb') as f:
                proc=subprocess.Popen(c['argv'],cwd=repo,stdout=f,stderr=subprocess.STDOUT,
                    shell=False,start_new_session=(os.name!='nt'))
                try:proc.wait(timeout=c.get('timeout_seconds',120))
                except subprocess.TimeoutExpired:
                    if os.name=='nt':
                        subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],stdout=f,stderr=subprocess.STDOUT)
                    else:
                        try:os.killpg(proc.pid,signal.SIGKILL)
                        except ProcessLookupError:pass
                    if proc.poll() is None:proc.kill()
                    proc.wait()
                    raise
            row.update(exit_code=proc.returncode,status='pass' if proc.returncode==0 else 'fail')
        except subprocess.TimeoutExpired:
            row.update(exit_code=None,status='timeout')
        except OSError as e:
            row.update(exit_code=None,status='unavailable',error=str(e))
        row['seconds']=round(time.monotonic()-start,3);results.append(row)
        if row['required'] and row['status']!='pass':failed=True
        pending=[{'name':x['name'],'argv':x['argv'],'status':'not_run'} for x in checks[len(results):]]
        (out/'results.json').write_text(json.dumps({'checks':results,'not_run':pending,'run_finished':failed or not pending,'required_checks_pass':not failed and not pending,
            'limitation':'Exit codes only; inspect simulator/UVM/checker reports and tool versions separately.'},ensure_ascii=False,indent=2),encoding='utf-8')
        print(c['name']+': '+row['status'],flush=True)
        if failed:break
    return 1 if failed else 0

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest',type=Path);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    try:
        repo=a.repo.resolve()
        if not repo.is_dir():raise ValueError('repo must exist')
        return run(a.manifest,repo,a.out.resolve())
    except (OSError,ValueError,KeyError,TypeError) as e:p.exit(2,f'Configuration error: {e}\n')

if __name__=='__main__':raise SystemExit(main())
