"""Publish the visually reviewed, lightly corrected and explicitly marked manuscript."""
import json, os, pathlib, re, shutil, subprocess
from urllib.parse import unquote
from article_release import ROOT, ARTICLE, identity, read, sha, save_new, utc, contained, verify

work=ROOT/'work/manuscript-marked-20260925-v3'
update=ROOT/'reporting/working-article-update-20260925-v1'
archive=ROOT/'archive/working-article-update-20260925-v1'
out=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to\outputs')
def git(*a):return subprocess.check_output(['git',*a],cwd=ARTICLE)
base=read(update/'commit.json');assert git('rev-parse','HEAD').decode().strip()==base['Commit']
assert not git('diff','--cached','--name-only')
changes=read(work/'manuscript-change-log.json');build=read(work/'build-validation.json');assert build['Passed']
verify(changes['Original']);verify(changes['Revised']);verify(build['PDF'])
pages=sorted((work/'review-pages').glob('page-*.png'));sheets=sorted(work.glob('contact-*.png'))
assert len(pages)==32 and len(sheets)==8
save_new(work/'visual-review.json',dict(Schema='page-by-page-visual-qa-v1',Passed=True,ReviewedUtc=utc(),
    InspectionMethod='All 32 final pages were opened using view_image in eight four-page contact sheets at original resolution. Text, italic editorial markers, all 17 exhibit pages, captions and references were inspected.',
    PDF=identity(work/'Article and bibliography/corr_signals.pdf'),Pages=[identity(p) for p in pages],ContactSheets=[identity(p) for p in sheets],
    Checks=['27 bold italic Update needed labels are visible with the preserved outdated passages in italics.',
        'All pages of Tables 3, 5 and 6 are included; Figure 7 replaces Table 4 at its original section location.',
        'No clipping, overlap, undefined citations or unresolved cross-references. Original manual section breaks and basic typography preserved.',
        'The two missing Table 5 comparisons remain explicitly Pending.'],CompleteArticlePublication=False))

overlay=work/'publication';overlay.mkdir(exist_ok=False)
sources={
 'Article and bibliography/corr_signals.tex':work/'Article and bibliography/corr_signals.tex',
 'Article and bibliography/corr_signals.pdf':work/'Article and bibliography/corr_signals.pdf',
 'Results/Run records/manuscript-revision-20260925.json':work/'manuscript-change-log.json',
 'Results/Run records/manuscript-visual-review-20260925.json':work/'visual-review.json',
 'Results/Run records/manuscript-build-20260925.json':work/'build-validation.json',
}
def newtext(rel,text):
 p=contained(overlay,rel);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');sources[rel]=p
newtext('Article and bibliography/Revision notes.md',
 '# Manuscript revision marks\n\nThe author\'s narrative and organization are retained. Bold italic **[Update needed: ...]** labels explain why each marked passage needs attention; the retained passage is italicized. No replacement analysis has been drafted.\n\n'+
 'Basic corrections update tree sizes, approved grid and timing values, the American risk-averse settlement percentage, multiple-start coverage and ranges, and exhibit references. All pages of the updated multi-page tables are included. Figure 7 replaces Table 4 without moving the Welfare Analysis section.\n\n'+
 '## Passages requiring author revision\n\n'+'\n'.join(f'{i}. {f["Reason"]}' for i,f in enumerate(changes['EditorialFlags'],1))+
 '\n\nThe exact substitutions and evidence are recorded in [the change log](../Results/Run%20records/manuscript-revision-20260925.json). Two grid comparisons, the fourth trajectory/interactive QA, truth-map scope and full release evidence remain unresolved in the recorded collection.\n')
roottext=(ARTICLE/'README.md').read_text(encoding='utf-8')
roottext=roottext.replace('Complete release evidence, then the authorized archive/replacement procedure.','Complete final release evidence after the pending work; the reviewed available working collection has now been archived, synchronized and committed.')
roottext+='\nThe manuscript now contains limited factual corrections and explicit italicized **Update needed** passages. See [revision notes](Article%20and%20bibliography/Revision%20notes.md); the substantive narrative remains for the author to revise.\n'
newtext('README.md',roottext)
newtext('Results/Run records/README.md','# Run records\n\nReproducible sources, executed commands, source identities, numerical and visual QA, and the staging manifest accompany the current working collection. Full solver records remain in the isolated workspace identified by those records. No separate computational-methods section is introduced.\n\nThe user authorized this working-repository refresh and removal of superseded generated files on September 25, 2026. The entire prior generated collection and pre-existing manuscript/backup files were archived and hash-verified before replacement. working-collection-update.json identifies that archive and the complete file-level change plan. Utility curves, bibliography, unrelated build logs and backups were preserved.\n\nThe manuscript source and its compiled PDF now contain only documented factual/mechanical changes and explicit editorial flags; manuscript-revision-20260925.json records those changes, with separate build and visual-review evidence. This working update is not a completed final-publication certificate. Remaining comparisons, trajectory QA and other recorded release gates are still pending.\n')
rel='Supplemental materials/Equilibrium solution paths/README.md'
newtext(rel,(ARTICLE/rel).read_text(encoding='utf-8').replace('The British risk-averse replay is still running.','The British risk-averse replay is pending in the latest recorded status.'))
for name in ('update_article_working_collection.py','mark_article_manuscript.py','render_marked_article.py','finish_article_manuscript_revision.py'):
 sources['Results/Run records/Sources/'+name]=ROOT/'scripts'/name

