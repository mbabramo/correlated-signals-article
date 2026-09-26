"""Rebuild and regenerate the article Results collection from frozen complete profiles."""
import argparse, concurrent.futures, csv, datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, zipfile
PACKAGE=pathlib.Path(__file__).resolve().parent
ENV=dict(os.environ,DOTNET_PROCESSOR_COUNT='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def identity(p):return dict(Path=str(pathlib.Path(p).resolve()),Sha256=sha(p))
def save(p,x):
    p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f:json.dump(x,f,indent=2,allow_nan=False)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def extract(source,destination):
    with zipfile.ZipFile(source) as z:
        for n in z.namelist():
            if not (destination/n).resolve().is_relative_to(destination.resolve()):raise ValueError('Unsafe archive path')
        z.extractall(destination)
def check_package():
    manifest=read(PACKAGE/'package-manifest.json')
    for row in manifest['Files']:
        if sha(PACKAGE/row['Path'])!=row['Sha256']:raise ValueError('Changed package file: '+row['Path'])
    return manifest
def command(work,name,args,cwd=None):
    logs=work/'logs';logs.mkdir(exist_ok=True)
    record=logs/(name+'.json')
    if record.exists():raise FileExistsError('Command was already attempted: '+name)
    before=utc()
    with (logs/(name+'.stdout.log')).open('xb') as out,(logs/(name+'.stderr.log')).open('xb') as err:
        child=subprocess.run([str(x) for x in args],cwd=cwd or work,env=ENV,stdout=out,stderr=err,
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    save(record,dict(Command=[str(x) for x in args],WorkingDirectory=str(cwd or work),StartedUtc=before,FinishedUtc=utc(),ExitCode=child.returncode,Environment={k:ENV[k] for k in ['DOTNET_PROCESSOR_COUNT','OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']}))
    if child.returncode:raise RuntimeError(f'{name} failed: see {logs}')
def write_csv(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def safe_publish(staged,destination,archive):
    """Copy generated files only; retain every unrelated file and archive replacements."""
    destination.mkdir(parents=True,exist_ok=True);changes=[]
    for src in sorted(staged.rglob('*')):
        if not src.is_file():continue
        # LaTeX diagnostics remain in the isolated run, outside the reader collection.
        if src.suffix.lower() in ['.aux','.log','.out','.toc','.gz'] and src.parent.parent.name=='Individual simulations':continue
        rel=src.relative_to(staged);dst=destination/rel
        if dst.exists() and sha(dst)==sha(src):continue
        prior=None
        if dst.exists():
            backup=archive/rel;backup.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(dst,backup);assert sha(dst)==sha(backup);prior=identity(backup)
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);assert sha(dst)==sha(src)
        changes.append(dict(RelativePath=rel.as_posix(),Previous=prior,Current=identity(dst)))
    return changes

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=pathlib.Path,required=True,help='Results destination; unrelated files are retained')
    p.add_argument('--work',type=pathlib.Path,required=True,help='Fresh isolated build and log directory')
    p.add_argument('--workers',type=int,default=1,help='Concurrent single-thread reports, default 1; include other work within 32')
    p.add_argument('--build-only',action='store_true',help=argparse.SUPPRESS)
    args=p.parse_args();work=args.work.resolve();dest=args.output.resolve()
    if not 1<=args.workers<=32:raise ValueError('Workers must be 1..32')
    if work.exists():raise FileExistsError('Preserve prior runs: choose a new --work directory')
    if dest==work or dest.is_relative_to(work) or work.is_relative_to(dest) or dest==PACKAGE or PACKAGE.is_relative_to(dest):raise ValueError('Build, source and destination must be separate')
    manifest=check_package();work.mkdir(parents=True)
    save(work/'started.json',dict(StartedUtc=utc(),Command=sys.argv,Package=identity(PACKAGE/'package-manifest.json'),Workers=args.workers,SolvesStarted=0))
    try:
        command(work,'pipeline-tests',[sys.executable,PACKAGE/'test_pipeline.py'])
        extract(PACKAGE/'solver-source.zip',work/'solver')
        shutil.copytree(PACKAGE/'host',work/'host');shutil.copy2(PACKAGE/'global.json',work/'global.json')
        for name in ['ACESimBase','LitigCharts']:
            lock=PACKAGE/'locks'/name/'packages.lock.json'
            if lock.exists():shutil.copy2(lock,work/'solver'/name/'packages.lock.json')
        host_lock=PACKAGE/'locks/Reports/packages.lock.json'
        if host_lock.exists():shutil.copy2(host_lock,work/'host/packages.lock.json')
        command(work,'dotnet-info',['dotnet','--info'])
        restore=['dotnet','restore',work/'host/Reports.csproj','--use-lock-file','--disable-parallel']
        if (PACKAGE/'locks/ACESimBase/packages.lock.json').exists():restore+=['--locked-mode']
        command(work,'restore',restore)
        command(work,'build',['dotnet','build',work/'host/Reports.csproj','-c','Release','--no-restore','-m:1','/p:UseSharedCompilation=false','-o',work/'runtime'])
        save(work/'build.json',dict(Passed=True,Source=read(PACKAGE/'source-provenance.json'),RuntimeFiles=[identity(x) for x in sorted((work/'runtime').rglob('*')) if x.is_file()]))
        if args.build_only:return
        def host(name,mode,*argv):return command(work,name,['dotnet',work/'runtime/Reports.dll',mode,*argv])
        output=work/'Results';output.mkdir();raw=work/'primary';raw.mkdir()
        requests=[];cases=read(PACKAGE/'inputs/primary.json')
        for original in cases:
            r=json.loads(json.dumps(original));r['Output']=str(raw/r['CaseId'])
            for key in ['ExpectedAudit','ExpectedProfile']:r[key]=str(PACKAGE/r[key])
            for item in r['Inputs'].values():item['Path']=str(PACKAGE/item['Path'])
            req=work/'requests'/('primary-'+r['CaseId']+'.json');save(req,r);requests.append(req)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(lambda r:host(r.stem,'primary',r),requests))
        command(work,'primary-reports',[sys.executable,PACKAGE/'python/primary_reports.py','--package',PACKAGE,'--work',work])
        # Existing four-corner evaluator performs endpoint validation and all replay/accounting checks.
        pairs=[];by_id={c['CaseId']:c for c in cases}
        seen=set()
        for a in cases:
            if a['Case']['FeeRule']!='american':continue
            b_id=a['CaseId'].replace('__american__','__complete__')
            if b_id not in by_id:continue
            b=by_id[b_id]
            def endpoint(c):return dict(Case=c['Case'],EquilibriumFile=str(PACKAGE/c['Inputs']['Equilibrium']['Path']),ActionReportFile=str(PACKAGE/c['Inputs']['Actions']['Path']),NumericReportFile=str(PACKAGE/c['Inputs']['Numeric']['Path']),EquilibriumNumber=1)
            name=a['CaseId'].replace('__american__','__pair__');r=dict(Id=name,American=endpoint(a),Complete=endpoint(b),TruthMapExponents=[1.0])
            req=work/'requests'/('welfare-'+name+'.json');save(req,r);pairs.append((name,req))
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(lambda pair:host('welfare-'+pair[0],'welfare','--request',pair[1],'--output',work/'welfare'/pair[0]),pairs))
        command(work,'welfare-reports',[sys.executable,PACKAGE/'python/welfare_reports.py','--package',PACKAGE,'--work',work])
        command(work,'main-welfare-render',[sys.executable,PACKAGE/'python/draw_main_welfare_decomposition.py','--catalog',output/'Aggregated Data/selected-primary-catalog.json','--wave',work/'welfare-wave.json','--output',work/'main-welfare-render'])
        for f in (work/'main-welfare-render').iterdir():
            if f.is_file():shutil.copy2(f,output/'Aggregated Data/Main-welfare-decomposition'/f.name)
        tremble=work/'tremble';(tremble/'inputs/run-v1').mkdir(parents=True);(tremble/'results').mkdir();(tremble/'reports').mkdir()
        profiles=read(PACKAGE/'inputs/profiles.json');games=read(PACKAGE/'inputs/games.json')
        for r in profiles:r['FrozenFile']=str(PACKAGE/r['FrozenFile'])
        save(tremble/'inputs/profiles.json',profiles);shutil.copy2(PACKAGE/'inputs/tremble-protocol.json',tremble/'inputs/protocol.json')
        requests=[]
        for case,g in games.items():
            ps=[r for r in profiles if r['CaseId']==case]
            for n in range(8):
                if not ps[n::8]:continue
                name=case+'-part-'+str(n);r=dict(**g,Profiles=ps[n::8],Epsilons=[.001,.005,.01],Directions=5,Output=str(tremble/'results'/name))
                req=tremble/'inputs/run-v1'/(name+'.json');save(req,r);requests.append(req)
        save(tremble/'suite-started.json',dict(StartedUtc=utc(),Workers=args.workers,Requests=[identity(r) for r in requests],SolvesStarted=0))
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(lambda r:host('tremble-'+r.stem,'tremble',r),requests))
        save(tremble/'suite-completed.json',dict(Passed=True,FinishedUtc=utc(),SolvesStarted=0))
        host('independent-validation','verify',tremble)
        command(work,'tremble-reports',[sys.executable,PACKAGE/'python/tremble_report.py','--work',tremble,'--output',output/'Aggregated Data/Equilibrium sensitivity'])
        command(work,'report-validation',[sys.executable,PACKAGE/'python/check_reports.py','--package',PACKAGE,'--work',work])
        # Every profile's existing presentation is rendered from freshly revalidated data.
        sources=sorted((output/'Individual simulations').glob('*/Sources/strategy.tex'))
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(lambda s:command(work,'latex-'+s.parent.parent.name,['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(s.parent.parent),s]),sources))
        for name in ['host','python']:shutil.copytree(PACKAGE/name,output/'Run records/Reproduction sources'/name)
        shutil.copy2(PACKAGE/'source-provenance.json',output/'Run records/source-provenance.json')
        save(output/'Run records/reproduction.json',dict(Passed=True,FinishedUtc=utc(),WorkDirectory=str(work),Package=identity(PACKAGE/'package-manifest.json'),Build=identity(work/'build.json'),Validation=identity(work/'report-validation.json'),Commands=[identity(x) for x in sorted((work/'logs').glob('*.json'))],PrimaryProfiles=len(cases),WelfarePairs=len(pairs),TrembleProfiles=len(profiles),IndependentChecks=32,SolvesStarted=0,CompleteArticle=False))
        (output/'README.md').write_text('# Results\n\nRebuilt from the frozen validated profiles: '+str(len(cases))+' primary profiles, '+str(len(pairs))+' four-corner welfare comparisons, and '+str(len(profiles))+' tremble-sensitivity profiles.\n\n- [Individual simulations](Individual%20simulations/README.md)\n- [Aggregated data](Aggregated%20Data/README.md)\n- [Tremble sensitivity](Aggregated%20Data/Equilibrium%20sensitivity/Report.md)\n- [Reproduction record](Run%20records/reproduction.json)\n\nThe two incomplete British risk-averse grid cases remain explicitly missing. No new equilibrium was solved.\n',encoding='utf-8')
        check_package()
        changes=safe_publish(output,dest,work/'archive')
        save(work/'completed.json',dict(Passed=True,FinishedUtc=utc(),Results=str(dest),Changes=changes,SolvesStarted=0))
        print(f'Completed: {len(cases)} primary profiles, {len(pairs)} welfare pairs, {len(profiles)} tremble profiles. Results: {dest}',flush=True)
    except BaseException as e:
        save(work/'failed.json',dict(Passed=False,FinishedUtc=utc(),Error=repr(e)));raise

if __name__=='__main__':main()
