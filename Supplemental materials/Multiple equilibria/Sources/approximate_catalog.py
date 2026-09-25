"""Audit every requested attempt and count three separate notions of distinctness.

Tolerances must be explicit. They affect only this descriptive catalog, never the
search, saved strategies, BR validation or exact-equivalence acceptance. Greedy
complete-link clusters use increasing start order; all pairs within each cluster
must meet the declared metric. No averaging or transitive-chain merging occurs.
"""
import argparse
import collections
import itertools
import math
import pathlib
import sys
from approximate_queue import ROOT, identity, inside, job_state, now, read, verify, write_new

HISTORY_KEYS = ('PSignal','DSignal','File','Answer','PExit','DExit','PAgree','DAgree','POffer','DOffer')

def reached_distribution(profile):
    grouped = collections.defaultdict(list)
    for row in profile['ReachedHistories']:
        p = row['Probability']
        if not math.isfinite(p) or p <= 0: raise ValueError('Invalid reached-history probability')
        grouped[tuple(row[k] for k in HISTORY_KEYS)].append(p)
    distribution = {k:math.fsum(v) for k,v in grouped.items()}
    if abs(math.fsum(distribution.values())-1) > 1e-9: raise ValueError('Reached-history mass does not sum to one')
    return distribution

def strategy_distance(a,b):
    if a['coordinates'] != b['coordinates']: raise ValueError('Complete strategy coordinates changed within a core game')
    return max(abs(x-y) for x,y in zip(a['probabilities'],b['probabilities'],strict=True))

def reached_distance(a,b):
    p,q = a['reached'],b['reached']
    return 0.5*math.fsum(abs(p.get(k,0)-q.get(k,0)) for k in p.keys()|q.keys())

def outcome_distance(a,b):
    p,q = a['outcomes'],b['outcomes']
    if p.keys()!=q.keys(): raise ValueError('Outcome coordinates changed')
    differences=[]
    for k in p:
        if p[k] is None or q[k] is None:
            if p[k] is not q[k]: return math.inf
        else: differences.append(abs(p[k]-q[k]))
    return max(differences,default=0)

def complete_link(items, metric, tolerance):
    if not math.isfinite(tolerance) or tolerance < 0: raise ValueError('Declare a finite nonnegative catalog tolerance')
    clusters=[]
    for item in sorted(items,key=lambda x:x['StartIndex']):
        group = next((g for g in clusters if all(metric(item,other)<=tolerance for other in g)),None)
        if group is None: clusters.append([item])
        else: group.append(item)
    return [dict(Cluster=n+1,RepresentativeStart=g[0]['StartIndex'],Starts=[i['StartIndex'] for i in g],
        RecoveryCount=len(g),MaximumPairwiseDistance=max((metric(a,b) for a,b in itertools.combinations(g,2)),default=0))
        for n,g in enumerate(clusters)]

def accepted_profile(job, result, selection, maximum_pivots=1000):
    output=pathlib.Path(job['Output'])
    validation=result.get('Validation')
    accepted=selection['Decision']['Accepted']
    if not validation or validation.get('Passed') is not True or validation.get('CompleteVectorRoundTripExact') is not True:
        raise ValueError('An accepted attempt lacks complete reload/audit validation')
    reason=selection['Decision']['Reason']
    average=accepted['AverageGain']
    threshold=0.001 if reason=='first-below-0.001' else 0.0025 if reason=='cap-accepted' else None
    if threshold is None or not math.isfinite(average) or not 0<=average<threshold:
        raise ValueError('Accepted attempt does not satisfy the strict recorded threshold')
    if reason=='cap-accepted' and (average<0.001 or selection['Decision']['StoppingPivot']!=maximum_pivots):
        raise ValueError('Cap catalog overlaps early acceptance or did not reach the cap')
    if average!=validation['AverageGain'] or threshold!=validation['Threshold']:
        raise ValueError('Selection and reload gains differ')
    profile_paths=list((output/'Sources'/'Profiles').glob('*.json'))
    if len(profile_paths)!=1: raise ValueError('Accepted start must export exactly one complete profile')
    profile=read(profile_paths[0])
    if not profile.get('AgreementEnabled'): raise ValueError('Agreement-disabled profile cannot enter the catalog')
    vector=[p for s in profile['Strategies'] for p in s['Probabilities']]
    if vector!=accepted['Probabilities']: raise ValueError('Export differs from the selected complete strategy')
    if not vector or any(not math.isfinite(p) or not 0<=p<=1 for p in vector): raise ValueError('Invalid strategy vector')
    for s in profile['Strategies']:
        if abs(math.fsum(s['Probabilities'])-1)>1e-9: raise ValueError('Unnormalized strategy')
    outcomes={'metric:'+k:v for k,v in profile['Metrics'].items()}
    outcomes.update({'welfare:'+k:v for k,v in validation['Welfare']['Headline'].items()})
    if any(v is not None and (not isinstance(v,(int,float)) or not math.isfinite(v)) for v in outcomes.values()):
        raise ValueError('Outcome metric must be finite numeric or explicitly undefined')
    item=dict(StartIndex=job['StartIndex'],Band='below-0.001' if reason=='first-below-0.001' else 'cap-0.001-to-0.0025',
        SelectedPivot=accepted['Pivot'],StoppingPivot=selection['Decision']['StoppingPivot'],
        AverageGain=average,MaximumGain=validation['MaximumGain'],RawGains=validation['FullBestResponseRawGains'],
        AcceptanceGains=validation['AcceptanceGains'],Result=identity(output/'result.json'),Profile=identity(profile_paths[0]),
        coordinates=[(s['InformationSet'],s['Player'],s['Decision'],tuple(s['Actions'])) for s in profile['Strategies']],
        probabilities=vector,reached=reached_distribution(profile),outcomes=outcomes)
    return item

