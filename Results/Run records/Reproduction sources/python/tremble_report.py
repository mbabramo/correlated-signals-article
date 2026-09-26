"""Verify full diagnostic coverage and summarize local response sensitivity."""
import pathlib,json,hashlib,csv,statistics,datetime
import argparse
p=argparse.ArgumentParser();p.add_argument('--work',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
R=a.work;OUT=a.output
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
 with p.open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def csvwrite(p,rows):
 with p.open('x',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
done=read(R/'suite-completed.json');assert done['Passed']
profiles=read(R/'inputs/profiles.json');lookup={p['Id']:p for p in profiles}
primary={p['CaseId']:p for p in profiles if p['Kind']=='exact-primary'}
data=[];profile_rows=[];files=[]
for d in sorted((R/'results').glob('*-part-*')):
 status=read(d/'completed.json');assert status['Passed'] and status['SolvesStarted']==0
 for p in sorted(d.glob('*/completed.json')):
  assert read(p)['Passed'];folder=p.parent;original=lookup[folder.name];base=read(folder/'baseline.json');risk=original['CaseId'].split('__')[3];rule=original['CaseId'].split('__')[2]
  ref=primary[f'baseline__standard__american__{risk}__cost-1']['Welfare']
  flip=('plaintiff reversal' if base['Outcome']['Welfare'][0]>ref['MeritoriousPlaintiffShortfall'] else 'defendant reversal' if base['Outcome']['Welfare'][1]>ref['NonliableDefendantBurden'] else 'other') if rule=='complete' else 'American'
  these=[]
  for f in sorted(folder.glob('p*.json')):
   x=read(f);assert x['SelectionGapNormalized']<=1e-8
   if x['Epsilon']==0:assert x['OriginalReachWeightedTV']==0
   row=dict(Id=original['Id'],Kind=original['Kind'],Risk=risk,Rule=rule,Group=flip,Start=original['Start'],Player=x['Player'],Direction=x['Direction'],Epsilon=x['Epsilon'],NormalizedGain=x['NormalizedGain'],BaselineNormalizedGain=x['BaselineNormalizedGain'],IncrementalNormalizedGain=x['IncrementalNormalizedGain'],OriginalReachWeightedTV=x['OriginalReachWeightedTV'],PerturbedReachWeightedTV=x['PerturbedReachWeightedTV'],OffPathMeanTV=x['OffPathMeanTV'],SelectionGapNormalized=x['SelectionGapNormalized'])
   for i,k in enumerate(['PlaintiffShortfall','NonliableDefendantBurden','LiableDefendantExcess','GrossError','LitigationCosts']):
    row[k]=x['ResponseOutcome']['Welfare'][i];row[k+'ChangeFromZeroResponse']=x['ResponseOutcome']['Welfare'][i]-x['BaselineResponseOutcome']['Welfare'][i]
   for k in ['NotFiled','NotAnswered','Settlement','Abandonment','Default','Trial']:row[k+'ChangeFromZeroResponse']=x['ResponseOutcome'][k]-x['BaselineResponseOutcome'][k]
   these.append(row);files.append(dict(Path=str(f),Sha256=sha(f)))
  assert len(these)==32 and len({(x['Player'],x['Direction'],x['Epsilon']) for x in these})==32
  data+=these
  z=[x for x in these if x['Epsilon']==.01]
  profile_rows.append(dict(Id=original['Id'],Kind=original['Kind'],Risk=risk,Rule=rule,Group=flip,Start=original['Start'],WorstAdditionalGainAt1Percent=max(x['IncrementalNormalizedGain'] for x in z),WorstTotalGainAt1Percent=max(x['NormalizedGain'] for x in z),WorstReachWeightedTVAt1Percent=max(x['OriginalReachWeightedTV'] for x in z),WorstOffPathMeanTVAt1Percent=max(x['OffPathMeanTV'] for x in z),LargestWelfareChangeAt1Percent=max(abs(x[k+'ChangeFromZeroResponse']) for x in z for k in ['PlaintiffShortfall','NonliableDefendantBurden','LiableDefendantExcess','GrossError','LitigationCosts']),LargestDispositionChangeAt1Percent=max(abs(x[k+'ChangeFromZeroResponse']) for x in z for k in ['NotFiled','NotAnswered','Settlement','Abandonment','Default','Trial'])))
assert len(profile_rows)==203 and len({x['Id'] for x in profile_rows})==203 and len(data)==6496
groups=[]
for risk in ['rn','ra']:
 for rule in ['american','complete']:
  for group in (['American'] if rule=='american' else ['other','plaintiff reversal','defendant reversal']):
   z=[x for x in profile_rows if x['Kind']=='approximate' and x['Risk']==risk and x['Rule']==rule and x['Group']==group]
   if not z:continue
   row=dict(Risk=risk,Rule=rule,Group=group,Profiles=len(z))
   for k in ['WorstAdditionalGainAt1Percent','WorstTotalGainAt1Percent','WorstReachWeightedTVAt1Percent','LargestWelfareChangeAt1Percent','LargestDispositionChangeAt1Percent']:
    row[k]=dict(Minimum=min(x[k] for x in z),Median=statistics.median(x[k] for x in z),Maximum=max(x[k] for x in z))
   groups.append(row)
OUT.mkdir(parents=True,exist_ok=False);csvwrite(OUT/'profiles.csv',profile_rows);csvwrite(OUT/'all-tremble-tests.csv',data)
summary=dict(Passed=True,CreatedUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),Profiles=203,ApproximateProfiles=199,ExactPrimaryProfiles=4,Checks=6496,Groups=groups,Primary=[x for x in profile_rows if x['Kind']=='exact-primary'],MaximumSelectionGap=max(x['SelectionGapNormalized'] for x in data),Protocol=read(R/'inputs/protocol.json'),Execution=read(R/'suite-started.json'),Files=files,SolvesStarted=0)
write(OUT/'validation-and-summary.json',summary)
lines=['# Equilibrium tremble sensitivity','', 'All 199 accepted approximate profiles and four exact primary profiles passed baseline reproduction and the completed sensitivity checks. No equilibrium solve was run.','', 'At each opponent information set, the saved behavior was mixed with a uniform distribution or one of four frozen nonuniform full-support distributions. Tremble probabilities were 0.1%, 0.5% and 1%; each player was optimized separately. Chance probabilities and the full game were unchanged.','', 'The main statistic below is the largest *additional* best-response gain at 1% trembles across both players and five directions, relative to that profile\'s no-tremble gap. Gains are expressed as a percentage of the responding player\'s full terminal utility range. Repeated discoveries count as separate profiles; these counts do not measure equilibrium likelihood.','', '| Risk | Rule / profile group | Profiles | Median additional gain (%) | Range (%) | Median largest behavior change (%) |','|---|---|---:|---:|---:|---:|']
for g in groups:
 v=g['WorstAdditionalGainAt1Percent'];b=g['WorstReachWeightedTVAt1Percent']
 lines.append(f"| {g['Risk']} | {g['Rule']} / {g['Group']} | {g['Profiles']} | {100*v['Median']:.4f} | {100*v['Minimum']:.4f}–{100*v['Maximum']:.4f} | {100*b['Median']:.2f} |")
lines+=['','Behavior change is total-variation distance from the zero-tremble selected response, averaged over information sets using original reach weights. All off-path policies remain included in the complete records and are summarized separately.','', 'Response selection preserves original probabilities among actions within 1e-10 of the full terminal utility range of optimal continuation value. Every selected complete policy was independently checked against the untouched best-response value; its residual must be at most 1e-8. The precise gain uses the engine\'s unchanged strict best-response value.','', 'The CSV includes each welfare and disposition change relative to the no-tremble response. These are unilateral response experiments, not new equilibria, not a proof of trembling-hand perfection, and not predictions of selection frequency.','', '[Per-profile results](profiles.csv) · [All tests](all-tremble-tests.csv) · [Protocol, hashes and validation](validation-and-summary.json)','']
(OUT/'Report.md').write_text('\n'.join(lines),encoding='utf-8')
print(f'Generated tremble report for {len(profile_rows)} profiles and {len(data)} checks.')
