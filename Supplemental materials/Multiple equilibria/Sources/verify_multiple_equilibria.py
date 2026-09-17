from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import argparse, csv, hashlib, json, math, re
from pypdf import PdfReader
from PIL import Image

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def near(a,b,tol=1e-10):
    assert math.isfinite(a) and math.isfinite(b) and abs(a-b)<=tol, (a,b)
def fingerprints(j):
    if isinstance(j,dict):
        if 'Path' in j and 'Sha256' in j: yield j
        for v in j.values(): yield from fingerprints(v)
    elif isinstance(j,list):
        for v in j: yield from fingerprints(v)

def verify(root):
    inventory=read(root/'multiple-equilibria-exhibits.json')
    original=Path(inventory['Summary']['Path']).parent.parent
    def local(p):
        p=Path(p)
        return root/p.relative_to(original) if p.is_relative_to(original) else p
    checked=set()
    def check(j):
        for f in fingerprints(j):
            p=local(f['Path'])
            assert p.is_file() and sha(p).lower()==f['Sha256'].lower(), str(p)
            checked.add(str(p))
    assert inventory['Compiled'] and inventory['Validation']['OptionSetCount']==6
    check(inventory)
    audit=read(root/'Sources/strategy-verification.json');check(audit)
    assert len(audit['Profiles'])==inventory['Validation']['EquilibriumCount']
    assert all(abs(g)<=audit['Tolerance'] for p in audit['Profiles'] for g in p['PlayerGains'])
    audited={(p['OptionSet'],p['Equilibrium']):p for p in audit['Profiles']}
    outcomes=rows(root/'Sources/equilibrium-outcomes.csv');ranges=rows(root/'Sources/equilibrium-ranges.csv')
    groups=defaultdict(list)
    for r in outcomes: groups[r['OptionSetName']].append(r)
    assert len(groups)==len(ranges)==6
    raw=root/'Sources/Production';manifest=read(raw/'CS004ME run manifest.json')
    assert set(groups)==set(manifest['OptionSetNames']) and manifest['Status'] in ('Solved','Aggregated')
    assert manifest['WorkingTreeWasDirty'] is False
    cases=[];cells=0
    def n(row,k): return float(row[k])
    def payment(r):
        settles=n(r,'SettlesBR1');default=n(r,'DDefaultsBR1')
        residual=n(r,'DAnswers')-settles-default-n(r,'PAbandonsBR1')-n(r,'Trial')
        if abs(residual)>1e-5:
            near(residual,n(r,'BothReadyToGiveUp'),1e-5);default+=.5*n(r,'BothReadyToGiveUp')
        return settles*(n(r,'ValIfSettled') if settles else 0)+n(r,'DDoesntAnswer')+default+n(r,'P Wins')
    for option,items in groups.items():
        rec=rows(raw/f'CS004ME {option} -EquilibriumRecoveries.csv');first=rec[0]
        profiles=(raw/f'CS004ME {option} -equ.csv').read_text().strip().splitlines()
        assert len(profiles)==len(set(profiles))==len(items)==len(rec)==int(first['Distinct Reported Strategy Profiles'])
        recoveries=sum(int(r['Recovery Count']) for r in rec)
        assert recoveries==int(first['Verified Recoveries'])<=int(first['Requested Priors'])==50
        assert int(first['Attempted Solves'])==int(first['Inexact Attempts'])+int(first['Exact Attempts'])
        for r in rec: near(n(r,'Recovery Share of Verified Recoveries'),n(r,'Recovery Count')/recoveries)
        logs=list(raw.glob(f'CS004ME {option}  task-*-log.txt'));assert len(logs)==1
        log=logs[0].read_text(encoding='utf-8-sig')
        final=re.split(r'Using exact arithmetic for \d+ remaining random priors',log)[-1]
        cutoffs=final.count('ECTA algorithm failed Max (1000) pivoting steps reached.')
        cases.append(dict(OptionSet=option,Risk=items[0]['Risk Aversion'],FeeRule=items[0]['Fee Rule'],
            Requested=50,Attempts=int(first['Attempted Solves']),Recoveries=recoveries,Profiles=len(profiles),ExactCutoffs=cutoffs))
        for r in items:
            key=(option,int(r['Equilibrium']));assert key in audited
            near(n(r,'Exploitability'),audited[key]['MaximumGain'])
            detail={d['Filter']:d for d in rows(raw/r['Source File'])}
            a,l,u=(detail[k] for k in ['All','Truly Liable','Truly Not Liable'])
            expected={
                'Plaintiff shortfall contribution':.5*n(l,'False-'),
                'Nonliable defendant contribution':.5*n(u,'False+'),
                'Liable defendant contribution':.5*n(l,'False+'),
                'Outcome Error Before Legal Costs and Fee Transfers':.5*(1-payment(l))+.5*payment(u),
                'Real Litigation Costs':n(a,'TotExpense'),
                'Does Not File':n(a,'PDoesntFile'),'Does Not Answer':n(a,'DDoesntAnswer'),
                'Settles':n(a,'SettlesBR1'),
                'P Abandons (Mutual Give-Up Allocated)':n(a,'PAbandonsBR1')+.5*n(a,'BothReadyToGiveUp'),
                'D Defaults (Mutual Give-Up Allocated)':n(a,'DDefaultsBR1')+.5*n(a,'BothReadyToGiveUp'),
                'P Loses':n(a,'P Loses'),'P Wins':n(a,'P Wins')}
            for k,v in expected.items(): near(n(r,k),v);cells+=1
            near(sum(expected[k] for k in list(expected)[5:]),1,1e-4)
    range_cells=0
    for r in ranges:
        for k in r:
            if not k.startswith('Minimum '):continue
            metric=k[8:];v=[n(o,metric) for o in groups[r['OptionSetName']]]
            mean=sum(v)/len(v);sd=math.sqrt(sum((x-mean)**2 for x in v)/len(v))
            expected={'Minimum':min(v),'Maximum':max(v),'Range':max(v)-min(v),'Mean':mean,'Standard Deviation':sd}
            for prefix,value in expected.items():near(n(r,prefix+' '+metric),value);range_cells+=1
    table_numbers=0
    filing_chart_entries=0
    for p in audit['Profiles']:
        if 'ReplayReport' not in p:
            continue
        action_rows=list(csv.DictReader(local(p['ActionReport']).open(encoding='utf-8-sig')))
        filing=[a for a in action_rows if a['Decision']=='P Files' and a['Action Label']=='Yes']
        filing.sort(key=lambda a:int(re.search(r'Liability Signal: (\d+)',a['Information Set Labels'])[1]))
        tex=local(next(s for s in p['DiagramSources'] if '-fileans-' in s)).read_text(encoding='utf-8-sig')
        shown=[float(s) for s in re.findall(r'node\[midway\] \{([\d.]+)\\%\}',tex)][:20]
        expected=[100*float(a['Equilibrium Action Probability']) for a in filing]
        expected += [100-v for v in expected]
        assert len(shown)==len(expected)==20,p['OptionSet']
        assert all(abs(a-b)<=.500001 for a,b in zip(shown,expected)),(p['OptionSet'],p['Equilibrium'],shown,expected)
        filing_chart_entries += len(shown)
    def numbers(s):
        s=s.replace('\u2212','-').replace('\u2013',' ').replace('--',' ')
        s=re.sub(r'(?<=\d)\s*\.\s*(?=\d)','.',s)
        return [float(x) for x in re.findall(r'[+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?',s)]
    for artifact in inventory['Artifacts']:
        source=local(artifact['Source']['Path']);pdf=local(artifact['Pdf']['Path']);png=local(artifact['Png']['Path'])
        doc=PdfReader(pdf);assert len(doc.pages)==1,str(pdf)
        with Image.open(png) as im: assert im.width>100 and im.height>50
        if 'Individual simulations' not in source.parts:
            tex=source.read_text(encoding='utf-8-sig')
            body='\n'.join(line for line in tex.splitlines() if line.startswith(('Risk Neutral &','Risk Averse &')))
            a=numbers(doc.pages[0].extract_text());b=numbers(body)
            assert a==b,(str(pdf),a,b)
            table_numbers+=len(b)
            data=read(source.with_suffix('.json'));check(data)
            for row in data['Data']:assert row in ranges
    assert len(inventory['Artifacts'])==6*len(outcomes)+7
    result=dict(VerifiedUtc=datetime.now(timezone.utc).isoformat(),Status='Passed',Cases=cases,
        TotalRecoveries=sum(c['Recoveries'] for c in cases),DistinctProfiles=len(outcomes),
        ActionRowsReproduced=sum(p['ActionRows'] for p in audit['Profiles']),MaximumBestResponseGain=max(p['MaximumGain'] for p in audit['Profiles']),
        NumericOutcomeCells=cells,RangeCells=range_cells,TableNumericEntries=table_numbers,
        ReplayedOutcomeCells=sum(p.get('ReproducedOutcomeCells',0) for p in audit['Profiles']),
        FilingDiagramPercentagesVerified=filing_chart_entries,
        Exhibits=len(inventory['Artifacts']),Fingerprints=len(checked),
        NumericalSourceCommit=manifest['GitCommit'],SourceRoot=str(original),VerifiedRoot=str(root),
        Scope='Saved-profile audit, source-derived welfare and dispositions, dispersion statistics, rendered table values, PDF/PNG completeness and SHA256 provenance. Visual review recorded separately.')
    (root/'Sources/final-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('root',type=Path)
    verify(parser.parse_args().root.resolve())
