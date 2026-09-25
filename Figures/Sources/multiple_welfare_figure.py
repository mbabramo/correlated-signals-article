"""Every accepted multiple-start welfare vector, with the article's marker style."""
import argparse, csv, math, pathlib, shutil, subprocess
from article_release import ROOT, identity, read, verify, save_new, utc
from article_presentation import PREAMBLE, compile_tex, mark

TITLE='Figure 8 - Multiple equilibrium welfare outcomes'
FIELDS=[('MeritoriousPlaintiffShortfall',r'Meritorious plaintiff\\shortfall'),
        ('NonliableDefendantBurden',r'Nonliable defendant\\burden'),
        ('LiableDefendantExcessBurden',r'Liable defendant\\excess burden'),
        ('GrossOutcomeError',r'Gross outcome\\error'),
        ('RealLitigationExpenditures',r'Real litigation\\expenditures')]
CAPTION=('Welfare outcomes for every accepted approximate profile from the four American/British searches. '
         'Panels distinguish risk neutrality and symmetric risk aversion; columns are the five welfare measures. '
         'Rows identify starting profiles, not matched equilibria or an equilibrium ranking. Repeated outcomes remain separate. '
         '199 of 200 starts were accepted; British risk-averse start 12 was not accepted and is omitted. '
         'Scales match across risk panels within each measure. The underlying full profiles, acceptance criteria and disposition ranges remain in the Multiple equilibria supplement.')

def generate(out, write_manifest=True):
    source=ROOT/'reporting/approximate-stable-200-grouping-v1/catalog.json'
    catalog=read(source);rows=[]
    for a in catalog['Attempts']:
        if not a['Accepted']:continue
        data=read(verify(a['Result']));assert data['Validation']['Passed']
        parts=a['Case'].split('__')
        rows.append(dict(Risk=parts[3],Rule=parts[2],Start=a['StartIndex'],AverageGain=a['AverageGain'],**data['Validation']['Welfare']['Headline']))
    assert len(rows)==199 and len({(r['Risk'],r['Rule'],r['Start']) for r in rows})==199
    prior=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to\outputs\Multiple-equilibrium-outcome-diagram-British\all-outcomes.csv')
    previous=list(csv.DictReader(prior.open(encoding='utf-8-sig')))
    key=lambda r:(r['Risk'],r['Rule'],int(r['Start']))
    assert len(previous)==len(rows)
    for a,b in zip(sorted(rows,key=key),sorted(previous,key=key)):
        assert key(a)==key(b)
        for k in [f[0] for f in FIELDS]+['AverageGain']:assert a[k]==float(b[k])
    (out/'Figures/Sources').mkdir(parents=True,exist_ok=True)
    bounds={f:math.ceil(max(r[f] for r in rows)*1.04/.05)*.05 for f,_ in FIELDS}
    lines=[r'\begin{tikzpicture}[font=\small]'];points=[]
    for i,risk in enumerate(('rn','ra')):
        top=18.0-i*9.5;bottom=top-6.7
        lines.append(f'\\node[anchor=west,font=\\bfseries] at (.7,{top+1.45}) {{'+('Risk neutral' if risk=='rn' else 'Risk averse')+'};')
        for j,(field,label) in enumerate(FIELDS):
            x0=.85+j*3.35;width=2.72;bound=bounds[field]
            lines.append(f'\\node[align=center,anchor=south] at ({x0+width/2},{top+.25}) {{{label}}};')
            for idx in (0,10,20,30,40,49):
                y=top-6.7*(idx+.5)/50
                lines.append(f'\\draw[black!12] ({x0},{y})--({x0+width},{y});')
                if j==0:lines.append(f'\\node[anchor=east,font=\\footnotesize] at ({x0-.1},{y}) {{{idx}}};')
            for frac in (0,.5,1):
                x=x0+width*frac
                lines.append(f'\\draw[black!10] ({x},{bottom})--({x},{top});')
                anchor={0:'north west',.5:'north',1:'north east'}[frac]
                lines.append(f'\\node[anchor={anchor},font=\\footnotesize,inner xsep=0pt] at ({x},{bottom-.08}) {{{bound*frac:.3f}'.rstrip('0').rstrip('.')+'};')
            lines.append(f'\\draw ({x0},{top})--({x0},{bottom})--({x0+width},{bottom});')
            for rule in ('american','complete'):
                selected=sorted((r for r in rows if r['Risk']==risk and r['Rule']==rule),key=lambda r:r['Start'])
                assert len(selected)==(49 if (risk,rule)==('ra','complete') else 50)
                for r in selected:
                    x=x0+width*r[field]/bound;y=top-6.7*(r['Start']+.5)/50
                    lines.append(mark(x,y,rule,diameter=2.6))
                    points.append(dict(Risk=risk,Rule=rule,Start=r['Start'],Measure=field,Value=r[field],X=x,Y=y))
        lines.append(f'\\node[rotate=90] at (-.12,{top-3.35}) {{Start index}};')
    lines += [mark(5.5,.25,'american',diameter=3.5),r'\node[anchor=west] at (5.85,.25) {American};',
              mark(10,.25,'complete',diameter=3.5),r'\node[anchor=west] at (10.3,.25) {British};',r'\end{tikzpicture}']
    assert len(points)==995
    pdf=compile_tex(out,'Figures',TITLE,PREAMBLE+'\n'.join(lines)+r'\end{document}')
    stem=out/'Figures/Sources'/TITLE
    save_new(stem.with_suffix('.json'),dict(CreatedUtc=utc(),Catalog=identity(source),PriorValues=identity(prior),Rows=rows,PlottedPoints=points,AxisMaxima=bounds,
        AcceptedProfiles=199,AttemptedStarts=200,Rejected=[dict(Risk='ra',Rule='complete',Start=12)],ExactEqualityWithEarlierPlot=True,NoAveragingOrGrouping=True,Replaces='Table 6 - Disposition ranges'))
    with stem.with_suffix('.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    stem.with_suffix('.txt').write_text(CAPTION+'\n',encoding='utf-8')
    for filename in ('multiple_welfare_figure.py','article_presentation.py'):
        shutil.copy2(ROOT/'scripts'/filename,out/'Figures/Sources'/filename)
    subprocess.run(['pdftoppm','-scale-to','1800','-singlefile','-png',str(pdf),str(out/'Figures'/TITLE)],check=True,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    manifest=dict(CreatedUtc=utc(),Generator=identity(out/'Figures/Sources/multiple_welfare_figure.py'),PDF=identity(pdf),Preview=identity(out/'Figures'/(TITLE+'.png')),Data=identity(stem.with_suffix('.json')),CSV=identity(stem.with_suffix('.csv')),Caption=identity(stem.with_suffix('.txt')),SolvesStarted=0,VisualReviewPending=True)
    if write_manifest:save_new(out/'manifest.json',manifest)
    print('Figure 8: 995 points from 199 accepted profiles, exactly matching the earlier plot.')
    return dict(Title=TITLE,Folder='Figures',PDF=manifest['PDF'],Data=manifest['Data'],Caption=manifest['Caption'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False);generate(a.output)
