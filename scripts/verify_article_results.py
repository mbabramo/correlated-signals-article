"""Verify the retained article collection without rewriting any scientific outputs.

Requires pypdf. Optional --compare-results compares against ACESim4/ReportResults.
Writes a compact summary and per-artifact hashes to Results/Run records.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, re, subprocess
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'Results'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,j):p.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8',newline='\n')
def fingerprints(j):
    if isinstance(j,dict):
        if 'Path' in j and 'Sha256' in j:yield j
        for v in j.values():yield from fingerprints(v)
    elif isinstance(j,list):
        for v in j:yield from fingerprints(v)
def check_fingerprint(f):
    p=Path(f['Path']);assert p.is_file(),str(p)
    assert sha(p).lower()==f['Sha256'].lower(),str(p)

def verify(compare=None):
    inv=read(RESULTS/'Run records/diagram-inventory.json')
    assert inv['Cases']==124 and inv['Compiled'] and len(inv['Artifacts'])==937
    kinds=Counter(a['Kind'] for a in inv['Artifacts'])
    assert kinds=={'individual-results':744,'selection-offers':57,'welfare-outcomes':68,'dispositions':68},kinds
    artifacts=[];numeric=0
    for a in inv['Artifacts']:
        rel=Path(a['Source']).relative_to(Path(inv['Root']))
        source=RESULTS/rel
        assert source.is_file() and source.parent.name=='Sources',str(source)
        assert 'node[midway] {\\huge Costs:' not in source.read_text(encoding='utf-8-sig')
        outdir=source.parent.parent
        record={'Kind':a['Kind'],'Source':str(rel),'SourceSha256':sha(source)}
        for ext in ['.pdf','.png']:
            p=outdir/(source.stem+ext);assert p.is_file() and p.stat().st_size>1000,str(p)
            record[ext[1:].upper()]={'Path':str(p.relative_to(RESULTS)),'Sha256':sha(p)}
            if compare:
                other=compare/p.relative_to(RESULTS);assert sha(other)==sha(p),str(p)
        pdf=PdfReader(outdir/(source.stem+'.pdf'))
        assert len(pdf.pages)==1,str(source)
        record['PageSize']=[float(pdf.pages[0].mediabox.width),float(pdf.pages[0].mediabox.height)]
        if a['Kind']=='welfare-outcomes':
            j=read(source.with_suffix('.json'))
            cells=[c for panel in j['Panels'] for row in panel['Rows'] for c in row['Cells'] if c['Value'] is not None]
            printed=re.findall(r'(?<![\d.])-?\d+\.\d{4}(?![\d.])',pdf.pages[0].extract_text())
            assert printed==[c['Latex'] for c in cells],str(source)
            assert all(abs(float(c['Latex'])-c['Value'])<=.0000500001 for c in cells),str(source)
            numeric+=len(cells)
        artifacts.append(record)
    assert numeric==890,numeric
    assert len(list(RESULTS.glob('Aggregated Data/**/*.pdf')))==193
    assert len(list(RESULTS.glob('Individual simulations/**/*.pdf')))==744
    assert len(list(RESULTS.glob('Aggregated Data/*/Risk Comparison')))==3
    manifest=read(ROOT/'manuscript-exhibits.json')['Exhibits']
    for f in manifest:
        p=ROOT/f['Output'];assert sha(p)==f['Sha256'],str(p)
        origin=ROOT/f['Source']
        if origin.is_file():assert sha(origin)==sha(p),str(origin)
    for folder,n in [('Figures',4),('Tables',3)]:
        assert len(list((ROOT/folder).glob('*.pdf')))==n
        assert len(list((ROOT/folder).glob('*.png')))==n
        for p in (ROOT/folder).glob('*.pdf'):
            assert len(PdfReader(p).pages)==1,str(p)
            for ext in ['.tex','.json','.txt']:assert (ROOT/folder/'Sources'/(p.stem+ext)).is_file(),str(p)
    supp=ROOT/'Supplemental materials'
    expected={'Equilibrium solution paths','Equilibrium strategy changes','Game tree diagrams','Liability signals diagrams','Multiple equilibria'}
    assert {p.name for p in supp.iterdir() if p.is_dir()}==expected
    retained_profiles=read(supp/'Equilibrium strategy changes/Sources/profile-provenance.json')
    for f in fingerprints(retained_profiles):check_fingerprint(f)
    supplemental=read(supp/'Equilibrium strategy changes/Sources/supplemental-verification.json')
    assert supplemental['Scope']=='complete supplemental expansion'
    assert supplemental['DirectedContrasts']==90 and len(supplemental['Paths'])==6
    assert supplemental['MultipleEquilibria']['OptionSetCount']==6
    for filename in ['Equilibrium solution paths/equilibrium-paths-collection-manifest.json',
                     'Multiple equilibria/multiple-equilibria-exhibits.json']:
        for f in fingerprints(read(supp/filename)):check_fingerprint(f)
    supplemental_checks=0
    for p in supp.rglob('equilibrium-changes-manifest.json'):
        j=read(p);assert j['Schema']=='2'
        check_fingerprint(j['Request'])
        for f in list(fingerprints(j['Sources']))+j['OutputFingerprints']:
            check_fingerprint(f);supplemental_checks+=1
        for filename in j['OutputJsonFiles']:
            out=read(Path(filename));assert out['Schema']=='2' and out['Changes'] is not None
    # Resolve only live request input fields; recorded requests retain historical paths.
    fields={'EquilibriumFile','ActionReportFile','ProfileFile','SourceRequest','OriginalLog','InputFile',
            'NumericalResultsCsv','BaselineNumericalCsv','ExtensionNumericalCsv','IndividualDirectory'}
    def input_paths(j,parent):
        if isinstance(j,dict):
            for k,v in j.items():
                if k in fields and isinstance(v,str) and v:
                    assert (parent/v).exists(),str(parent/v)
                else:input_paths(v,parent)
        elif isinstance(j,list):
            for v in j:input_paths(v,parent)
    requests=list(supp.rglob('*.request.json'))
    for p in requests:input_paths(read(p),p.parent)
    batches=[]
    for name,count in [('CS004',114),('CS006EF',10)]:
        j=read(RESULTS/f'Run records/Retained study/{name} run manifest.json')
        assert j['Status']=='Aggregated' and j['OptionSetCount']==count and len(j['ReusedEquilibria'])==count
        assert not any('Mandatory' in x for x in j['OptionSetNames'])
        batches.append({'Batch':name,'Cases':count,'Reused':len(j['ReusedEquilibria']),'ProductionCommit':j['GitCommit']})
    summary={'RoutineExhibits':len(artifacts),'Kinds':dict(kinds),'WelfareNumericCellsVerified':numeric,
             'MainFigures':4,'MainTables':3,'PreservedSupplementalInputs':len({f['Path'] for f in fingerprints(retained_profiles)}),
             'SupplementalFingerprintsVerified':supplemental_checks,'LiveSupplementalRequestsChecked':len(requests),
             'Batches':batches,'Errors':[],
             'VisualReview':'All 193 aggregate exhibits and all seven main exhibits inspected; representative individual charts inspected. Journal manuscript/proof integration is pending.',
             'CleanRegeneration':'937 TeX sources matched across two complete generations from empty generated folders. A later targeted regeneration removed legacy titles from individual diagrams; this record hashes the final outputs.',
             'SupplementalExpansion':supplemental,
             'Scope':'Separate workflows cover 90 saved-equilibrium directed comparisons, six original exact paths and the six-case multiple-start study; their own manifests establish completion. Broader offer support and Complete Fee-Shifting finer-grid checks remain pending.'}
    write(RESULTS/'Run records/final-verification.json',summary)
    write(RESULTS/'Run records/final-artifact-hashes.json',artifacts)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compare-results',type=Path)
    verify(parser.parse_args().compare_results)
