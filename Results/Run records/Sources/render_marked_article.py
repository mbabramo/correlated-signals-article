"""Build the marked manuscript only in its isolated review directory."""
import os, pathlib, re, subprocess
from article_release import ROOT, identity, save_new, utc, read
work=ROOT/'work/manuscript-marked-20260925-v3';cwd=work/'Article and bibliography'
commands=[]
for n,cmd in enumerate([
 ['lualatex','-interaction=nonstopmode','-halt-on-error','corr_signals.tex'],
 ['bibtex','corr_signals'],
 ['lualatex','-interaction=nonstopmode','-halt-on-error','corr_signals.tex'],
 ['lualatex','-interaction=nonstopmode','-halt-on-error','corr_signals.tex']]):
    with (work/f'build-{n+1}.log').open('wb') as log:
        p=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    commands.append(dict(Command=cmd,WorkingDirectory=str(cwd),ExitCode=p.returncode,Log=identity(work/f'build-{n+1}.log')))
    if p.returncode:raise RuntimeError(f'Compilation failed: {cmd}; see build-{n+1}.log')
import pdfplumber
pdf=cwd/'corr_signals.pdf'
with pdfplumber.open(pdf) as doc:
    pages=[dict(Page=i+1,Width=p.width,Height=p.height,Characters=len(p.chars)) for i,p in enumerate(doc.pages)]
    text='\n'.join(p.extract_text() or '' for p in doc.pages)
    expected=len(read(work/'manuscript-change-log.json')['EditorialFlags'])
    assert len(re.findall(r'\[Update\s*needed:',text))==expected
    assert 'Figure 7:' in text and 'Table 5:' in text and 'Table 6:' in text
    assert 'Table 4:' not in text
    assert not any('??' in (p.extract_text() or '') for p in doc.pages)
    (work/'rendered-text.txt').write_text(text,encoding='utf-8')
save_new(work/'build-validation.json',dict(Passed=True,CreatedUtc=utc(),Commands=commands,PDF=identity(pdf),Source=identity(cwd/'corr_signals.tex'),Pages=pages,VisualReviewPending=True))
previews=work/'review-pages';previews.mkdir(exist_ok=False)
cmd=['pdftoppm','-r','85','-png',str(pdf),str(previews/'page')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
print(f'Manuscript compiled with all exhibit pages; {len(pages)} pages rendered for visual review.')
