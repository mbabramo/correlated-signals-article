"""Regenerate the curated primary catalog, outcomes, and unchanged strategy presentation."""
import argparse,csv,hashlib,json,pathlib,shutil
from individual_strategy_sources import source
from build_profile_catalog import validate_profile
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def identity(p):return dict(Path=str(p),Sha256=sha(p))
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,allow_nan=False),encoding='utf-8')
p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,required=True);p.add_argument('--work',type=pathlib.Path,required=True);a=p.parse_args()
catalog=read(a.package/'inputs/selected-primary-catalog.json');cases={c['CaseId']:c for c in catalog['Cases']}
expected=list(csv.DictReader((a.package/'inputs/selected-primary-outcomes.csv').open(encoding='utf-8-sig')))
expected_by_id={r['CaseId']:r for r in expected};rows=[];checks=[]
for request in read(a.package/'inputs/primary.json'):
    case_id=request['CaseId'];raw=a.work/'primary'/case_id;validation=read(raw/'validation.json')
    profiles=list((raw/'Sources/Profiles').glob('*.json'));assert len(profiles)==1
    profile=read(profiles[0]);prior=read(a.package/request['ExpectedProfile']);metrics=validate_profile(validation,profile)
    # Every scientific coordinate is exactly equal to the previous replay, including off-path behavior.
    scientific={k:v for k,v in profile.items() if k not in ['Profile','ActionReport','ReplayReport']}
    prior_scientific={k:v for k,v in prior.items() if k not in ['Profile','ActionReport','ReplayReport']}
    assert scientific==prior_scientific, 'Scientific replay changed: '+case_id
    prior_audit=read(a.package/request['ExpectedAudit'])
    assert validation['Welfare']==prior_audit['Welfare'], 'Welfare replay changed: '+case_id
    folder=a.work/'Results/Individual simulations'/case_id;sources=folder/'Sources';sources.mkdir(parents=True)
    shutil.copy2(raw/'validation.json',sources/'individual-audit.json');shutil.copy2(profiles[0],sources/'complete-profile.json')
    shutil.copy2(raw/'replayed-report.csv',sources/'replayed-report.csv')
    (sources/'strategy.tex').write_text(source(validation,profile),encoding='utf-8',newline='\n')
    case=cases[case_id];case.update(Audit=identity(sources/'individual-audit.json'),CompleteProfile=identity(sources/'complete-profile.json'),Welfare=validation['Welfare'],ParticipationAndDispositions=metrics,FullBestResponseGains=validation['FullBestResponseGains'])
    spec=request['Case'];flat=dict(CaseId=case_id,Family=spec['Family'],Variant=spec['Variant'],FeeRule=spec['FeeRule'],AlphaP=spec['AlphaP'],AlphaD=spec['AlphaD'],CostMultiplier=spec['CostMultiplier'],Signals=spec['Signals'],Offers=len(spec['Offers']),**metrics,**validation['Welfare']['Headline'])
    row={k:flat[k] for k in expected[0]}
    old=expected_by_id[case_id]
    for k,v in row.items():
        if isinstance(v,(float,int)):assert abs(float(old[k])-v)<=1e-10,(case_id,k)
        else:assert ('' if v is None else str(v))==old[k],(case_id,k)
    rows.append(row);checks.append(dict(CaseId=case_id,ScientificProfileIdentical=True,WelfareIdentical=True,Passed=True))
aggregate=a.work/'Results/Aggregated Data';aggregate.mkdir(parents=True)
catalog['Reproduction']='Fresh Release build, full primary audits, exact saved scientific-profile comparison; no solves.'
catalog['Cases']=list(cases.values());write(aggregate/'selected-primary-catalog.json',catalog)
def csvwrite(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
csvwrite(aggregate/'selected-primary-outcomes.csv',rows)
main=[r for r in rows if r['Family'] in ['baseline','cost-multiplier'] and r['FeeRule'] in ['american','complete']]
assert len(main)==20
csvwrite(aggregate/'American-British-cost-outcomes-20/selected-exact-outcomes.csv',main)
(aggregate/'README.md').write_text('# Aggregated data\n\n'+str(len(rows))+' revalidated primary profiles; all 20 main American/British cost-series profiles are present. The selected catalog lists the two incomplete grid cases.\n\n- [Outcomes](selected-primary-outcomes.csv)\n- [Catalog](selected-primary-catalog.json)\n- [Welfare decompositions](Main-welfare-decomposition/welfare-decomposition.csv)\n- [Tremble sensitivity](Equilibrium%20sensitivity/Report.md)\n',encoding='utf-8')
(a.work/'Results/Individual simulations/README.md').write_text('# Individual simulations\n\nEach complete profile was reloaded and checked for normalization, full unilateral best response, accounting, saved actions and numeric replay. All scientific profile data match the previous audited outputs exactly.\n\n'+'\n'.join('- ['+r['CaseId']+']('+r['CaseId']+'/strategy.pdf)' for r in rows)+'\n',encoding='utf-8')
write(a.work/'primary-validation.json',dict(Passed=True,Profiles=len(rows),Results=checks))
print(f'Regenerated {len(rows)} individual and aggregate primary reports.')