# Preserve exact pre-application bytes, including the user's pre-existing compiled PDF.
before=archive/'manuscript-update-before';before.mkdir(exist_ok=False);actions=[]
for rel,src in sources.items():
 target=contained(ARTICLE,rel);old=identity(target) if target.exists() else None
 if old:
  dst=contained(before,rel);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,dst);assert sha(dst)==old['Sha256']
 actions.append(dict(RelativePath=rel,Original=old,New=identity(src)))
save_new(work/'publication-plan.json',dict(CreatedUtc=utc(),Actions=actions,VisualReview=identity(work/'visual-review.json'),PreviousCommit=base['Commit']))
for a in actions:
 target=contained(ARTICLE,a['RelativePath'])
 if a['Original']:verify(a['Original'])
 else:assert not target.exists()
 target.parent.mkdir(parents=True,exist_ok=True);temp=target.with_name(target.name+'.manuscript-update-tmp');assert not temp.exists()
 shutil.copy2(verify(a['New']),temp);os.replace(temp,target);assert sha(target)==a['New']['Sha256']

# Verify the complete synchronized scope, changing only the explicitly listed manuscript/navigation files.
allow=set(sources);plan=read(update/'plan.json')
for a in plan['Actions']:
 if a['RelativePath'] in allow:continue
 p=contained(ARTICLE,a['RelativePath'])
 if a['Action']=='Remove':assert not p.exists()
 else:assert sha(p)==(a['New'] or a['Old'])['Sha256']
links=[]
for p in ARTICLE.rglob('README.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
  if '://' in target:continue
  target=target.strip('<>');dest=(p.parent/unquote(target.split('#',1)[0])).resolve()
  assert dest.exists(),(str(p),str(dest));links.append(dict(Source=str(p.relative_to(ARTICLE)),Target=target))
for item in read(ARTICLE/'manuscript-exhibits.json')['Exhibits']:
 assert sha(ARTICLE/item['Output'])==item['Sha256']
 assert (ARTICLE/item['Data']).exists() and (ARTICLE/item['Caption']).exists()
tex=(ARTICLE/'Article and bibliography/corr_signals.tex').read_text(encoding='utf-8')
for rel in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',tex):assert (ARTICLE/'Article and bibliography'/rel).is_file()
assert not (ARTICLE/'Tables/Table 4 - Welfare outcomes.pdf').exists()
assert tex.count(r'\revisionnote{')==27
save_new(work/'repository-validation.json',dict(Passed=True,CreatedUtc=utc(),FilesRechecked=len(plan['Actions']),NavigationLinks=len(links),NumberedExhibits=12,EditorialFlags=27,ManuscriptPages=32,ProtectedFilesPreserved=True,FinalPublicationComplete=False))
paths=work/'commit-paths.bin';paths.write_bytes(b'\0'.join(p.encode() for p in sources)+b'\0')
subprocess.run(['git','add','--pathspec-from-file='+str(paths),'--pathspec-file-nul'],cwd=ARTICLE,check=True)
actual=set(git('diff','--cached','--no-renames','--name-only','-z').decode().strip('\0').split('\0'));assert actual==allow
subprocess.run(['git','commit','-q','-m','Correct manuscript facts and mark passages requiring author revision'],cwd=ARTICLE,check=True)
result=dict(CreatedUtc=utc(),CollectionCommit=base['Commit'],ManuscriptCommit=git('rev-parse','HEAD').decode().strip(),RepositoryValidation=identity(work/'repository-validation.json'),VisualReview=identity(work/'visual-review.json'),Source=identity(ARTICLE/'Article and bibliography/corr_signals.tex'),PDF=identity(ARTICLE/'Article and bibliography/corr_signals.pdf'),WorkingStatus=git('status','--porcelain=v1').decode(),Archive=str(archive),Pushed=False)
save_new(work/'completion.json',result)
for src,name in [(ARTICLE/'Article and bibliography/corr_signals.pdf','Article-with-revision-marks-20260925.pdf'),(ARTICLE/'Article and bibliography/Revision notes.md','Article-revision-notes-20260925.md'),(work/'completion.json','Article-repository-update-20260925.json')]:
 dest=out/name;assert not dest.exists();shutil.copy2(src,dest);assert sha(src)==sha(dest)
print(json.dumps(dict(CollectionCommit=result['CollectionCommit'],ManuscriptCommit=result['ManuscriptCommit'],FilesChecked=len(plan['Actions']),Links=len(links),Flags=27,Pages=32,RemainingWorkingStatus=result['WorkingStatus'])))
