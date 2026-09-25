"""Apply the user's explicit working-repository update, preserving incomplete-release gates.

This publishes the reviewed available collection with pending items disclosed. It is
not a full-release certificate and does not weaken article_release.py's final gates.
Archive every old file before any file-level replacement/removal; preserve dirty files.
"""
import argparse, collections, json, os, pathlib, shutil, subprocess
from article_release import ROOT, ARTICLE, inventory, contained, identity, read, sha, save_new, utc, verify

NAME='working-article-update-20260925-v1'
WORK=ROOT/'reporting'/NAME
STAGE=ROOT/'article-staging/Article-collection-20260925-v4'
ARCHIVE=ROOT/'archive'/NAME
SCOPES=('Figures','Tables','Results','Supplemental materials','Article and bibliography')
TOP=('README.md','article-diagrams.json','manuscript-exhibits.json')
def git(*args):return subprocess.check_output(['git',*args],cwd=ARTICLE)
def allfiles(root, scopes):
    out={i['RelativePath']:i for i in inventory(root,scopes,include_readme=False).values()}
    for rel in TOP:
        p=contained(root,rel)
        if p.exists():out[rel]=dict(RelativePath=rel,Sha256=sha(p),Bytes=p.stat().st_size)
    return out
def protected(rel,dirty):
    return rel in dirty or rel.startswith(('Article and bibliography/','Supplemental materials/Risk aversion utility curves/')) or rel.lower().endswith('.bak')
