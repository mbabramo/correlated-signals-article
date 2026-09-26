"""Collect recalculated four-corner results; verify the ten main contrasts."""
import argparse,csv,json,pathlib,hashlib
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,required=True);p.add_argument('--work',type=pathlib.Path,required=True);a=p.parse_args()
rows=[];main=[];validated=[]
primary={c['CaseId']:c for c in read(a.work/'Results/Aggregated Data/selected-primary-catalog.json')['Cases']}
fields=dict(zip(['Meritorious plaintiff shortfall','Nonliable defendant burden','Liable defendant excess burden','Gross outcome error','Real litigation expenditures'],['MeritoriousPlaintiffShortfall','NonliableDefendantBurden','LiableDefendantExcessBurden','GrossOutcomeError','RealLitigationExpenditures']))
def identity(path):return dict(Path=str(path.resolve()),Sha256=hashlib.sha256(path.read_bytes()).hexdigest())
for folder in sorted((a.work/'welfare').iterdir()):
    data=read(folder/'decomposition.json');assert data['Passed'] and data['SolvesStarted']==0
    req=read(a.work/'requests'/('welfare-'+data['Id']+'.json'));spec=req['American']['Case']
    for label,c in data['Components'].items():
        assert c['AmericanWithAmericanProfile']==primary[spec['Id']]['Welfare']['Headline'][fields[label]], (spec['Id'],label)
        assert c['CompleteWithCompleteProfile']==primary[req['Complete']['Case']['Id']]['Welfare']['Headline'][fields[label]], (spec['Id'],label)
    validation=folder/'validation.json'
    validation.write_text(json.dumps(dict(Passed=True,CompleteEndpointValuesIdentical=True,Request=identity(a.work/'requests'/('welfare-'+data['Id']+'.json')),Outputs=[identity(folder/'decomposition.json')]),indent=2))
    validated.append(identity(validation))
    for label,c in data['Components'].items():
        assert abs(c['Residual'])<=1e-10
        row=dict(Risk='Risk neutral' if spec['AlphaP']==spec['AlphaD']==0 else 'Risk averse' if spec['AlphaP']==spec['AlphaD'] else 'Asymmetric risk',CostMultiplier=spec['CostMultiplier'],Measure=label,AmericanCase=spec['Id'],BritishCase=req['Complete']['Case']['Id'],**c)
        rows.append(row)
        if spec['Family'] in ['baseline','cost-multiplier']:main.append(row)
expected=list(csv.DictReader((a.package/'inputs/expected-main-decomposition.csv').open(encoding='utf-8-sig')))
key=lambda r:(r['AmericanCase'],r['Measure']);old={key(r):r for r in expected}
assert len(main)==len(old)==50
for row in main:
    for k,v in row.items():
        if isinstance(v,(float,int)):assert v==float(old[key(row)][k]),(key(row),k,v,old[key(row)][k])
        else:assert v==old[key(row)][k]
def csvwrite(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
csvwrite(a.work/'Results/Aggregated Data/Main-welfare-decomposition/welfare-decomposition.csv',main)
csvwrite(a.work/'Results/Aggregated Data/all-welfare-decompositions.csv',rows)
(a.work/'welfare-validation.json').write_text(json.dumps(dict(Passed=True,Pairs=len(rows)//5,MainRowsIdentical=len(main)),indent=2))
(a.work/'welfare-wave.json').write_text(json.dumps(dict(Passed=True,Catalog=identity(a.work/'Results/Aggregated Data/selected-primary-catalog.json'),Validated=validated),indent=2))
print(f'Regenerated {len(rows)//5} welfare comparisons; 50 main component rows identical.')
