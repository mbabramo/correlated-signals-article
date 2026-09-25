"""Prepare, validate, archive and apply the authorized Figure 8 working update.

No solver, final-release certification, broad cleanup or unrelated file staging.
"""
import argparse, json, pathlib, re, shutil, subprocess
from article_release import ROOT, ARTICLE, identity, read, sha, save_new, utc
from multiple_welfare_figure import TITLE, generate

TASK=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to')
WORK=ROOT/'work/manuscript-figure8-20260925-v2'
DELTA=WORK/'delta'
FIG=TASK/'outputs/Multiple-equilibrium-welfare-figure-20260925-v4'
ARCHIVE=ROOT/'archive/table6-to-figure8-20260925-v1'
OLD='Table 6 - Disposition ranges'

def write(rel,text):
    path=DELTA/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')

def put(source,rel):
    path=DELTA/rel;path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,path)

def update(rel,old,new):
    p=DELTA/rel
    s=(p if p.exists() else ARTICLE/rel).read_text(encoding='utf-8')
    assert old in s,(rel,old);write(rel,s.replace(old,new))

def protected():
    names=['Article and bibliography/corr_signals'+x for x in ('.aux','.log','.synctex.gz','.tex.bak')]+['Tables/Sources/Table 1 - Model primitives.tex.bak']
    names += [p.relative_to(ARTICLE).as_posix() for p in (ARTICLE/'Supplemental materials/Risk aversion utility curves').rglob('*') if p.is_file()]
    return {n:sha(ARTICLE/n) for n in names}

