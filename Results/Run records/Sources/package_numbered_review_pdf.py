"""Assemble the separate numbered exhibits into a bookmarked review copy.

Their original files and numbering remain separate. Raster equivalence binds
the combined pages to the explicit visual reviews without repeating them.
"""
import argparse, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from article_release import ROOT, read, verify, identity, save_new, sha, utc

OUT=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to\outputs')
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args()
source=args.source.resolve();m=read(source/'manifest.json')
qa=read(source/'visual-review.json');assert qa['Passed']
order=['Figure 1','Table 1','Figure 2','Figure 3','Figure 4','Table 2',
       'Figure 5','Figure 6','Table 3','Figure 7','Table 5','Figure 8']
pdf=args.output.resolve()
assert not pdf.exists()
writer=PdfWriter();expected=[];contents=[]
for prefix in order:
    [item]=[x for x in m['Artifacts'] if x['Title'].startswith(prefix+' -')]
    src=verify(item['PDF']);count=len(PdfReader(src).pages)
    assert count==len(item['Pages'])
    contents.append(dict(Title=item['Title'],FirstPage=len(expected)+1,Pages=count,Source=item['PDF']))
    writer.append(str(src),outline_item=item['Title']);expected.extend(item['Pages'])
writer.add_metadata({'/Title':'Article tables and figures — review copy','/Subject':'Existing numbered exhibits kept separate in the repository'})
with pdf.open('wb') as file:writer.write(file)
assert len(PdfReader(pdf).pages)==len(expected)
work=ROOT/'work'/pdf.stem;work.mkdir(exist_ok=False)
command=['pdftoppm','-r','135','-png',str(pdf),str(work/'page')]
subprocess.run(command,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
pages=sorted(work.glob('page-*.png'),key=lambda x:int(x.stem.rsplit('-',1)[1]))
assert len(pages)==len(expected)
proof=[]
for actual,old in zip(pages,expected):
    verify(old);assert sha(actual)==old['Sha256']
    proof.append(dict(Combined=identity(actual),PreviouslyReviewed=old,Identical=True))
save_new(pdf.with_name(pdf.stem+'-manifest.json'),dict(
    Schema='numbered-exhibits-review-copy-v1',Passed=True,CreatedUtc=utc(),PDF=identity(pdf),
    Contents=contents,OriginalExhibits=identity(source/'manifest.json'),VisualReview=identity(source/'visual-review.json'),
    PageEquivalenceProof=proof,RenderCommand=command,ChangesToNumberedArtifacts=False,
    Table5PendingComparisons=2,CompleteArticlePublication=False))
print(f'{len(expected)}-page review copy verified pixel-identical to the inspected exhibit pages.')