def build(queue_path, output, tolerances):
    queue=read(queue_path)
    if queue['Schema']!='finite-four-core-approximate-queue-v1': raise ValueError('Not an approximate queue')
    output=inside(output,ROOT/'reporting')
    if len(queue['Jobs'])!=4*queue['StartsPerCore']: raise ValueError('Incomplete requested attempt inventory')
    records=[]; accepted=collections.defaultdict(list)
    for job in queue['Jobs']:
        state=job_state(job)
        record=dict(CaseId=job['CaseId'],StartIndex=job['StartIndex'],State=state,Request=identity(verify(job['Request'])))
        if state=='completed':
            directory=pathlib.Path(job['Output']); result=read(directory/'result.json'); selection=read(directory/'selection.json')
            if selection['StartIndex']!=job['StartIndex'] or selection['ActualPriorSeed']!=1_000_000+job['StartIndex']:
                raise ValueError('Recorded initialization differs from the requested start')
            if result['Decision']!=selection['Decision'] or result['Accepted']!=(selection['Decision']['Accepted'] is not None):
                raise ValueError('Result and selection disagree')
            record.update(Accepted=result['Accepted'],Reason=selection['Decision']['Reason'],
                EvaluatedPivots=selection['EvaluatedPivots'],InvalidCandidates=selection['InvalidCandidates'],
                Error=selection['Error'],ElapsedSeconds=result['ElapsedSeconds'],Result=identity(directory/'result.json'))
            if result['Accepted']:
                item=accepted_profile(job,result,selection,read(verify(job['Request'])).get('MaximumPivots',1000))
                accepted[(job['CaseId'],item['Band'])].append(item)
                record.update({k:v for k,v in item.items() if k not in ('coordinates','probabilities','reached','outcomes')})
            elif selection['EvaluatedPivots']>0 and selection['InvalidCandidates']==selection['EvaluatedPivots']:
                record['FailureDetail']='all-evaluated-profiles-invalid'
        records.append(record)
    catalogs=[]
    for (case,band),items in sorted(accepted.items()):
        catalogs.append(dict(CaseId=case,Band=band,AcceptedStarts=len(items),RequestedStarts=queue['StartsPerCore'],
            CompleteStrategies=complete_link(items,strategy_distance,tolerances['CompleteStrategyMaxAbsolute']),
            ReachedBehavior=complete_link(items,reached_distance,tolerances['ReachedHistoryTotalVariation']),
            Outcomes=complete_link(items,outcome_distance,tolerances['OutcomeMaxAbsolute'])))
    counts=dict(collections.Counter(r['State'] for r in records))
    result=dict(Schema='approximate-attempt-catalog-v1',CreatedUtc=now(),Queue=identity(queue_path),Script=identity(__file__),
        Command=[sys.executable,*sys.argv],Complete=counts.get('completed',0)==len(records),RequestedAttempts=len(records),
        StateCounts=counts,AcceptedStarts=sum(bool(r.get('Accepted')) for r in records),Attempts=records,Catalogs=catalogs,
        Tolerances=tolerances,Clustering='Start-ordered greedy complete-link; every within-cluster pair must pass; no profile averaging.',
        ReachedBehaviorDefinition='Joint distribution of complete observed decision histories, aggregating omitted truth/court copies.',
        OutcomeDefinition='All unrounded exported participation/disposition metrics plus the five monetary welfare measures. Null is distinct from a number.',
        Interpretation='Recovery counts describe this finite numerical search, not litigant selection probabilities or an enumeration of all equilibria.',
        ExactEquivalenceUsesTheseTolerances=False,PrimaryEquilibriumCatalog=False)
    output.parent.mkdir(parents=True,exist_ok=True); write_new(output,result)
    print(__import__('json').dumps(dict(Output=str(output),Complete=result['Complete'],StateCounts=counts,AcceptedStarts=result['AcceptedStarts'])))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue',type=pathlib.Path,required=True); parser.add_argument('--output',type=pathlib.Path,required=True)
    for name in ('strategy-tolerance','reached-tv-tolerance','outcome-tolerance'): parser.add_argument('--'+name,type=float,required=True)
    args=parser.parse_args()
    tolerances=dict(CompleteStrategyMaxAbsolute=args.strategy_tolerance,ReachedHistoryTotalVariation=args.reached_tv_tolerance,OutcomeMaxAbsolute=args.outcome_tolerance)
    if any(not math.isfinite(v) or v<0 for v in tolerances.values()): raise ValueError('Tolerances must be finite and nonnegative')
    build(args.queue.resolve(),args.output.resolve(),tolerances)

if __name__=='__main__': main()
