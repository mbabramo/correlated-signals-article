"""Bind explicit page inspections performed during preparation of the selected supplement.

This records completed human-visible inspections; it does not perform them.
"""
from article_release import ROOT, read, verify, identity, save_new, utc

COLLECTION=ROOT/'reporting/inherited-strategic-british-v2/result.json'
prior=read(ROOT/'validation/inherited-strategic-visual-coverage-v2.json')
old={x['PairId']:x for x in prior['Validated']}
viewed=set('07aae708ecb98666 0fc7a2a287270bd8 1c7425246eab07dc 2ea93bae2da524db 47be08911a585e26 53c9a8e36428a91f 56ff6016b4c6159e 9e472d80c2ef001d a02ec8fdac528f16 bee428ba07d61647 c2314e34aca69429 c53a0fdc79f5919d d2e4b12e09de085a e1711b2f1451a02d e7eea98ccda5ead3 f25d77bce0833f42'.split())
viewed={'pair-'+x for x in viewed}
overrides={
 'pair-bee428ba07d61647':ROOT/'reporting/inherited-selected-layout-bee-v3/render-validation.json',
 'pair-f25d77bce0833f42':ROOT/'reporting/inherited-selected-layout-f25-v1/render-validation.json'}
items=[];proof=[]
for f in read(COLLECTION)['Validated']:
    original=read(verify(f)); pid=original['PairId']
    if pid not in old and pid not in viewed:continue
    final=read(overrides[pid]) if pid in overrides else original
    if pid in overrides:
        assert len(final['Artifacts'][0]['Pages'])==2
        # The changed payoff page was opened again; first pages are identical.
        assert final['Artifacts'][0]['Pages'][0]['Sha256']==original['Artifacts'][0]['Pages'][0]['Sha256']
        proof.append(dict(PairId=pid,Original=f,Revised=identity(overrides[pid]),
                          FirstPagePreviouslyViewedAndIdentical=True,RevisedPayoffPageActuallyViewed=True))
    for a in final['Artifacts']:
        for i in [a['PDF'],a['TeX']]+a['Pages']:verify(i)
    items.append(dict(PairId=pid,SourceManifest=identity(overrides[pid]) if pid in overrides else f,
        Artifacts=final['Artifacts'],PriorReview=old.get(pid)))
assert len(items)==25 and sum(len(i['Artifacts']) for i in items)==50
save_new(ROOT/'validation/article-selected-inherited-strategic-v1.json',dict(
    Schema='page-by-page-visual-qa-v1',Passed=True,ReviewedUtc=utc(),
    InspectionMethod='Every page of the 16 newly selected pairs was opened with view_image. Two notes-only overflow pages were repaired with typography-only derivatives and their changed payoff pages inspected again. First pages match the inspected originals byte-for-byte. The other nine pairs retain their existing full-page review bindings.',
    Collection=identity(COLLECTION),SelectedPairs=items,TypographyProof=proof,
    Artifacts=[dict(PDF=a['PDF'],Pages=a['Pages']) for i in items for a in i['Artifacts']],
    PriorCoverage=identity(ROOT/'validation/inherited-strategic-visual-coverage-v2.json'),
    Checks=['50 directed reports: all included pages legible, no clipping or overlapping rows.',
            'Both directions, payoff tables, agreement contributions, sensitivity and remaining terms retained.',
            '20 non-cost-1 trial-only pairs excluded editorially; their source records preserved.'],CompleteArticle=False))
p=ROOT/'reporting/article-selected-welfare-decompositions-v2/result.json';m=read(p)
assert m['Passed'] and len(m['Pages'])==6
for f in [m['PDF']]+m['Pages']:verify(f)
save_new(ROOT/'validation/article-selected-welfare-decompositions-v2.json',dict(
    Schema='page-by-page-visual-qa-v1',Passed=True,ReviewedUtc=utc(),
    InspectionMethod='All six complete page PNGs opened with view_image and inspected in this task.',
    Collection=identity(p),PDF=m['PDF'],Pages=m['Pages'],
    Checks=['34 comparisons and all five measures readable; formulas, signs, residuals and key retained.',
            'No split last rows; two pending comparisons and absent alternative truth maps declared.'],CompleteArticle=False))
print('Recorded reviews for 50 selected inherited directions and all six welfare decomposition pages.')