def prepare():
    WORK.mkdir(exist_ok=False);DELTA.mkdir();FIG.mkdir(exist_ok=False)
    artifact=generate(FIG)
    for p in (FIG/'Figures').rglob('*'):
        if p.is_file():put(p,p.relative_to(FIG))
    put(ARTICLE/f'Tables/Sources/{OLD}.json','Supplemental materials/Multiple equilibria/Sources/disposition-ranges.json')
    # Reviewed old display sources are archived on application; full research data stay.
    removed=[p.relative_to(ARTICLE).as_posix() for p in (ARTICLE/'Tables').rglob(OLD+'*') if p.is_file()]
    removed += ['Supplemental materials/Multiple equilibria/'+n for n in ('multiple-outcomes.png','multiple-outcomes.svg','Sources/reproduce.py')]
    for folder in ('Figures','Tables'):
        rel=folder+'/README.md'
        update(rel,'Figure 7 replaces Table 4 in Welfare Analysis; other file identifiers are unchanged.',
               'Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria. Other file identifiers are unchanged.')
    update('Tables/README.md','- [Table 6 - Disposition ranges](Table%206%20-%20Disposition%20ranges.pdf)\n','')
    p=DELTA/'Figures/README.md';p.write_text(p.read_text(encoding='utf-8')+'- [Figure 8 - Multiple equilibrium welfare outcomes](Figure%208%20-%20Multiple%20equilibrium%20welfare%20outcomes.pdf)\n',encoding='utf-8')
    update('README.md','Seven figures and five tables','Eight figures and four tables')
    update('README.md','Figure 7 replaces Table 4 in Welfare Analysis;', 'Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria;')
    update('Supplemental materials/Multiple equilibria/README.md',
           '[multiple-outcomes.svg](multiple-outcomes.svg) plots every accepted outcome; Table 6 reports disposition ranges.',
           '[Figure 8](../../Figures/Figure%208%20-%20Multiple%20equilibrium%20welfare%20outcomes.pdf) plots all five welfare measures for every accepted profile. [Disposition ranges](Sources/disposition-ranges.json) remain available numerically. Each row is a start index, not a matched equilibrium pair or ranking; repeated outcomes are retained.')
    plan='Results/Run records/Revised article and exhibit plan.md'
    update(plan,'The user approved one change of exhibit type: Figure 7 replaces Table 4 within Welfare Analysis. The set is now seven figures and five tables. Figures 1-6 and Tables 1-3, 5-6 retain their existing file identifiers and roles; no unrelated renumbering or article reorganization is introduced. The prepared collection is an isolated overlay, subject to the existing final release gates.',
           'The user approved two changes of exhibit type: Figure 7 replaces Table 4 within Welfare Analysis, and Figure 8 replaces Table 6 within Multiple Equilibria. The set is now eight figures and four tables. Figures 1-6 and Tables 1-3, 5 retain their existing identifiers and roles; no unrelated renumbering or reorganization is introduced. This is the reviewed working collection; final release gates still apply.')
    update(plan,'| **Table 6 - Disposition ranges** | Robustness / Multiple Equilibria | Retain the range table and location, updated from the 200-start/199-accepted-profile study. Discuss monetary ranges here too, with the requested full outcome plot available in the existing multiple-equilibria materials. |',
           '| **Figure 8 - Multiple equilibrium welfare outcomes** | Robustness / Multiple Equilibria | Show all 199 accepted profiles across five welfare measures in risk-neutral and risk-averse panels. Use the established American circles and British small open diamonds, shared scales and bottom legend. Retain disposition ranges in the supplement. |')
    update(plan,'alongside the updated Table 6.','as Figure 8 in place of Table 6.')
    rel='Article and bibliography/corr_signals.tex';tex=(ARTICLE/rel).read_text(encoding='utf-8')
    start=tex.index('\\begin{table}[H]',tex.index('\\subsection{Multiple Equilibria}'))
    end=tex.index('\\section{Conclusion}',start)
    tex=tex[:start]+r'''\begin{figure}[H]
\centering
\includegraphics[width=\linewidth,height=0.80\textheight,keepaspectratio]{../Figures/Figure 8 - Multiple equilibrium welfare outcomes.pdf}
\caption{Multiple equilibrium welfare outcomes}
\label{fig:multiple-equilibria}
\end{figure}

\clearpage
'''+tex[end:]
    tex=tex.replace(r'As shown in Table \ref{tab:multiple-equilibria}',r'As shown in Figure \ref{fig:multiple-equilibria}')
    tex=tex.replace('The current risk-neutral searches show outcome variation. These are accepted approximate profiles,',
                    'Figure 8 now shows welfare outcomes rather than disposition ranges. The current risk-neutral searches show outcome variation. These are accepted approximate profiles,')
    assert tex.count('\\revisionnote{')==27 and OLD not in tex and 'tab:multiple-equilibria' not in tex
    write(rel,tex)
    update('Article and bibliography/Revision notes.md','Figure 7 replaces Table 4 without moving the Welfare Analysis section.',
           'Figure 7 replaces Table 4 without moving Welfare Analysis. Figure 8 replaces Table 6 within Multiple Equilibria; its five welfare measures show every accepted start, while the disposition ranges remain in the supplement.')
    m=read(ARTICLE/'manuscript-exhibits.json');m['CreatedUtc']=utc()
    m['Exhibits']=[e for e in m['Exhibits'] if e['Exhibit']!=OLD]
    e=dict(Exhibit=TITLE,Output=f'Figures/{TITLE}.pdf',Sha256=artifact['PDF']['Sha256'],Caption=f'Figures/Sources/{TITLE}.txt',Data=f'Figures/Sources/{TITLE}.json')
    m['Exhibits'].insert(7,e);m['Figure8ReplacesTable6']=True;m['SourceManifest']='Results/Run records/figure8-exhibits-manifest.json'
    write('manuscript-exhibits.json',json.dumps(m,indent=2)+'\n')
    write(m['SourceManifest'],json.dumps(dict(CreatedUtc=utc(),Exhibits=m['Exhibits'],NumberedFigures=8,NumberedTables=4,Previous=identity(ARTICLE/'Results/Run records/numbered-exhibits-manifest.json'),Figure8Source=identity(FIG/'manifest.json'),CompleteArticlePublication=False),indent=2)+'\n')
    write('Supplemental materials/Multiple equilibria/Sources/manifest.json',json.dumps(dict(CreatedUtc=utc(),Accepted=199,Expected=200,CurrentFigure='../../../Figures/'+TITLE+'.pdf',FullPrecisionOutcomes=identity(ARTICLE/'Supplemental materials/Multiple equilibria/Sources/all-outcomes.csv'),DispositionRanges=identity(DELTA/'Supplemental materials/Multiple equilibria/Sources/disposition-ranges.json'),Figure8=identity(FIG/'manifest.json'),Previous=identity(ARTICLE/'Supplemental materials/Multiple equilibria/Sources/manifest.json')),indent=2)+'\n')
    for name in ('multiple_welfare_figure.py','numbered_article_exhibits.py','package_numbered_review_pdf.py','replace_table6_with_figure8.py'):
        put(ROOT/'scripts'/name,'Results/Run records/Sources/'+name)
    for folder in ('Figures','Tables'):put(ROOT/'scripts/numbered_article_exhibits.py',folder+'/Sources/numbered_article_exhibits.py')
    cwd=WORK/'Article and bibliography';cwd.mkdir()
    for name in ('corr_signals.bib','corr_signals.bbl'):
        p=ARTICLE/'Article and bibliography'/name
        if p.exists():shutil.copy2(p,cwd/name)
    shutil.copy2(DELTA/rel,cwd/'corr_signals.tex')
    for folder in ('Figures','Tables'):
        (WORK/folder).mkdir()
        for p in (ARTICLE/folder).glob('*.pdf'):
            if not p.name.startswith(OLD):shutil.copy2(p,WORK/folder/p.name)
    shutil.copy2(FIG/'Figures'/(TITLE+'.pdf'),WORK/'Figures'/(TITLE+'.pdf'))
    before={p.relative_to(DELTA).as_posix():(sha(ARTICLE/p.relative_to(DELTA)) if (ARTICLE/p.relative_to(DELTA)).exists() else None) for p in DELTA.rglob('*') if p.is_file()}
    before['Article and bibliography/corr_signals.pdf']=sha(ARTICLE/'Article and bibliography/corr_signals.pdf')
    before.update({n:sha(ARTICLE/n) for n in removed})
    save_new(WORK/'plan.json',dict(CreatedUtc=utc(),Before=before,Removed=removed,Protected=protected(),ArticleHead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ARTICLE,text=True).strip()))
    print('Prepared Figure 8 and isolated manuscript; repository unchanged.')

