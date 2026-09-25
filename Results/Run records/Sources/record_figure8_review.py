"""Bind the actual visual reviews and data equality to the current Figure 8 update."""
import ast, json, pathlib, re, shutil
from urllib.parse import unquote
from article_release import ROOT, ARTICLE, identity, read, sha, save_new, utc
from replace_table6_with_figure8 import WORK, DELTA, FIG, TASK, TITLE

# Update the future staging recipe without regenerating the historical collection.
p=ROOT/'scripts/stage_preserved_article.py';s=p.read_text(encoding='utf-8')
s=s.replace('Figure 7 replaces Table 4 in Welfare Analysis; other file identifiers are unchanged.',
            'Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria. Other file identifiers are unchanged.')
s=s.replace('[multiple-outcomes.svg](multiple-outcomes.svg) plots every accepted outcome; Table 6 reports disposition ranges.',
            '[Figure 8](../../Figures/Figure%208%20-%20Multiple%20equilibrium%20welfare%20outcomes.pdf) plots every accepted welfare outcome; [disposition ranges](Sources/disposition-ranges.json) remain in Sources.')
s=s.replace('Seven figures and five tables','Eight figures and four tables')
s=s.replace('Figure 7 replaces Table 4 in Welfare Analysis; Table 5 labels',
            'Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria; Table 5 labels')
p.write_text(s,encoding='utf-8');ast.parse(s)
plan=read(WORK/'plan.json')
for name in ('stage_preserved_article.py','record_figure8_review.py'):
    rel='Results/Run records/Sources/'+name
    assert rel not in plan['Before']
    plan['Before'][rel]=sha(ARTICLE/rel) if (ARTICLE/rel).exists() else None
    shutil.copy2(ROOT/'scripts'/name,DELTA/rel)
(WORK/'plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')

preview=FIG/'Figures'/(TITLE+'.png')
inspected=TASK/'outputs/Multiple-equilibrium-welfare-figure-20260925-v2/Figures'/(TITLE+'.png')
assert preview.read_bytes()==inspected.read_bytes()
manifest=read(FIG/'manifest.json');data=read(manifest['Data']['Path'])
assert data['ExactEqualityWithEarlierPlot'] and len(data['Rows'])==199 and len(data['PlottedPoints'])==995
build=read(WORK/'build-validation.json');assert build['Passed']
new=[x for x in build['PageComparisons'] if x['PreviouslyReviewed'] is None]
assert [pathlib.Path(x['Current']['Path']).name for x in new]==['page-28.png','page-29.png','page-30.png']
assert sha(WORK/'review-pages/page-28.png')==sha(ROOT/'work/manuscript-figure8-20260925-v1/review-pages/page-28.png')
links=[]
for p in DELTA.rglob('*.md'):
    for link in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if '://' in link or link.startswith('#'):continue
        rel=(p.parent/unquote(link.split('#')[0])).resolve().relative_to(DELTA.resolve())
        assert (DELTA/rel).exists() or (ARTICLE/rel).exists(),(p,link)
        links.append(dict(Source=p.relative_to(DELTA).as_posix(),Target=rel.as_posix()))
qa=dict(Passed=True,CreatedUtc=utc(),ReviewedArtifacts=[manifest['PDF'],manifest['Preview'],manifest['Data'],build['PDF'],build['Source']],
    FigureReview=dict(InspectedPreview=identity(inspected),IdenticalFinalPreview=identity(preview),Checks=['All five welfare columns and both risk panels legible','No overlapping headings or clipped points','American circles and small open British diamonds match established typography','Legend at bottom','All 995 points retained without grouping']),
    ManuscriptReview=dict(Pages=32,InheritedPixelIdenticalPages=29,ChangedPages=new,Checks=['Pages 28, 29 and 30 actually inspected','27 editorial flags retained','Conclusion starts on its own page','No undefined references or clipped content']),
    LinksChecked=links,ExactDataEquality=True,SolvesStarted=0)
save_new(WORK/'visual-review.json',qa);save_new(FIG/'visual-review.json',qa)
print('Visual review passed: 995 identical values, 32 manuscript pages, '+str(len(links))+' links.')
