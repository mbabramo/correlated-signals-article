"""One command: rebuild the numerical/report projects and populate Results from saved profiles."""
import argparse,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,uuid,zipfile
REPO=pathlib.Path(__file__).resolve().parent
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workers',type=int,default=1,help='Concurrent single-thread report workers (1–32); include existing work in the machine total')
    p.add_argument('--output',type=pathlib.Path,default=REPO/'Results',help='Results destination; existing replaced files are archived, unrelated files retained')
    p.add_argument('--work',type=pathlib.Path,help='Fresh build/log directory (default .reproduction/<timestamp>)')
    a=p.parse_args()
    if not 1<=a.workers<=32:p.error('--workers must be 1..32')
    if sys.version_info<(3,12):p.error('Python 3.12 or newer is required')
    for executable in ['dotnet','lualatex']:
        if not shutil.which(executable):p.error(executable+' is not on PATH; see the reproduction README')
    try:import matplotlib
    except ImportError:p.error('Install the pinned requirements from Results/Run records/Reproduction/requirements.txt')
    # OS ownership prevents duplicate reports even if an earlier caller has not returned.
    lock_path=REPO/'.reproduction/active.lock';lock_path.parent.mkdir(parents=True,exist_ok=True)
    lock=lock_path.open('a+b')
    if lock_path.stat().st_size==0:lock.write(b'1');lock.flush()
    lock.seek(0)
    try:
        if os.name=='nt':
            import msvcrt
            msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except OSError:
        lock.close();p.error('Another Results regeneration is already running for this repository')
    source=REPO/'Results/Run records/Reproduction'
    distribution=json.loads((source/'distribution.json').read_text(encoding='utf-8'))
    for item in distribution['Files']:
        path=(source/item['Path']).resolve()
        if not path.is_relative_to(source.resolve()) or digest(path)!=item['Sha256']:raise ValueError('Distribution hash mismatch: '+item['Path'])
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=(a.work or REPO/'.reproduction'/stamp).resolve();root.mkdir(parents=True,exist_ok=False)
    package=root/'package';package.mkdir()
    for src in source.rglob('*'):
        if not src.is_file() or src.name in ['inputs.zip','distribution.json'] or '__pycache__' in src.parts:continue
        dest=package/src.relative_to(source);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    with zipfile.ZipFile(source/'inputs.zip') as archive:
        for name in archive.namelist():
            if not (package/name).resolve().is_relative_to(package):raise ValueError('Unsafe input archive path')
        archive.extractall(package)
    argv=[sys.executable,str(package/'pipeline.py'),'--work',str(root/'build'),'--output',str(a.output.resolve()),'--workers',str(a.workers)]
    (root/'entry-command.json').write_text(json.dumps(dict(Command=argv,DistributionSha256=digest(source/'distribution.json')),indent=2))
    print('Rebuilding and regenerating saved-profile reports. Logs: '+str(root/'build/logs'),flush=True)
    try:
        return subprocess.call(argv,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    finally:lock.close()
if __name__=='__main__':sys.exit(main())
