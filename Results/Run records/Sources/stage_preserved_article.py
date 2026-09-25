"""Create a fresh, curated repository-shaped overlay; never modify the article repo.

All copies are hash-checked. Large scientific JSON is losslessly compressed with
round-trip hashes. Missing results remain explicit. This is not a release approval.
"""
import argparse, csv, gzip, hashlib, json, pathlib, shutil, subprocess, sys, zipfile
from urllib.parse import quote
from article_release import ROOT, ARTICLE, identity, read, save_new, sha, utc, verify

TASK=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to')
OUTPUTS=TASK/'outputs'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--name',required=True)
p.add_argument('--exhibits',type=pathlib.Path,required=True)
a=p.parse_args()
stage=(ROOT/'article-staging'/a.name).resolve()
delivery=(OUTPUTS/a.name).resolve()
assert stage.parent==ROOT/'article-staging' and delivery.parent==OUTPUTS
stage.mkdir(parents=True,exist_ok=False);delivery.mkdir(parents=True,exist_ok=False)
copied=[];generated=[];reviews=[];indexes={}

def put(item,rel,compress=False):
    source=verify(item) if isinstance(item,dict) else pathlib.Path(item)
    original=identity(source);dest=stage/rel
    assert dest.resolve().is_relative_to(stage)
    if compress:dest=dest.with_suffix(dest.suffix+'.gz')
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():
        existing=next(x for x in copied if x['RelativePath']==dest.relative_to(stage).as_posix())
        assert existing['Original']['Sha256']==original['Sha256'];return dest
    if compress:
        with source.open('rb') as src,dest.open('wb') as out:
            with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=6) as gz:
                shutil.copyfileobj(src,gz)
        with gzip.open(dest,'rb') as src:
            digest=hashlib.file_digest(src,'sha256').hexdigest()
        assert digest==original['Sha256']
    else:
        shutil.copy2(source,dest);assert sha(dest)==original['Sha256']
    copied.append(dict(RelativePath=dest.relative_to(stage).as_posix(),Original=original,
                       Staged=identity(dest),LosslessGzip=compress,RoundTripSha256=original['Sha256']))
    return dest

def write(rel,text):
    dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    assert not dest.exists();dest.write_text(text,encoding='utf-8')
    generated.append(dict(RelativePath=dest.relative_to(stage).as_posix(),Identity=identity(dest)))