def build():
    cwd=WORK/'Article and bibliography';commands=[]
    for i,cmd in enumerate([['lualatex','-interaction=nonstopmode','-halt-on-error','corr_signals.tex'],['bibtex','corr_signals'],['lualatex','-interaction=nonstopmode','-halt-on-error','corr_signals.tex'],['lualatex','-interaction=nonstopmode','-halt-on-error','corr_signals.tex']]):
        with (WORK/f'build-{i+1}.log').open('wb') as f:r=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        commands.append(dict(Command=cmd,WorkingDirectory=str(cwd),ExitCode=r.returncode,Log=identity(WORK/f'build-{i+1}.log')))
        assert r.returncode==0
    import pdfplumber
    pdf=cwd/'corr_signals.pdf'
    with pdfplumber.open(pdf) as doc:
        text='\n'.join(p.extract_text() or '' for p in doc.pages)
        assert len(re.findall(r'\[Update\s*needed:',text))==27
        assert 'Figure 8:' in text and 'Table 6:' not in text and 'Table 4:' not in text and '??' not in text
        count=len(doc.pages)
    (WORK/'review-pages').mkdir()
    cmd=['pdftoppm','-r','85','-png',str(pdf),str(WORK/'review-pages/page')]
    subprocess.run(cmd,check=True,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    old=ROOT/'work/manuscript-marked-20260925-v3/review-pages'
    old_hashes={sha(p):identity(p) for p in old.glob('*.png')}
    comparisons=[dict(Current=identity(p),PreviouslyReviewed=old_hashes.get(sha(p))) for p in sorted((WORK/'review-pages').glob('*.png'))]
    save_new(WORK/'build-validation.json',dict(Passed=True,CreatedUtc=utc(),PDF=identity(pdf),Source=identity(cwd/'corr_signals.tex'),Commands=commands,RenderCommand=cmd,PageCount=count,EditorialFlags=27,PageComparisons=comparisons))
    print(json.dumps(dict(Pages=count,NewPages=[c['Current']['Path'] for c in comparisons if not c['PreviouslyReviewed']]),indent=2))

def apply():
    plan=read(WORK/'plan.json');qa=read(WORK/'visual-review.json');assert qa['Passed']
    assert protected()==plan['Protected']
    assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ARTICLE,text=True).strip()==''
    for n,h in plan['Before'].items():assert (sha(ARTICLE/n) if (ARTICLE/n).exists() else None)==h,n
    for item in qa['ReviewedArtifacts']:assert sha(item['Path'])==item['Sha256']
    put(WORK/'Article and bibliography/corr_signals.pdf','Article and bibliography/corr_signals.pdf')
    for name in ('build-validation.json','visual-review.json','plan.json'):
        put(WORK/name,'Results/Run records/figure8-'+name)
    ARCHIVE.mkdir(exist_ok=False)
    archives=[]
    for n,h in plan['Before'].items():
        if h:
            target=ARCHIVE/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ARTICLE/n,target);assert sha(target)==h
            archives.append(identity(target))
    save_new(ARCHIVE/'manifest.json',dict(CreatedUtc=utc(),Files=archives))
    replacements=[]
    for p in DELTA.rglob('*'):
        if p.is_file():
            rel=p.relative_to(DELTA);target=(ARTICLE/rel).resolve();assert target.is_relative_to(ARTICLE.resolve())
            if rel.as_posix() not in plan['Before']:assert not target.exists(),rel
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);assert sha(p)==sha(target)
            replacements.append(rel.as_posix())
    for n in plan['Removed']:
        target=(ARTICLE/n).resolve();assert target.is_relative_to(ARTICLE.resolve()) and sha(target)==sha(ARCHIVE/n);target.unlink()
    assert protected()==plan['Protected']
    m=read(ARTICLE/'manuscript-exhibits.json')
    for e in m['Exhibits']:
        assert sha(ARTICLE/e['Output'])==e['Sha256']
        for k in ('Data','Caption'):assert (ARTICLE/e[k]).is_file()
    changed=sorted(set(replacements+plan['Removed']))
    subprocess.run(['git','add','--',*changed],cwd=ARTICLE,check=True)
    actual=subprocess.check_output(['git','diff','--cached','--no-renames','--name-only','-z'],cwd=ARTICLE).decode().strip('\0').split('\0')
    expected=[n for n in changed if n in actual];assert sorted(actual)==sorted(expected)
    subprocess.run(['git','commit','-m','Replace disposition range table with full multiple-equilibrium welfare figure'],cwd=ARTICLE,check=True)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ARTICLE,text=True).strip()
    save_new(WORK/'completion.json',dict(Passed=True,CreatedUtc=utc(),ArticleCommit=head,Archived=identity(ARCHIVE/'manifest.json'),Changed=actual,ProtectedHashes=plan['Protected'],Figure=identity(ARTICLE/f'Figures/{TITLE}.pdf'),Manuscript=identity(ARTICLE/'Article and bibliography/corr_signals.pdf'),SolvesStarted=0,CompleteArticlePublication=False))
    shutil.copy2(WORK/'Article and bibliography/corr_signals.pdf',TASK/'outputs/Article-with-Figure8-20260925.pdf')
    shutil.copy2(WORK/'completion.json',TASK/'outputs/Figure8-repository-update-20260925.json')
    print('Article update committed: '+head)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=('prepare','build','apply'));a=p.parse_args();globals()[a.mode]()