def write(rel,text):
    p=contained(WORK/'overlay',rel);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def prepare():
    WORK.mkdir(parents=True,exist_ok=False)
    validation=read(ROOT/'validation/prepared-article-collection-v4.json');assert validation['Passed']
    for item in validation['Files']:verify(item['Identity'])
    status=git('status','--porcelain=v1','-z')
    assert not git('diff','--cached','--name-only'), 'Preserve an existing staged change set'
    dirty={s[3:].decode() for s in status.split(b'\0') if s}
    save_new(WORK/'initial-status.json',dict(CreatedUtc=utc(),Head=git('rev-parse','HEAD').decode().strip(),Status=status.decode(),DirtyPaths=sorted(dirty)))
    old=allfiles(ARTICLE,SCOPES)
    m=read(STAGE/'Results/Run records/numbered-exhibits-manifest.json')
    write('README.md',(STAGE/'README.md').read_text(encoding='utf-8').replace('# Article tables, figures and supplemental materials','# Correlated-signals litigation article')+
          '\n[Manuscript and bibliography](Article%20and%20bibliography/) remain in their existing folder. This is the reviewed available working collection, not a certificate of completed final publication. Historical generated material is preserved in the external hash-verified archive identified in Results/Run records/working-collection-update.json.\n')
    write('Results/README.md','# Results\n\nThe selected agreement-enabled collection has 72 audited profiles out of 74 planned; all 20 main American/British cost-series profiles are present.\n\n- [Individual simulations](Individual%20simulations/README.md)\n- [Aggregated data](Aggregated%20Data/README.md)\n- [Run records](Run%20records/README.md)\n\nTwo risk-averse British grid comparisons remain pending in the latest recorded catalog. Trial-only fee shifting is retained at cost multiplier 1. Historical 276-case outputs have been archived outside this repository.\n')
    subs=[p.name for p in (STAGE/'Supplemental materials').iterdir() if p.is_dir()]
    from urllib.parse import quote
    write('Supplemental materials/README.md','# Supplemental materials\n\nCurrent materials retain the existing folder structure. Exact primary profiles, approximate multiple-start results and solver trajectories remain distinct.\n\n'+'\n'.join('- ['+s+']('+quote(s)+'/README.md)' for s in subs if (STAGE/'Supplemental materials'/s/'README.md').exists())+'\n\nThe utility curves are unchanged. Three endpoint-verified trajectory viewers are provided for review; the fourth replay and interactive viewer QA remain pending.\n')
    entries=[]
    for a in m['Artifacts']:
        entries.append(dict(Exhibit=a['Title'],Output=a['Folder']+'/'+pathlib.Path(a['PDF']['Path']).name,Sha256=a['PDF']['Sha256'],Caption=a['Folder']+'/Sources/'+pathlib.Path(a['Caption']['Path']).name,Data=a['Folder']+'/Sources/'+pathlib.Path(a['Data']['Path']).name))
    write('manuscript-exhibits.json',json.dumps(dict(Schema='current-numbered-exhibits-v1',CreatedUtc=utc(),Exhibits=entries,SourceManifest='Results/Run records/numbered-exhibits-manifest.json',Figure7ReplacesTable4=True,CompleteArticlePublication=False),indent=2)+'\n')
    write('article-diagrams.json',json.dumps(dict(Schema='reviewed-article-rendering-index-v1',NumberedExhibits='manuscript-exhibits.json',RenderSources=['Figures/Sources','Tables/Sources','Results/Run records/Sources'],ExecutedCommands='Results/Run records/Commands',CurrentCollection='Results/Run records/staging-manifest.json',AutomaticSolverLaunch=False,Legacy276CaseRebuildRetired=True),indent=2)+'\n')
    write('Results/Run records/working-collection-update.json',json.dumps(dict(Schema='authorized-working-collection-update-v1',CreatedUtc=utc(),Authorization='User explicitly requested all article repository folders updated, superseded files removed and changes committed on September 25, 2026.',Archive=str(ARCHIVE),FileLevelPlan=str(WORK/'plan.json'),Validation=identity(ROOT/'validation/prepared-article-collection-v4.json'),FinalPublicationComplete=False,Pending=validation['Pending']),indent=2)+'\n')
    new={r:dict(i,Source=identity(contained(STAGE,r))) for r,i in allfiles(STAGE,SCOPES[:-1]).items()}
    for f in (WORK/'overlay').rglob('*'):
        if f.is_file():
            rel=f.relative_to(WORK/'overlay').as_posix();new[rel]=dict(RelativePath=rel,Sha256=sha(f),Bytes=f.stat().st_size,Source=identity(f))
    actions=[]
    for rel in sorted(set(old)|set(new)):
        b,a=old.get(rel),new.get(rel)
        if protected(rel,dirty):
            if a and b:assert a['Sha256']==b['Sha256'], 'Protected staged conflict: '+rel
            kind='Retain';reason='Preserve user working changes, manuscript/bibliography, backups and utility curves'
        elif a:
            kind='Add' if not b else 'Retain' if a['Sha256']==b['Sha256'] else 'Replace';reason='Reviewed current selected artifact or current navigation/provenance'
        else:kind='Remove';reason='Superseded generated artifact absent from the selected current collection; archived before removal'
        actions.append(dict(RelativePath=rel,Action=kind,Reason=reason,Old=b,New=a))
    save_new(WORK/'plan.json',dict(CreatedUtc=utc(),OldFiles=old,Actions=actions,DirtyPaths=sorted(dirty),Validation=identity(ROOT/'validation/prepared-article-collection-v4.json')))
    ARCHIVE.mkdir(parents=True,exist_ok=False)
    for rel,item in old.items():
        src=contained(ARTICLE,rel);dst=contained(ARCHIVE/'files',rel);dst.parent.mkdir(parents=True,exist_ok=True)
        assert sha(src)==item['Sha256'];shutil.copy2(src,dst);assert sha(dst)==item['Sha256']
    assert allfiles(ARTICLE,SCOPES)==old, 'Repository changed during archival'
    save_new(ARCHIVE/'archive-manifest.json',dict(Passed=True,CreatedUtc=utc(),Plan=identity(WORK/'plan.json'),Files=old,InitialStatus=read(WORK/'initial-status.json')))
    print(json.dumps(dict(ArchivedFiles=len(old),Counts=dict(collections.Counter(a['Action'] for a in actions)),Plan=str(WORK/'plan.json'))))
