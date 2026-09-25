"""Create an immutable typography-only derivative of one strategic report pair.

Run through run_reserved_command.py with one worker. The only permitted TeX
changes are payoff-table row spacing, line leading and optional table gaps. Scientific files,
table contents, font sizes and original render artifacts stay unchanged.
"""
import argparse, copy, pathlib, subprocess, sys
from article_release import ROOT, identity, read, save_new, utc, verify

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--collection', required=True, type=pathlib.Path)
p.add_argument('--pair', required=True)
p.add_argument('--direction', required=True, choices=['forward','reverse'])
p.add_argument('--output', required=True, type=pathlib.Path)
p.add_argument('--reason', required=True)
p.add_argument('--row-spacing', type=float, default=1)
p.add_argument('--line-leading', type=float, default=10)
p.add_argument('--compact-table-gaps', action='store_true')
a=p.parse_args()
collection_path=a.collection.resolve(); collection=read(collection_path)
if collection.get('Passed') is not True: raise ValueError('Unvalidated collection')
matches=[(f,read(verify(f))) for f in collection['Validated'] if read(verify(f))['PairId']==a.pair]
if len(matches)!=1: raise ValueError('Pair is not unique')
original_manifest, original=matches[0]
if original.get('Passed') is not True: raise ValueError('Unvalidated render')
for f in original['Files']+original['Pages']: verify(f)
selected=[x for x in original['Artifacts'] if x['Contrast']['Id'].endswith('-'+a.direction)]
if len(selected)!=1: raise ValueError('Direction is not unique')
artifact=selected[0]; source=verify(artifact['TeX']); before=source.read_bytes()
if not 0 <= a.row_spacing <= 3 or not 9 <= a.line_leading <= 11:
    raise ValueError('Typography adjustment outside legible bounds')
old=rb'\\[3pt]'; new=('\\\\['+format(a.row_spacing,'g')+'pt]').encode()
if not before.count(old) or new in before: raise ValueError('Unexpected row spacing source')
after=before.replace(old,new)
old_font=rb'{\small\setlength{\tabcolsep}{3pt}\begin{longtable}'
new_font=(r'{\fontsize{9}{'+format(a.line_leading,'g')+r'}\selectfont\setlength{\tabcolsep}{3pt}\begin{longtable}').encode()
if a.compact_table_gaps:
    new_font=new_font.replace(rb'\begin{longtable}',rb'\setlength{\LTpre}{3pt}\setlength{\LTpost}{3pt}\begin{longtable}')
if after.count(old_font)!=1 or new_font in before: raise ValueError('Unexpected payoff table font source')
after=after.replace(old_font,new_font)
if after.replace(new_font,old_font).replace(new,old)!=before: raise ValueError('Content changed beyond typography')
output=a.output.resolve()
if not output.is_relative_to(ROOT/'reporting'): raise ValueError('Keep derivative isolated')
output.mkdir(parents=True,exist_ok=False)
save_new(output/'rejected-visual-qa.json',dict(Schema='page-by-page-visual-qa-v1',Passed=False,
    RecordedUtc=utc(),PairId=a.pair,SourceManifest=original_manifest,
    PDFs=[x['PDF'] for x in original['Artifacts']],Pages=original['Pages'],Reason=a.reason,
    InspectionMethod='Every original pair page was opened with view_image and inspected.'))
tex=output/source.name; tex.write_bytes(after)
save_new(output/'layout-change.json',dict(Schema='strategic-typography-derivative-v1',CreatedUtc=utc(),
    OriginalCollection=identity(collection_path),OriginalManifest=original_manifest,OriginalTeX=identity(source),
    RevisedTeX=identity(tex),Generator=identity(__file__),Command=sys.argv,Reason=a.reason,
    Replacements=before.count(old),BeforeRowSpacingPoints=3,AfterRowSpacingPoints=a.row_spacing,
    PayoffFontSizePoints=9,PayoffLineLeadingPoints=a.line_leading,
    CompactTableGaps=a.compact_table_gaps,
    InverseTransformationByteIdentical=True,ScientificCalculationsStarted=0,SolvesStarted=0))
shutil_source=output/'strategic_layout_fix.py'; shutil_source.write_bytes(pathlib.Path(__file__).read_bytes())

def run(name,argv):
    child=subprocess.run([sys.executable,str(ROOT/'scripts/run_recorded.py'),output.name+'-'+name,*argv],cwd=ROOT)
    if child.returncode: raise RuntimeError('Rendering failed: '+name)

for n in (1,2): run('tex-'+str(n),['lualatex','-interaction=nonstopmode','-halt-on-error',
    '-output-directory='+str(output),str(tex)])
pdf=tex.with_suffix('.pdf'); png=output/'pages'; png.mkdir()
run('png',['pdftoppm','-r','130','-png',str(pdf),str(png/'page')])
pages=[identity(x) for x in sorted(png.glob('page-*.png'),key=lambda x:int(x.stem.rsplit('-',1)[1]))]
if not pages: raise ValueError('No pages')
for f in original['Files']+original['Pages']: verify(f)
revised=copy.deepcopy(original)
changed=[x for x in revised['Artifacts'] if x['Contrast']['Id']==artifact['Contrast']['Id']][0]
changed.update(TeX=identity(tex),PDF=identity(pdf),Pages=pages,VisualQAPending=True)
revised.update(FinishedUtc=utc(),OriginalRenderManifest=original_manifest,LayoutAdjustment=identity(output/'layout-change.json'),
    Pages=[f for x in revised['Artifacts'] for f in x['Pages']],
    Files=[identity(x) for x in sorted(output.rglob('*')) if x.is_file()],VisualQAPending=True)
manifest=output/'render-validation.json'; save_new(manifest,revised)
scientific_collection=collection
while 'Wave' not in scientific_collection or 'Build' not in scientific_collection:
    scientific_collection=read(verify(scientific_collection['OriginalCollection']))
save_new(output/'result.json',dict(Schema='strategic-render-collection-v1',Passed=True,FinishedUtc=utc(),
    Validated=[identity(manifest)],DirectedReports=2,Wave=scientific_collection['Wave'],Build=scientific_collection['Build'],
    VisualQAPending=True,Complete=False,SolvesStarted=0,ScientificCalculationsStarted=0,
    SupersedesForPublication=original_manifest))
print('Created typography derivative; all pages still require visual review.')
