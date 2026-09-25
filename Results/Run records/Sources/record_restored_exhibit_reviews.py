"""Bind the pages actually opened in this task to the final restored collection."""
import pathlib
from article_release import ROOT, read, identity, verify, save_new, utc

OUT=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to\outputs')
final=OUT/'Article-exhibits-restored-20260925-v4';prior=OUT/'Article-exhibits-restored-20260925-v3'
m=read(final/'manifest.json');old={x['Title']:x for x in read(prior/'manifest.json')['Artifacts']}
assert read(final/'data-preservation-validation.json')['Passed']
final_pages={('Table 2 - Strategy mechanisms',1),*[('Table 3 - Risk-averse strategy changes',n) for n in (1,2,3)],
             ('Table 5 - Overall results summary',2),('Table 5 - Overall results summary',3)}
proof=[]
for art in m['Artifacts']:
    for n,p in enumerate(art['Pages'],1):
        seen=p if (art['Title'],n) in final_pages else old[art['Title']]['Pages'][n-1]
        verify(p);verify(seen);assert p['Sha256']==seen['Sha256']
        proof.append(dict(FinalPage=p,ActuallyOpenedPage=seen,PixelFileSha256Identical=True))
assert len(proof)==17
save_new(final/'visual-review.json',dict(Schema='page-by-page-visual-qa-v1',Passed=True,ReviewedUtc=utc(),
    InspectionMethod='All 17 version-3 pages were opened with view_image. The six changed version-4 table pages were opened after the final typography/pending-label correction. All other final pages are pixel-file identical to those inspected version-3 pages.',
    Manifest=identity(final/'manifest.json'),DataPreservation=identity(final/'data-preservation-validation.json'),
    Artifacts=[dict(PDF=a['PDF'],Pages=a['Pages']) for a in m['Artifacts']],PageInspectionProof=proof,
    Checks=['Latin Modern restored; table names and captions outside the rendered tables.',
        'Full worked equilibrium path includes agreement, offers, settlement and trial; information-set links verified.',
        'Directional black/white fills and prior patterns restored.',
        'Rule markers overlay; exactly unreached policies omitted; all reached offer support retained.',
        'No clipping, overlapping labels, heatmaps, flags or remainder columns in main exhibits.',
        'Figure 7 has two risk panels, five cost rows, five outcome columns and all 20 main profiles.',
        'Trial-only rows follow earlier/later costs; calibrated direct binary joins merits at the end.'],
    PriorAttemptNotes=['v1: rejected table cropping, axis-label/tick spacing; v2: missing TikZ package after table preamble change; v3: revised narrow strategy headers and repeated Pending labels. All attempts retained.'],
    CompleteArticle=False))
print('All 17 final exhibit pages bound to actual visual inspection.')