def apply():
    plan=read(WORK/'plan.json');archive=read(ARCHIVE/'archive-manifest.json');assert archive['Passed'];verify(archive['Plan'])
    assert allfiles(ARTICLE,SCOPES)==plan['OldFiles'], 'Repository changed since archive'
    assert git('status','--porcelain=v1','-z').decode()==read(WORK/'initial-status.json')['Status']
    for item in plan['Actions']:
        rel=item['RelativePath'];target=contained(ARTICLE,rel)
        if item['Old']:assert sha(contained(ARCHIVE/'files',rel))==item['Old']['Sha256']
        if item['New']:verify(item['New']['Source'])
    with (ARCHIVE/'application-journal.jsonl').open('x',encoding='utf-8') as log:
        for item in plan['Actions']:
            if item['Action']=='Retain':continue
            rel=item['RelativePath'];target=contained(ARTICLE,rel)
            assert sha(target)==item['Old']['Sha256'] if item['Old'] else not target.exists()
            log.write(json.dumps(dict(Phase='Intent',RelativePath=rel,Action=item['Action']))+'\n');log.flush()
            if item['Action']=='Remove':target.unlink() # One archived, resolved literal file; never recursive deletion.
            else:
                source=verify(item['New']['Source']);target.parent.mkdir(parents=True,exist_ok=True)
                temporary=target.with_name(target.name+'.article-update-tmp');assert not temporary.exists()
                shutil.copy2(source,temporary);assert sha(temporary)==item['New']['Sha256'];os.replace(temporary,target)
            log.write(json.dumps(dict(Phase='Applied',RelativePath=rel))+'\n');log.flush()
    for item in plan['Actions']:
        p=contained(ARTICLE,item['RelativePath'])
        if item['Action']=='Remove':assert not p.exists()
        else:assert sha(p)==(item['New'] or item['Old'])['Sha256']
    # Remove only verified empty generated directories, deepest first; no recursive operation.
    for scope in SCOPES[:-1]:
        for p in sorted((ARTICLE/scope).rglob('*'),key=lambda p:len(p.parts),reverse=True):
            if p.is_dir() and not any(p.iterdir()) and not p.is_relative_to(ARTICLE/'Supplemental materials/Risk aversion utility curves'):
                contained(ARTICLE,p.relative_to(ARTICLE).as_posix()).rmdir()
    save_new(ARCHIVE/'application-result.json',dict(Passed=True,FinishedUtc=utc(),Plan=identity(WORK/'plan.json'),Counts=dict(collections.Counter(a['Action'] for a in plan['Actions'])),FinalPublicationComplete=False))
    changed=[a['RelativePath'] for a in plan['Actions'] if a['Action']!='Retain']
    paths=WORK/'commit-paths.bin';paths.write_bytes(b'\0'.join(p.encode() for p in changed)+b'\0')
    subprocess.run(['git','add','-A','--pathspec-from-file='+str(paths),'--pathspec-file-nul'],cwd=ARTICLE,check=True)
    commit_applied()
def commit_applied():
    plan=read(WORK/'plan.json');assert read(ARCHIVE/'application-result.json')['Passed']
    changed={a['RelativePath'] for a in plan['Actions'] if a['Action']!='Retain'}
    for a in plan['Actions']:
        target=contained(ARTICLE,a['RelativePath'])
        if a['Action']=='Remove':assert not target.exists()
        else:assert sha(target)==(a['New'] or a['Old'])['Sha256']
    # Rename detection combines deletion/addition pairs and hides an old path from
    # --name-only. Verify the complete literal change set with detection disabled.
    actual=set(git('diff','--cached','--no-renames','--name-only','-z').decode().strip('\0').split('\0'));assert actual==changed
    subprocess.run(['git','commit','-q','-m','Refresh reviewed article figures, tables and supplemental collection'],cwd=ARTICLE,check=True,stdout=subprocess.DEVNULL)
    save_new(WORK/'commit.json',dict(Commit=git('rev-parse','HEAD').decode().strip(),Application=identity(ARCHIVE/'application-result.json'),RemainingWorkingStatus=git('status','--porcelain=v1').decode()))
    print(json.dumps(read(WORK/'commit.json')))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','apply','commit']);a=p.parse_args()
    {'prepare':prepare,'apply':apply,'commit':commit_applied}[a.mode]()
