import json, os, subprocess, time, sys
from pathlib import Path
os.umask(0o077)
root=Path('/queue')
for p in root.glob('*.running'):
    p.with_suffix('.result').write_text(json.dumps({'exit_code':125,'error':'worker restarted; no replay'}))
    p.unlink()
print('Epic helper worker ready',flush=True)
while True:
    for p in sorted(root.glob('*.request')):
        running=p.with_suffix('.running');p.rename(running)
        try:
            job=json.loads(running.read_text())
            if job.get('phase') not in ('login','claim'): raise ValueError('unsupported phase')
            if time.time()-job['created']>300: raise ValueError('expired request')
            with running.with_suffix('.log').open('w') as log:
                proc=subprocess.run(['timeout','--signal=TERM','--kill-after=30','1230',sys.executable,'/adapter/run.py',job['phase']],stdout=log,stderr=subprocess.STDOUT)
            result={'exit_code':proc.returncode,'finished':time.time()}
        except Exception as e: result={'exit_code':125,'error':str(e)}
        tmp=running.with_suffix('.tmp');tmp.write_text(json.dumps(result));tmp.replace(running.with_suffix('.result'));running.unlink()
    time.sleep(1)