def jwrite(rel,data):write(rel,json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def review(item):
    f=verify(item) if isinstance(item,dict) else pathlib.Path(item)
    data=read(f);assert data.get('Passed') is True
    ident=identity(f)
    if not any(x['Sha256']==ident['Sha256'] for x in reviews):
        reviews.append(ident)
        put(ident,'Results/Run records/Visual review/'+ident['Sha256'][:12]+'-'+f.name)

def link(text,path,folder):
    return '['+text+']('+quote(path.relative_to(stage/folder).as_posix())+')'

# The numbered exhibits retain both their existing roles and source files.
main=a.exhibits.resolve();m=read(main/'manifest.json')
review(main/'visual-review.json')
for folder in ('Figures','Tables'):
    for f in sorted((main/folder).rglob('*')):
        if f.is_file():put(f,f.relative_to(main))
    rows=[link(x['Title'],stage/folder/pathlib.Path(x['PDF']['Path']).name,folder) for x in m['Artifacts'] if x['Folder']==folder]
    write(folder+'/README.md','# '+folder+'\n\nExisting roles and article order are preserved. Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria. Other file identifiers are unchanged. Editable sources, complete numerical data and separate captions are in Sources.\n\n'+'\n'.join('- '+x for x in rows)+'\n')
put(main/'manifest.json','Results/Run records/numbered-exhibits-manifest.json')
put(main/'data-preservation-validation.json','Results/Run records/exhibit-data-preservation.json')

# Full profiles: editorial selection only, with no probability filtering.
catalogpath=ROOT/'reporting/audited-primary-catalog-v13/catalog.json';catalog=read(catalogpath)
def selected(c):return c['Parameters']['FeeRule']!='trial-only' or c['Parameters']['CostMultiplier']==1
cases={x['CaseId']:x for x in catalog['Cases'] if selected(x)}
excluded=[x['CaseId'] for x in catalog['Cases'] if not selected(x)]
assert len(cases)==72 and len(excluded)==8
strategy=read(ROOT/'reporting/primary-strategy-collection-v11/result.json')
inventory=read(ROOT/'reporting/exhibit-inventory-v12/inventory.json')
iv={x['PDF']['Sha256']:x for x in inventory['Exhibits']}
rows=[]
for art in strategy['Artifacts']:
    cid=art['CaseId']
    if cid not in cases:continue
    qa=iv[art['PDF']['Sha256']];assert qa['VisuallyReviewed'];review(qa['VisualQA'])
    folder='Results/Individual simulations/'+cid
    pdf=put(art['PDF'],folder+'/strategy.pdf')
    sm=read(verify(art['SourceManifest']))
    for f in sm['Files']:
        source=verify(f);put(f,folder+'/Sources/'+source.name)
    assert sm['CompleteProfile']['Sha256']==cases[cid]['CompleteProfile']['Sha256']
    put(art['SourceManifest'],folder+'/Sources/source-manifest.json')
    rows.append('- '+link(cid,pdf,'Results/Individual simulations'))
assert len(rows)==72
write('Results/Individual simulations/README.md','# Individual simulations\n\n72 of 74 profiles selected for the revised article are available and fully audited. Each report includes entry, exit commitments, agreement decisions and complete mixed offer policies, including off-path actions.\n\nThe two pending profiles are British, risk averse, cost 1, with 8 signals/15 offers and 12 signals/8 offers. No placeholder equilibrium is substituted.\n\nTrial-only fee shifting is included only at cost 1. The other eight historical trial-only profiles remain in the preserved computational archive.\n\n'+'\n'.join(rows)+'\n')
jwrite('Results/Aggregated Data/selected-primary-catalog.json',dict(
    Schema='editorially-selected-primary-catalog-v1',Source=identity(catalogpath),Cases=list(cases.values()),
    ExpectedSelected=74,AvailableSelected=72,Missing=catalog['MissingAuditedCaseIds'],
    ArchivedOutsideReaderCollection=excluded,ProbabilityFilteringApplied=False))
fields=['CaseId','Family','Variant','FeeRule','AlphaP','AlphaD','CostMultiplier','Signals','Offers']
fields+=list(next(iter(cases.values()))['ParticipationAndDispositions'])
fields+=list(next(iter(cases.values()))['Welfare']['Headline'])
csvpath=stage/'Results/Aggregated Data/selected-primary-outcomes.csv'
with csvpath.open('w',newline='',encoding='utf-8') as file:
    writer=csv.DictWriter(file,fieldnames=fields);writer.writeheader()
    for cid,c in cases.items():
        row={k:c['Parameters'].get(k) for k in fields[:9]};row['CaseId']=cid;row['Offers']=len(c['Parameters']['Offers'])
        row.update(c['ParticipationAndDispositions']);row.update(c['Welfare']['Headline']);writer.writerow(row)
generated.append(dict(RelativePath=csvpath.relative_to(stage).as_posix(),Identity=identity(csvpath)))

# Current welfare documents stay inside the existing pairwise-comparisons folder.
folder='Supplemental materials/Generated pairwise comparisons'
for name,manifest in [('welfare-overview','article-selected-welfare-overview-v1/manifest.json'),
                      ('welfare-decompositions','article-selected-welfare-decompositions-v2/result.json')]:
    fp=ROOT/'reporting'/manifest;doc=read(fp);put(doc['PDF'],folder+'/'+name+'.pdf')
    for f in doc['Sources']:put(f,folder+'/Sources/'+name+'/'+pathlib.Path(f['Path']).name)
    put(fp,folder+'/Sources/'+name+'/manifest.json')
review(ROOT/'validation/article-selected-welfare-overview-v1.json')
review(ROOT/'validation/article-selected-welfare-decompositions-v2.json')
write(folder+'/README.md','# Generated pairwise comparisons\n\n- [Welfare levels and signed comparisons](welfare-overview.pdf): 72 selected profiles and 34 completed American/British pairs.\n- [Rule and behavioral decompositions](welfare-decompositions.pdf): all five measures, four counterfactual corners, both replacement orders, signed components and accounting residuals.\n\nTwo risk-averse grid comparisons remain pending. Alternative truth-map strengths await specification and are not silently assumed. The decomposition evaluates fixed profiles under alternative rules; hybrid corners are not newly solved equilibria. Full precision data and sources are retained in Sources.\n')

# Strategic material: 46 new pairs + 25 selected inherited pairs.
newpath=ROOT/'reporting/new-strategic-british-v2/result.json'
new=[dict(SourceManifest=f) for f in read(newpath)['Validated']]
inhpath=ROOT/'validation/article-selected-inherited-strategic-v1.json'
inherited=read(inhpath)['SelectedPairs'];pairs=new+inherited
assert len(pairs)==71
review(ROOT/'validation/new-strategic-british-v2.json');review(inhpath)
folder='Supplemental materials/Equilibrium strategy changes';pairrows=[]
for x in pairs:
    f=x['SourceManifest'];doc=read(verify(f));pid=doc['PairId'];sub=folder+'/'+pid
    artlinks=[]
    for art in doc['Artifacts']:
        aid=art['Contrast']['Id'];pdf=put(art['PDF'],sub+'/'+aid+'.pdf')
        put(art['TeX'],sub+'/Sources/'+aid+'.tex')
        artlinks.append(link(art['Contrast']['Label'].replace('__complete__','__british__'),pdf,folder))
    put(f,sub+'/Sources/render-validation.json');put(doc['Request'],sub+'/Sources/request.json')
    for raw in doc['OriginalCalculationFilesUnchanged']:
        put(raw,sub+'/Sources/'+pathlib.Path(raw['Path']).name,compress=pathlib.Path(raw['Path']).suffix=='.json' and pathlib.Path(raw['Path']).stat().st_size>1000000)
    pairrows.append('- '+'; '.join(artlinks))
write(folder+'/README.md','# Equilibrium strategy changes\n\n142 directed reports (71 pairs) are ready, including both directions, probability contributions and relative-payoff changes. Eight additional directions depend on the two pending grid profiles. Main Tables 2 and 3 contain selected excerpts; the complete reports retain agreement, sensitivity and equilibrium-selection remainder terms.\n\nOnly cost-1 trial-only comparisons are included. Forty historical directions involving other trial-only costs remain archived outside this reader collection. Large raw JSON is losslessly compressed as .json.gz; decompress with Python gzip or a standard archive tool. The staging manifest verifies the decompressed SHA-256 against the original.\n\nThese are accounting decompositions of strategy changes, not an observed adjustment path.\n\n'+'\n'.join(pairrows)+'\n')

# Retain one black-and-white version of each signal panel.
inventory=read(ROOT/'reporting/exhibit-inventory-v12/inventory.json')
iv={x['PDF']['Sha256']:x for x in inventory['Exhibits']}
folder='Supplemental materials/Liability signals diagrams';sigrows=[]
for art in read(ROOT/'reporting/final-signal-collection-v2/result.json')['Artifacts']:
    if not art['Monochrome']:continue
    qa=iv[art['PDF']['Sha256']];assert qa['VisuallyReviewed'];review(qa['VisualQA'])
    sub=folder+'/'+art['CaseId'];pdf=put(art['PDF'],sub+'/'+art['FileStem']+'.pdf')
    for k in ('TeX','Data','Caption'):put(art[k],sub+'/Sources/'+pathlib.Path(art[k]['Path']).name)
    sigrows.append('- '+link(art['CaseId']+': '+art['FileStem'],pdf,folder))
assert len(sigrows)==39
write(folder+'/README.md','# Liability signals diagrams\n\n39 reviewed black-and-white panels cover the eight current signal models. Duplicate color versions are excluded. Sources include the numerical panels, TeX and captions. Figure 1 retains its distinct main-article role.\n\n'+'\n'.join(sigrows)+'\n')
folder='Supplemental materials/Game tree diagrams';treerows=[]
for art in read(ROOT/'reporting/final-structure-collection-v2/result.json')['SelectedArtifacts']:
    if not art['FileStem'].startswith('game tree'):continue
    qa=iv[art['PDF']['Sha256']];assert qa['VisuallyReviewed'];review(qa['VisualQA'])
    pdf=put(art['PDF'],folder+'/'+art['FileStem']+'.pdf')
    for k in ('TeX','Caption'):put(art[k],folder+'/Sources/'+pathlib.Path(art[k]['Path']).name)
    treerows.append('- '+link(art['FileStem'],pdf,folder))
assert len(treerows)==3
write(folder+'/README.md','# Game tree diagrams\n\nThese three illustrations explain the unchanged sequence of decisions, including agreement before offers. They are schematic small-tree illustrations, not smaller games used for equilibrium calculation. Figure 2 follows a current American equilibrium history through entry, commitments, agreement, offers and trial, with a neighboring settlement path.\n\n'+'\n'.join(treerows)+'\n')

# Approximate multiple-start evidence is distinct from exact primary profiles.
folder='Supplemental materials/Multiple equilibria';ap=ROOT/'reporting/approximate-stable-200-grouping-v1/catalog.json';approx=read(ap)
assert approx['RequestedStarts']==200 and approx['AcceptedStarts']==199
put(ap,folder+'/Sources/catalog.json')
put(ap.parent/'summary.csv',folder+'/Sources/grouping-summary.csv')
for item in approx['Attempts']:
    stem=item['Case']+'-start-'+str(item['StartIndex']).zfill(5)
    put(item['Result'],folder+'/Sources/Attempts/'+stem+'-result.json')
    if item['Accepted']:put(item['Profile'],folder+'/Sources/Profiles/'+stem+'.json')
diagram=OUTPUTS/'Multiple-equilibrium-outcome-diagram-British'
put(diagram/'all-outcomes.csv',folder+'/Sources/all-outcomes.csv')
put(main/'Supplemental materials/Multiple equilibria/Sources/disposition-ranges.json',folder+'/Sources/disposition-ranges.json')
put(ROOT/'scripts/approximate_catalog.py',folder+'/Sources/approximate_catalog.py')
write(folder+'/README.md','# Multiple equilibria\n\nThe cost-1 floating-point search completed 200 starts across American/British and risk-neutral/risk-averse cases. 199 passed the approved acceptance criteria; British risk-averse start 12 did not. These are accepted profiles, not 199 distinct exact equilibria.\n\n[Figure 8](../../Figures/Figure%208%20-%20Multiple%20equilibrium%20welfare%20outcomes.pdf) plots every accepted welfare outcome; [disposition ranges](Sources/disposition-ranges.json) remain in Sources. Grouping by complete strategies, reached strategies and outcomes is retained separately in Sources/catalog.json. Tolerance-based groups are descriptive, not proof of mathematical identity, nor estimates of equilibrium likelihood.\n\nAll full profiles, audit results, failed-attempt accounting, full-precision outcomes and grouping thresholds are retained. Exact primary profiles and approximate acceptance bands remain distinct.\n')

# No outdated trajectory is substituted for the running fourth replay.
folder='Supplemental materials/Equilibrium solution paths'
tracepath=ROOT/'reporting/trajectory-viewers-v1/result.json';trace=read(tracepath)
for f in trace['Files']:
    src=verify(f)
    if src.suffix=='.html' and src.name not in ('index.html','all-equilibrium-solution-paths.html'):
        put(f,folder+'/'+src.name)
put(tracepath,folder+'/Sources/trajectory-validation.json')
write(folder+'/README.md','# Equilibrium solution paths\n\nThree current exact replays have passed endpoint/trajectory checks: American risk neutral, British risk neutral, and American risk averse, all at cost 1. Their self-contained viewers are included for review. The British risk-averse replay is still running.\n\nInteractive browser QA is pending: the available browser tool rejected local files. These viewers are not marked publication-ready. No superseded trajectory or duplicate solve is substituted. The fourth viewer will be added only after replay verification.\n')

# Existing utility curves are copied unchanged, not regenerated or replaced.
utility=ARTICLE/'Supplemental materials/Risk aversion utility curves'
protected=[]
for f in sorted(utility.rglob('*')):
    if f.is_file():
        protected.append(identity(f));put(f,'Supplemental materials/Risk aversion utility curves/'+f.relative_to(utility).as_posix())

# Keep existing aggregate exhibits without obsolete trial-only cost series.
for name in ('American-British-cost-outcomes-20','Main-welfare-decomposition'):
    for f in sorted((OUTPUTS/name).iterdir()):
        if f.is_file() and (name!='American-British-cost-outcomes-20' or f.suffix=='.csv'):
            put(f,'Results/Aggregated Data/'+name+'/'+f.name)
write('Results/Aggregated Data/README.md','# Aggregated data\n\nThe primary catalog and outcomes contain 72 selected, audited profiles, including full precision welfare and participation measures. The main cost diagram covers all 20 American/British baseline profiles. Main-welfare-decomposition covers the ten baseline fee-rule comparisons. Trial-only fee shifting is restricted to cost 1.\n\nTwo pending risk-averse grid profiles are explicitly listed in the selected catalog. Approximate multiple-start results are in the existing Multiple equilibria supplement.\n')

planptr=ROOT/'provenance/current-editorial-plan-20260925-presentation.json'
put(read(planptr)['Plan'],'Results/Run records/Revised article and exhibit plan.md')
put(ROOT/'validation/remaining-profile-check-v29.json','Results/Run records/latest-grid-status.json')
for f in (catalogpath,planptr):
    put(f,'Results/Run records/'+f.name)
for name in ('numbered_article_exhibits.py','article_presentation.py','revise_marker_figures.py','record_marker_exhibit_reviews.py','update_presentation_plan.py','verify_restored_exhibits.py','record_restored_exhibit_reviews.py','stage_preserved_article.py','welfare_overview.py','welfare_decomposition_exhibits.py',
             'strategic_layout_fix.py','record_selected_supplement_reviews.py','record_article_exhibit_reviews.py',
             'render_strategic_terminology_v2.py','article_release.py','build_profile_catalog.py'):
    put(ROOT/'scripts'/name,'Results/Run records/Sources/'+name)
for f in sorted((ROOT/'provenance/commands').glob('*/execution.json')):
    if f.parent.name.startswith(('figure-marker-revision-v3','marker-exhibit-visual-review-v1','marker-review-copy-v1','restored-article-exhibits-','restored-worked-path-','agreed-presentation-plan-','article-selected-welfare-','new-strategic-terminology-v2','inherited-selected-layout-','selected-supplement-visual-review','bind-numbered-and-current')):
        put(f,'Results/Run records/Commands/'+f.parent.name+'/execution.json')
write('Results/Run records/README.md','# Run records\n\nReproducible render sources, executed commands, source identities, immutable QA evidence and the file-level staging manifest accompany the exhibits. Full build/source/input manifests and historical attempts remain in the isolated execution workspace identified by those records. No separate computational-methods section is introduced.\n\nThis overlay is prepared for review, not final publication. The repository, manuscript, bibliography, unrelated working-tree changes and protected utility-curve sources were not modified.\n')

pending=[
 'Two British risk-averse cost-1 exact profiles: 8 signals/15 offers and 12 signals/8 offers.',
 'Their two welfare comparisons and eight strategic directions, followed by updated Table 5 and supplemental summaries.',
 'Fourth verified trajectory and interactive visual QA of the viewers.',
 'User choice on truth-map sensitivity exponents (proposed 0.5 and 2, baseline 1), or explicit omission.',
 'Complete release evidence, then the authorized archive/replacement procedure.']
intro='# Article tables, figures and supplemental materials\n\nRevised 25 September 2026 in the existing repository structure. Eight figures and four tables cover the currently available results. Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria; Table 5 labels the two unfinished grid contrasts. The prior typography, directional patterns and shared American/British strategy axes are restored. Table names and captions are separate from the table files. No manuscript reorganization or figure consolidation is introduced.\n\n'
intro+='- [Figures](Figures/README.md)\n- [Tables](Tables/README.md)\n- [Individual simulations](Results/Individual%20simulations/README.md)\n- [Aggregated data](Results/Aggregated%20Data/README.md)\n'
for sub in ('Generated pairwise comparisons','Equilibrium strategy changes','Liability signals diagrams','Game tree diagrams','Multiple equilibria','Equilibrium solution paths','Risk aversion utility curves'):
    intro+='- ['+sub+'](Supplemental%20materials/'+quote(sub)+'/README.md)\n'
intro+='\nThe main material says American and British. Trial-only fee shifting is a cost-1 extension. Agreement decisions remain part of every primary game. Technical evidence stays with Sources and Run records.\n\nCuration excludes eight non-cost-1 trial-only profiles, 40 associated directed decomposition reports, duplicate color signal diagrams, superseded overviews and failed render caches. All underlying research records are preserved in the isolated workspace.\n\nStill pending before final publication:\n\n'+'\n'.join('- '+x for x in pending)+'\n'
write('README.md',intro)
record=dict(Schema='preserved-article-staging-v1',CreatedUtc=utc(),Generator=identity(__file__),Command=sys.argv,
    Stage=str(stage),ArticleRepository=str(ARTICLE),ArticleRepositoryModified=False,ReleaseApproved=False,
    MainFigures=m['NumberedFigures'],MainTables=m['NumberedTables'],SelectedPrimaryProfiles=72,ExpectedSelectedPrimaryProfiles=74,
    WelfareComparisons=34,ExpectedWelfareComparisons=36,DirectedStrategicReports=142,ExpectedSelectedDirections=150,
    SignalPanels=39,GameTreeIllustrations=3,ApproximateStarts=200,AcceptedApproximateProfiles=199,
    ExcludedHistoricalTrialOnlyCases=excluded,ExcludedHistoricalStrategicDirections=40,
    ExcludedDuplicateColorPanels=39,HistoricalRecordsDeleted=False,Pending=pending,
    ProtectedUtilityFiles=protected,VisualReviewBindings=reviews,CopiedFiles=copied,GeneratedFiles=generated)
jwrite('Results/Run records/staging-manifest.json',record)
# Verify each staged copy again before packaging.
for entry in copied:verify(entry['Staged'])
for f in protected:verify(f)
archive=delivery/'Article collection.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in sorted(stage.rglob('*')):
        if f.is_file():z.write(f,f.relative_to(stage).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
shutil.copy2(stage/'README.md',delivery/'README.md')
shutil.copytree(stage/'Figures',delivery/'Figures');shutil.copytree(stage/'Tables',delivery/'Tables')
save_new(delivery/'delivery-manifest.json',dict(Schema='prepared-article-delivery-v1',CreatedUtc=utc(),
    StageManifest=identity(stage/'Results/Run records/staging-manifest.json'),Archive=identity(archive),
    NumberedExhibits=identity(main/'manifest.json'),Pending=pending,Published=False))
print(json.dumps(dict(Stage=str(stage),Delivery=str(delivery),Files=len(copied)+len(generated),ZipBytes=archive.stat().st_size,Pending=pending),indent=2))
