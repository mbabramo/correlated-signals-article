"""Preserve exact inputs to separate analyses, then rebase their requests/manifests.

This script copies and rewrites files; filesystem removal/moves are performed by
the explicit, path-checked PowerShell import script.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPP = ROOT / 'Supplemental materials'
MECHANISMS = SUPP / 'Equilibrium strategy changes'
RECORD = MECHANISMS / 'Sources/relocation.json'
RENAMES = {
    ROOT / 'Results/Equilibrium diagnostics': MECHANISMS / 'Calculations',
    ROOT / 'Tables/Equilibrium strategy changes': MECHANISMS / 'Published source tables',
    SUPP / 'Fee shifting on exit/Equilibrium strategy changes': MECHANISMS / 'Fee trigger comparison',
}

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def capture():
    mapping = {str(k): str(v) for k, v in RENAMES.items()}
    originals = []
    profiles = MECHANISMS / 'Sources/Profiles'
    def preserve(path):
        path = Path(path)
        if not path.is_file():
            return
        if path.suffix == '.csv' and ('-equ.csv' in path.name or '-InformationSetActions.csv' in path.name):
            target = profiles / path.name
        else:
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and sha(target) != sha(path):
            raise ValueError(f'Conflicting supplemental source: {target}')
        shutil.copy2(path, target)
        mapping[str(path.resolve())] = str(target)
        originals.append({'Path': str(target), 'OriginalPath': str(path), 'Sha256': sha(path)})
    def scan(value):
        if isinstance(value, dict):
            if 'Path' in value and 'Sha256' in value:
                preserve(value['Path'])
            for v in value.values(): scan(v)
        elif isinstance(value, list):
            for v in value: scan(v)
    for directory in [ROOT / 'Results/Equilibrium diagnostics', SUPP / 'Fee shifting on exit/Equilibrium strategy changes']:
        for path in directory.rglob('*manifest.json'):
            scan(read(path))
    request_path = SUPP / 'Equilibrium solution paths/equilibrium-paths.request.json'
    for selection in read(request_path)['Equilibria']:
        old = (request_path.parent / selection['OriginalLog']).resolve()
        local = ROOT / 'Results/Individual simulations' / old.name
        if not local.is_file(): raise FileNotFoundError(local)
        target = SUPP / 'Equilibrium solution paths/Sources/Original solve logs' / old.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local, target)
        mapping[str(old)] = str(target)
        originals.append({'Path': str(target), 'OriginalPath': str(old), 'Sha256': sha(local)})
    write(RECORD, {'Description': 'Exact source profiles/action reports and original solve logs needed by retained separate workflows; no numerical analysis was changed.',
                   'Checkpoint': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                   'Mappings': mapping, 'PreservedInputs': originals})
    print(f'Preserved {len({x["Path"] for x in originals})} exact source files.')

def rebase():
    record = read(RECORD)
    if record.get('Completed'):
        for source in record['PreservedInputs']: assert sha(Path(source['Path'])) == source['Sha256']
        print('Supplemental requests already rebased; source hashes verified.')
        return
    mappings = sorted(record['Mappings'].items(), key=lambda kv: -len(kv[0]))
    def mapped(value):
        normalized = os.path.normpath(value)
        for old, new in mappings:
            if normalized.lower() == old.lower(): return new
            if normalized.lower().startswith(old.lower() + os.sep):
                return new + normalized[len(old):]
        return value
    def old_parent(path):
        for old, new in RENAMES.items():
            try: return old / path.parent.relative_to(new)
            except ValueError: pass
        return path.parent
    # An interrupted relocation may already have written some requests. Restore
    # the checkpointed versions before applying the path-only transformation.
    checkpoint=record.get('Checkpoint','HEAD')
    for path in SUPP.rglob('*.request.json'):
        previous=old_parent(path)/path.name
        relative=previous.relative_to(ROOT).as_posix()
        original=subprocess.run(['git','show',checkpoint+':'+relative],cwd=ROOT,capture_output=True)
        if original.returncode==0:path.write_bytes(original.stdout)
    changed = []
    path_keys = {'EquilibriumFile','ActionReportFile','SourceRequest','OriginalLog','OutputDirectory',
                 'PublicationDirectory','OutputPrefix','InputFile','NumericalResultsCsv','BaselineNumericalCsv',
                 'ExtensionNumericalCsv','IndividualDirectory'}
    def request_values(value, before, after):
        if isinstance(value, dict):
            return {k: (os.path.relpath(mapped(str((before / v).resolve())), after).replace('\\','/')
                         if k in path_keys and isinstance(v,str) and v else request_values(v,before,after))
                    for k,v in value.items()}
        if isinstance(value,list): return [request_values(v,before,after) for v in value]
        return mapped(value) if isinstance(value,str) and os.path.isabs(value) else value
    for path in SUPP.rglob('*.request.json'):
        before_hash = sha(path)
        old = read(path)
        new = request_values(old, old_parent(path), path.parent)
        if new != old:
            write(path,new)
            changed.append({'Path':str(path),'PreviousSha256':before_hash,'Sha256':sha(path)})
    def manifest_values(value):
        if isinstance(value,dict):
            result = {k:manifest_values(v) for k,v in value.items()}
            if ('Path' in result and 'Sha256' in result and Path(result['Path']).is_file()
                and Path(result['Path']).suffix.lower() not in {'.dll','.exe'}):
                actual = sha(Path(result['Path']))
                if actual.lower() != result['Sha256'].lower():
                    if not any(c['Path'] == result['Path'] for c in changed):
                        raise ValueError(f'Unexpected changed analysis/input: {result["Path"]}')
                    result['Sha256'] = actual
            return result
        if isinstance(value,list):return [manifest_values(v) for v in value]
        return mapped(value) if isinstance(value,str) and os.path.isabs(value) else value
    for path in SUPP.rglob('*manifest.json'):
        old=read(path);new=manifest_values(old)
        if old!=new:write(path,new)
    record['RebasedRequests']=changed
    record['Completed']=True
    write(RECORD,record)
    for source in record['PreservedInputs']:
        assert sha(Path(source['Path'])) == source['Sha256']
    print(f'Rebased {len(changed)} live requests; preserved calculation and input hashes.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['capture','rebase'])
    phase=parser.parse_args().phase
    capture() if phase=='capture' else rebase()
