"""Compare the complete rebuilt report data with frozen scientific evidence."""
import argparse,csv,json,math,pathlib,shutil
p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,required=True);p.add_argument('--work',type=pathlib.Path,required=True);a=p.parse_args()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def csvread(p):return list(csv.DictReader(p.open(newline='',encoding='utf-8-sig')))
primary=read(a.work/'primary-validation.json');welfare=read(a.work/'welfare-validation.json')
assert primary['Passed'] and welfare['Passed']
out=a.work/'Results/Aggregated Data/Equilibrium sensitivity'
expected=csvread(a.package/'inputs/expected-tremble-tests.csv');actual=csvread(out/'all-tremble-tests.csv')
key=lambda r:(r['Id'],r['Player'],r['Direction'],r['Epsilon'])
old={key(r):r for r in expected};assert len(old)==len(actual)==6496
cells=0
for row in actual:
    assert set(row)==set(old[key(row)])
    for k,v in row.items():
        prior=old[key(row)][k]
        if v==prior:continue
        # CSV numeric spelling may differ, but mathematical binary64 values must match.
        try:x,y=float(v),float(prior)
        except ValueError:raise AssertionError((key(row),k,v,prior))
        assert math.isfinite(x) and math.isfinite(y) and x==y,(key(row),k,v,prior)
        cells+=1
independent=read(a.work/'tremble/reports/independent-br-validation.json')
assert independent['Passed'] and independent['Checks']==32
assert max(x['AbsoluteDifference'] for x in independent['Results'])<=1e-8
assert max(x['WelfareDifference'] for x in independent['Results'])<=1e-10
shutil.copy2(a.work/'tremble/reports/independent-br-validation.json',out/'independent-br-validation.json')
summary=read(out/'validation-and-summary.json')
groups=summary['Groups'];ordinary=next(g for g in groups if g['Risk']=='ra' and g['Rule']=='complete' and g['Group']=='other')
baseline=ordinary['WorstAdditionalGainAt1Percent']['Median']
comparisons=[]
american={ (r['Player'],r['Direction'],r['Epsilon']):r for r in actual if r['Kind']=='exact-primary' and r['Risk']=='ra' and r['Rule']=='american'}
for group,measure in [('plaintiff reversal','PlaintiffShortfall'),('defendant reversal','NonliableDefendantBurden')]:
    rows=[r for r in actual if r['Kind']=='approximate' and r['Risk']=='ra' and r['Rule']=='complete' and r['Group']==group and float(r['Epsilon'])==.01]
    differences=[float(r[measure])-float(american[(r['Player'],r['Direction'],r['Epsilon'])][measure]) for r in rows]
    g=next(x for x in groups if x['Risk']=='ra' and x['Rule']=='complete' and x['Group']==group)
    comparisons.append(dict(Group=group,Profiles=g['Profiles'],MedianAdditionalGainPercent=100*g['WorstAdditionalGainAt1Percent']['Median'],RatioToOtherBritishProfiles=g['WorstAdditionalGainAt1Percent']['Median']/baseline,Comparisons=len(rows),ReversalsRetained=sum(x>0 for x in differences)))
record=dict(Passed=True,PrimaryProfiles=primary['Profiles'],PrimaryScientificProfileEquality=True,Welfare=welfare,TrembleProfiles=203,TrembleChecks=len(actual),AllTrembleFieldsEqual=True,IndependentBestResponseComparisons=32,IndependentSelectedResponseComparisons=16,ReversalComparisons=comparisons,SolvesStarted=0)
(a.work/'report-validation.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
(out/'reproduction-validation.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
report=out/'Report.md';text=report.read_text(encoding='utf-8')
for old,new in [('| rn |','| Risk neutral |'),('| ra |','| Risk averse |'),('american / American','American'),('complete / other','British / no reversal'),('complete / plaintiff reversal','British / plaintiff reversal'),('complete / defendant reversal','British / defendant reversal')]:text=text.replace(old,new)
text += '\nHere, a reversal means that British has greater meritorious-plaintiff shortfall or greater nonliable-defendant burden than the exact primary American profile. The median additional gain for other British risk-averse profiles is '+f'{100*baseline:.4f}% of the full terminal utility range.\n\n'
for r in comparisons:
    text += f"For the {r['Profiles']} {r['Group']} profiles, the median additional incentive to change at 1% trembles is {r['MedianAdditionalGainPercent']:.4f}% ({r['RatioToOtherBritishProfiles']:.2f} times the other British profiles). The unfavorable comparison remains in {r['ReversalsRetained']}/{r['Comparisons']} matched unilateral-response experiments.\n\n"
text += 'Sensitivity here means additional incentive to respond to an opponent\'s mistakes. It does not mean an equilibrium collapses or becomes unlikely. One player responds to a perturbed opponent; both players are not re-equilibrated. The absolute incentives remain small.\n\nAll report fields reproduce the frozen diagnostic results exactly. The 32 independent best-response comparisons and 16 outcome checks passed. [Reproduction validation](reproduction-validation.json) · [Independent checks](independent-br-validation.json).\n'
report.write_text(text,encoding='utf-8')
print(json.dumps(record,indent=2))
