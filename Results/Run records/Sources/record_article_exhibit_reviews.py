"""Bind this task's explicit inspections and pixel-identical reused page reviews."""
import pathlib
from article_release import ROOT,read,verify,identity,save_new,utc
TASK=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to')
base=TASK/'outputs'
current=base/'Article-exhibits-20260925-v4';m=read(current/'manifest.json')
actually_viewed={
 2:{'Figure 1 - Information structure':[1],'Figure 2 - Worked equilibrium path':[1],
    'Figure 3 - Dispositions':[1],'Figure 5 - Risk-averse dispositions':[1],
    'Table 1 - Model primitives':[1],'Table 2 - Strategy mechanisms':[1],
    'Table 3 - Risk-averse strategy changes':[1],'Table 4 - Welfare outcomes':[1],
    'Table 6 - Disposition ranges':[1]},
 3:{'Figure 4 - Participation and offers':[1],'Figure 6 - Risk-averse participation and offers':[1],
    'Table 3 - Risk-averse strategy changes':[2,3],'Table 5 - Overall results summary':[1,2],
    'Table 6 - Disposition ranges':[2]},
 4:{'Table 5 - Overall results summary':[3]}}
viewed={}
for version,docs in actually_viewed.items():
 for title,pages in docs.items():
  for page in pages:
   f=base/f'Article-exhibits-20260925-v{version}'/'review-pages'/title/f'page-{page}.png'
   viewed[title,page]=identity(f)
proof=[]
for a in m['Artifacts']:
 for n,page in enumerate(a['Pages'],1):
  seen=viewed[a['Title'],n];verify(page);assert page['Sha256']==seen['Sha256']
  proof.append(dict(FinalPage=page,ActuallyOpenedPage=seen,PixelFileSha256Identical=True))
save_new(current/'visual-review.json',dict(Schema='page-by-page-visual-qa-v1',Passed=True,ReviewedUtc=utc(),
  InspectionMethod='All 17 pages opened with view_image in this task; final pages match the actually inspected page hashes. Final Table 5 page 3 was inspected after its label edit.',
  Manifest=identity(current/'manifest.json'),Artifacts=[dict(PDF=a['PDF'],Pages=a['Pages']) for a in m['Artifacts']],
  Checks=['No clipped or overlapping labels; strategy footnote overlap corrected before final review.',
          'Complete mixed and off-path policies remain visible; agreement and offer histories are separate.',
          'Existing numbering and roles retained; two missing grid rows explicitly pending.'],PageInspectionProof=proof,CompleteArticle=False))
overview=ROOT/'reporting/article-selected-welfare-overview-v1/manifest.json';o=read(overview)
assert len(o['Pages'])==8
save_new(ROOT/'validation/article-selected-welfare-overview-v1.json',dict(Schema='page-by-page-visual-qa-v1',Passed=True,
  ReviewedUtc=utc(),InspectionMethod='All eight complete pages opened with view_image in this task.',Collection=identity(overview),
  PDF=o['PDF'],Pages=o['Pages'],Checks=['72 selected profile levels and 34 signed comparisons present.','All five measure plots legible; tables and notes within pages.'],CompleteArticle=False))
colpath=ROOT/'reporting/new-strategic-british-v2/result.json';col=read(colpath)
inventory=read(ROOT/'reporting/exhibit-inventory-v12/inventory.json')
oldreviews={x['PDF']['Sha256']:x['VisualQA'] for x in inventory['Exhibits'] if x['Kind']=='Strategic decompositions'}
pixelpath=ROOT/'validation/new-strategic-title-review-v1/proof.json';pixel=read(pixelpath)
assert pixel['Passed'] and len(pixel['Pages'])==119 and len(pixel['HeadingSheets'])==15
pixelbyhash={x['Updated']['Sha256']:x for x in pixel['Pages']}
artifacts=[];priorreviews=[]
for f in col['Validated']:
 new=read(verify(f));original=read(verify(new['OriginalRenderManifest'])) if pathlib.Path(f['Path']).is_relative_to(colpath.parent) else new
 for old,a in zip(original['Artifacts'],new['Artifacts']):
  q=oldreviews[old['PDF']['Sha256']];assert read(verify(q))['Passed'];priorreviews.append(q)
  for before,after in zip(old['Pages'],a['Pages']):
   verify(after)
   if before['Sha256']!=after['Sha256']:
    p=pixelbyhash[after['Sha256']];assert p['Original']==before and p['BodyBelowY120PixelIdentical']
  artifacts.append(dict(PDF=a['PDF'],Pages=a['Pages']))
save_new(ROOT/'validation/new-strategic-british-v2.json',dict(Schema='page-by-page-visual-qa-v1',Passed=True,
  ReviewedUtc=utc(),InspectionMethod='All changed title areas on 119 pages inspected in 15 full-resolution heading sheets with view_image. Every pixel below y=120 is identical to the earlier fully reviewed page; unchanged reports retain their explicit prior page reviews.',
  Collection=identity(colpath),Artifacts=artifacts,PriorFullPageReviews=priorreviews,PixelProof=identity(pixelpath),
  ActuallyViewedHeadingSheets=pixel['HeadingSheets'],Checks=['American/British headings legible and correctly directed.','Only declared label substitutions; all rendered numeric tokens and body pixels unchanged.'],CompleteArticle=False))
print('Bound 17 main pages, 8 welfare pages, and all 92 new-scope strategic reports to actual reviews.')
