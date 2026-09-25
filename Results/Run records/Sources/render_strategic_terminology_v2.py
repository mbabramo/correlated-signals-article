"""Create immutable terminology-only report derivatives with numeric/text checks."""
import argparse
import collections
import concurrent.futures
import copy
import os
import pathlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from article_release import ROOT,identity,read,save_new,utc,verify
from strategic_terminology import transform,validate


def numeric_tokens(text):
    return collections.Counter(re.findall(r'(?<![A-Za-z])[-+\u2212]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',text))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collection',required=True,type=pathlib.Path)
    parser.add_argument('--output',required=True,type=pathlib.Path)
    parser.add_argument('--workers',required=True,type=int)
    parser.add_argument('--reuse',type=pathlib.Path,help='Reuse only completed, hash-verified pair derivatives')
    a=parser.parse_args();collection=read(a.collection)
    if not collection.get('Passed') or not 1<=a.workers<=29:raise ValueError('Passed collection and bounded worker count required')
    output=a.output.resolve()
    if not output.is_relative_to(ROOT/'reporting'):raise ValueError('Isolated output required')
    programs={name:pathlib.Path(shutil.which(name) or '') for name in ['lualatex','pdftoppm','pdftotext']}
    if not all(p.is_file() for p in programs.values()):raise ValueError('Missing PDF compiler/inspection tools')
    output.mkdir(parents=True,exist_ok=False)
    save_new(output/'execution.json',dict(StartedUtc=utc(),Generator=identity(__file__),
        Transformation=identity(ROOT/'scripts/strategic_terminology.py'),Collection=identity(a.collection),
        Command=sys.argv,Programs={k:identity(v) for k,v in programs.items()},Workers=a.workers,
        Reservation='Must run via run_reserved_command.py with the same worker bound',
        SolvesStarted=0,ScientificCalculationsStarted=0))
    def one(file):
        original_path=verify(file);original=read(original_path)
        for f in original['Files']+original['Pages']+original['OriginalCalculationFilesUnchanged']:verify(f)
        if a.reuse:
            done=a.reuse/original['PairId']/'render-validation.json'
            if done.exists():
                prior=read(done)
                if prior['OriginalRenderManifest']!=file:raise ValueError('Different reused source report')
                validate(original,prior)
                for item in prior['Files']+prior['Pages']:verify(item)
                checks=read(verify(prior['TerminologyChecks']))
                if not checks['Passed'] or not checks['OnlyDeclaredLabelChanges']:raise ValueError('Incomplete prior terminology checks')
                for check in checks['Checks']:
                    if not check['NumericTokensIdentical'] or not check['TextWithinPageBounds']:raise ValueError('Prior rendering check failed')
                override=done.parent/'override.json'
                if read(override)!=dict(Passed=True,SupersedesForPublication=file,Validated=[identity(done)]):raise ValueError('Changed reuse override')
                return dict(PairId=original['PairId'],Changed=True,Selected=identity(done),Override=identity(override),Reused=True)
        if not any(transform(verify(x['TeX']).read_bytes())!=verify(x['TeX']).read_bytes() for x in original['Artifacts']):
            return dict(PairId=original['PairId'],Changed=False,Selected=file)
        directory=output/original['PairId'];directory.mkdir()
        updated=copy.deepcopy(original);updated['OriginalRenderManifest']=file
        updated['TerminologyGenerator']=identity(__file__);updated['CreatedUtc']=utc()
        updated['Artifacts']=[];all_commands=[];checks=[]
        def command(argv,log_path=None,environment=None):
            argv=[str(v) for v in argv];all_commands.append(argv)
            if log_path:
                with log_path.open('xb') as log:
                    subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW,env=environment)
            else:
                subprocess.run(argv,check=True,creationflags=subprocess.CREATE_NO_WINDOW,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        for artifact in original['Artifacts']:
            d=directory/artifact['Contrast']['Id'];d.mkdir()
            original_tex=verify(artifact['TeX']);tex=d/original_tex.name
            tex.write_bytes(transform(original_tex.read_bytes()))
            # The installed MiKTeX renderer successfully uses its configured cache.
            # A TEXMFCACHE override is rejected by this installation's Lua loader.
            environment=dict(os.environ)
            environment.pop('TEXMFCACHE',None)
            for pass_number in range(2):
                command([programs['lualatex'],'-interaction=nonstopmode','-halt-on-error',
                         '-output-directory='+str(d),tex],d/f'compile-{pass_number}.log',environment)
            pdf=tex.with_suffix('.pdf');pages=d/'pages';pages.mkdir()
            command([programs['pdftoppm'],'-r','130','-png',pdf,pages/'page'])
            command([programs['pdftotext'],'-layout',verify(artifact['PDF']),d/'original.txt'])
            command([programs['pdftotext'],'-layout',pdf,d/'updated.txt'])
            before=(d/'original.txt').read_text(encoding='utf-8');after=(d/'updated.txt').read_text(encoding='utf-8')
            if numeric_tokens(before)!=numeric_tokens(after):raise ValueError('Rendered numbers changed: '+artifact['Contrast']['Id'])
            command([programs['pdftotext'],'-bbox-layout',pdf,d/'bounds.xhtml'])
            tree=ET.parse(d/'bounds.xhtml');ns={'x':'http://www.w3.org/1999/xhtml'}
            page_nodes=tree.findall('.//x:page',ns)
            if not page_nodes:raise ValueError('Missing PDF geometry')
            word_count=0
            for page in page_nodes:
                width,height=float(page.get('width')),float(page.get('height'))
                for word in page.findall('.//x:word',ns):
                    word_count+=1
                    if (float(word.get('xMin'))<-.2 or float(word.get('yMin'))<-.2 or
                        float(word.get('xMax'))>width+.2 or float(word.get('yMax'))>height+.2):
                        raise ValueError('Text extends beyond PDF page: '+artifact['Contrast']['Id'])
            new=dict(artifact,TeX=identity(tex),PDF=identity(pdf),Pages=[identity(p) for p in sorted(pages.glob('page-*.png'))])
            updated['Artifacts'].append(new)
            checks.append(dict(Contrast=artifact['Contrast']['Id'],OriginalPDF=artifact['PDF'],UpdatedPDF=new['PDF'],
                NumericTokensIdentical=True,TextWithinPageBounds=True,WordsChecked=word_count,
                OriginalText=identity(d/'original.txt'),UpdatedText=identity(d/'updated.txt'),Geometry=identity(d/'bounds.xhtml'),
                CompilerEnvironmentOverride=dict(TEXMFCACHE='unset; installed MiKTeX configured cache')))
        updated['Pages']=[p for artifact in updated['Artifacts'] for p in artifact['Pages']]
        updated['Files']=[identity(p) for p in sorted(directory.rglob('*')) if p.is_file()]
        updated['VisualQAPending']=True
        validate(original,updated)
        save_new(directory/'checks.json',dict(Passed=True,Checks=checks,Commands=all_commands,
            OnlyDeclaredLabelChanges=True,OriginalManifest=file,ScientificValuesChanged=False))
        updated['TerminologyChecks']=identity(directory/'checks.json')
        binding=directory/'render-validation.json';save_new(binding,updated)
        override=directory/'override.json'
        save_new(override,dict(Passed=True,SupersedesForPublication=file,Validated=[identity(binding)]))
        return dict(PairId=original['PairId'],Changed=True,Selected=identity(binding),Override=identity(override))
    records=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(one,file) for file in collection['Validated']]
        for future in concurrent.futures.as_completed(futures):
            records.append(future.result())
            (output/'progress.json').write_text(__import__('json').dumps(dict(CompletedPairs=len(records),ExpectedPairs=len(futures))))
    records.sort(key=lambda x:x['PairId'])
    save_new(output/'result.json',dict(Schema='strategic-terminology-collection-v1',Passed=True,FinishedUtc=utc(),
        OriginalCollection=identity(a.collection),Validated=[r['Selected'] for r in records],
        Overrides=[r['Override'] for r in records if r['Changed']],ChangedPairs=sum(r['Changed'] for r in records),
        DirectedReports=2*len(records),VisualQAPending=True,Records=records,SolvesStarted=0,ScientificCalculationsStarted=0))
    print(f'{len(records)*2} reports bound to unchanged values; visual QA pending.')


if __name__=='__main__':main()
