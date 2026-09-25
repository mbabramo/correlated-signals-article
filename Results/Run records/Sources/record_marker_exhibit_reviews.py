"""Record the six revised pages actually viewed, with inherited unchanged-page QA."""
import pathlib, shutil
from article_release import read, identity, verify, save_new, utc

OUT=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to\outputs')
final=OUT/'Article-exhibits-markers-20260925-v3'
prior=OUT/'Article-exhibits-restored-20260925-v4'
m=read(final/'manifest.json');old={a['Title']:a for a in read(prior/'manifest.json')['Artifacts']}
assert read(prior/'visual-review.json')['Passed'] and read(final/'data-preservation-validation.json')['Passed']
changed=set(m['RevisedFigures']);proof=[];newpages=0
for art in m['Artifacts']:
    for n,page in enumerate(art['Pages'],1):
        verify(page)
        if art['Title'] in changed:
            proof.append(dict(FinalPage=page,ActuallyOpenedPage=page,Inspection='Opened with view_image in this turn'))
            newpages+=1
        else:
            seen=old[art['Title']]['Pages'][n-1];verify(seen)
            assert page['Sha256']==seen['Sha256']
            assert art['PDF']['Sha256']==old[art['Title']]['PDF']['Sha256']
            proof.append(dict(FinalPage=page,PreviouslyReviewedPage=seen,PixelFileSha256Identical=True))
assert newpages==6 and len(proof)==17
# Keep editable table sources consistent with the generator snapshot used for these figures.
shutil.copy2(final/'Figures/Sources/numbered_article_exhibits.py',final/'Tables/Sources/numbered_article_exhibits.py')
save_new(final/'visual-review.json',dict(Schema='page-by-page-visual-qa-v1',Passed=True,ReviewedUtc=utc(),
    InspectionMethod='Figures 4, 6 and 7 and all three Table 5 pages were opened with view_image. The other 11 pages and their PDFs are byte-identical to the previous explicitly reviewed collection.',
    Manifest=identity(final/'manifest.json'),PriorVisualReview=identity(prior/'visual-review.json'),
    DataPreservation=identity(final/'data-preservation-validation.json'),
    Artifacts=[dict(PDF=a['PDF'],Pages=a['Pages']) for a in m['Artifacts']],PageInspectionProof=proof,
    Checks=['Participation legends at the bottom, with the mixed offer strategy area note adjacent.',
        'Circle and diamond enclosed areas share one probability scale, including the outer black diamond outline; white background halo excluded.',
        'Welfare diamonds small; welfare legend at the bottom; monetary-unit note removed.',
        'Table 5 headers say British minus American; trial-only row omits cost 1; bottom unit note removed.',
        'No clipping, overlap or typography changes beyond requested layout and labels; scientific data unchanged.'],
    CompleteArticle=False))
(final/'README.md').write_text('# Updated legends, marker areas and labels\n\nFigures 4 and 6 have bottom legends and an adjacent mixed-offer-strategy area note. Equal probabilities have equal enclosed areas across circles and diamonds, including the outer black diamond outline and excluding the white background halo. Both formulas and rendered PDF coordinates were checked. Figure 7 uses small diamonds, a bottom legend and no monetary-unit note. Table 5 says British minus American, omits cost 1 from the trial-only row, and omits its bottom unit note. All scientific data and other exhibits are unchanged. All 17 pages have current or inherited visual-review bindings.\n',encoding='utf-8')
print('Six revised pages inspected; all 17 pages covered by verified visual-review bindings.')
