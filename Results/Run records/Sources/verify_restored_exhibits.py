"""Exact data-preservation checks for the presentation-only revision."""
import argparse, csv, pathlib
from article_release import ROOT, read, identity, verify, save_new, utc

TASK=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to')
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);a=p.parse_args()
out=a.source.resolve();manifest=read(out/'manifest.json');old=TASK/'outputs/Article-exhibits-20260925-v4'
assert manifest['NumberedFigures']==7 and manifest['NumberedTables']==5
assert not any(x['Title'].startswith('Table 4') for x in manifest['Artifacts'])
def data(base,folder,title):return read(base/folder/'Sources'/(title+'.json'))
checks=[]
for idx,name in [(3,'Dispositions'),(5,'Risk-averse dispositions')]:
    title=f'Figure {idx} - {name}'
    assert data(out,'Figures',title)['Dispositions']==data(old,'Figures',title)['Dispositions']
    checks.append(title+': all seven unrounded disposition values unchanged')
for idx,name in [(4,'Participation and offers'),(6,'Risk-averse participation and offers')]:
    title=f'Figure {idx} - {name}';d=data(out,'Figures',title);before=data(old,'Figures',title)
    assert d['Profiles']==before['Profiles']
    assert d['ExactPositiveSupportVerified']
    for point in d['DisplayedPoints']:
        profile=d['Profiles'][0 if point['Rule']=='american' else 1]
        row=next(r for r in profile['Strategies'] if (r['Decision'],r['Signal'],r['OwnExit'])==(point['Decision'],point['Signal'],point['OwnExit']))
        assert point['Reach']==row['Reach']>0
        assert point['Probability']==row['Probabilities'][row['Actions'].index(point['Action'])]
    if idx==4:
        assert all(r['Probabilities'][r['Actions'].index('Yes')]==0 for profile in d['Profiles'] for r in profile['Strategies']
                   if r['Decision'] in ('PAbandon','DDefault') and r['Reach']>0)
    checks.append(title+': full profile identical, no zero-reach point, all reached positive offer support preserved')
for title in ('Table 1 - Model primitives','Table 2 - Strategy mechanisms','Table 3 - Risk-averse strategy changes','Table 6 - Disposition ranges'):
    assert data(out,'Tables',title)==data(old,'Tables',title)
    layout=read(out/'Tables'/'Sources'/(title+'.layout.json'));assert not layout['EmbeddedTitle']
    if title.startswith(('Table 2','Table 3')):assert 'Remain' not in layout['Headings'] and 'Flags' not in layout['Headings']
    checks.append(title+': all source data exactly unchanged')
title='Table 5 - Overall results summary';before=data(old,'Tables',title);after=data(out,'Tables',title)
key=lambda x:(x['American'],x.get('British',x.get('TrialOnly')))
assert sorted(before['Comparisons'],key=key)==sorted(after['Comparisons'],key=key)
layout=read(out/'Tables'/'Sources'/(title+'.layout.json'))
for subtitle,rows in layout['Sections'][:2]:
    labels=[r[0] for r in rows]
    assert labels.index('Trial-only fee shifting (cost 1)')==labels.index('Costs: later costs')+1
    assert labels[-3:]==['Merits: center weighted','Merits: polarized','Calibrated direct binary']
assert len(layout['Sections'][2][1])==2
assert sum(c['Status']=='pending' for c in after['Comparisons'])==2
checks.append('Table 5: exact comparison values unchanged; trial-only placed after cost timing; merits grouped last; two pending rows retained')
w=data(out,'Figures','Figure 7 - Welfare outcomes');assert w['MainProfiles']==20 and len(w['PlottedValues'])==100
csvpath=TASK/'outputs/American-British-cost-outcomes-20/selected-exact-outcomes.csv'
with csvpath.open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
byid={r['Case']:r for r in rows}
for value in w['PlottedValues']:assert value['Value']==float(byid[value['Case']][value['Measure']])
checks.append('Figure 7: all 100 plotted monetary values exactly equal to the previously requested latest-data plot')
worked=data(out,'Figures','Figure 2 - Worked equilibrium path');extraction=read(verify(worked['Extraction']))
assert worked['Paths']==extraction and worked['VerifiedInformationSetLinks']
assert extraction['ValidatedActionReportRows']>0
assert extraction['OptionSetName']=='Agreement-Enabled__Specification-Baseline__Cost-1__Fee-American'
for name in ('trial','settlement'):
    path=next(x for x in extraction['Paths'] if x['Name']==name)
    assert path['EquilibriumProbability']>0
    assert all(decision in [s['Decision'] for s in path['Steps']] for decision in ('PAgreeToBargain','DAgreeToBargain','POffer','DOffer'))
checks.append('Figure 2: fresh saved-profile extraction validates positive-probability agreement/offer histories and information-set links')
save_new(out/'data-preservation-validation.json',dict(Schema='restored-exhibits-data-validation-v1',Passed=True,CreatedUtc=utc(),
    Manifest=identity(out/'manifest.json'),PreviousManifest=identity(old/'manifest.json'),Checks=checks,SolvesStarted=0,
    ExactQuantityChanges=False,MissingProfiles=manifest['MissingProfiles'],FrozenSolverBuildsModified=False))
print('\n'.join(checks))
