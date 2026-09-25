"""Conservative compute reservations from frozen snapshots, without live polling."""
import hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))

def primary_reservations():
    cohorts=[]; group_capacity=0
    snapshots=[]
    for path in (ROOT/'imports').glob('*/snapshot.json'):
        record=read(path)
        if record.get('Schema')=='final-primary-completion-snapshot-v1': snapshots.append((record['CheckedUtc'],record))
    for path in (ROOT/'production').glob('*/queue/final-launch.json'):
        launch=read(path); manifest_path=pathlib.Path(launch['Manifest']); manifest=read(manifest_path)
        manifest_sha=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        budget=manifest['Resources']
        group_capacity=max(group_capacity,budget['GlobalCeiling']-budget['ExternalWorkersReserved']-budget['OtherWorkersReserved'])
        expected=sum(not c['Parameters'].get('OriginalOptionName') for c in manifest['Cases'])
        cap=min(expected,budget['MaximumNewWorkers']); evidence='frozen cohort maximum'
        done=path.parent/'final-scheduler-result.json'
        if done.exists() and read(done).get('Passed'): cap=0; evidence=str(done)
        else:
            matching=[(t,s) for t,s in snapshots if s['OriginManifest']['Sha256'].lower()==manifest_sha]
            if matching:
                _,s=max(matching,key=lambda x:x[0]); tasks=[t for t in s['Tasks'] if t['TaskType']=='Optimize']
                if len(tasks)!=expected: raise ValueError('Frozen task snapshot has an incomplete case inventory')
                primary=sum(not t['Complete'] and not t['Failed'] for t in tasks)
                other=any(not t['Complete'] and not t['Failed'] for t in s['Tasks'] if t['TaskType']!='Optimize')
                cap=min(cap,primary if primary else int(other)); evidence=s['CheckedUtc']
        cohorts.append(dict(Manifest=str(manifest_path),UpperBound=cap,Evidence=evidence))
    # The expanding cohort already subtracts earlier cohort work; summing both
    # immutable maxima must not double-count those shared slots.
    return dict(Workers=min(group_capacity,sum(c['UpperBound'] for c in cohorts)),Cohorts=cohorts,
        Method='Conservative bound from immutable manifests and completion snapshots; no live queue or process read')

def original_reservations():
    evidence_path=ROOT/'provenance/original-computation-complete.json'
    if not evidence_path.exists():return 3
    evidence=read(evidence_path)
    file=evidence['Completion']
    path=pathlib.Path(file['Path'])
    if hashlib.sha256(path.read_bytes()).hexdigest()!=file['Sha256']:
        raise ValueError('Original completion evidence changed')
    completed=read(path)
    if (evidence.get('Schema')!='completed-original-computation-reservation-v1' or
        completed.get('Status')!='SolvedAndAggregated' or completed.get('Cases')!=30 or not completed.get('EndedUtc') or
        completed.get('SourceCommit')!='80b1049dfc9c89a08e8b4923d0bdfa9e07eca060'):
        raise ValueError('Original computation is not authoritatively complete')
    return 0

def nonreporting_reservations():
    primary=primary_reservations()
    path=ROOT.parent/'ecta-performance-20260923'/'provenance'/'latest-benchmark-check.json'
    benchmark=0 if path.exists() and read(path).get('Complete') else 1
    original=original_reservations()
    return dict(Total=original+benchmark+primary['Workers'],Original=original,Benchmark=benchmark,Primary=primary,Ceiling=32)
