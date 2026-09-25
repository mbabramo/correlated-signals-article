"""Generate full-precision baseline welfare tables and signed-comparison plots.

Partial coverage is explicit. There is no averaging of profiles/specifications and
no welfare index or aggregation of the five distinct established measures.
"""
import argparse
import math
import pathlib
import shutil
import subprocess
import sys
from article_release import ROOT,identity,read,save_new,utc,verify
from individual_strategy_sources import tex
from resource_accounting import nonreporting_reservations

FIELDS=[('MeritoriousPlaintiffShortfall','Meritorious plaintiff shortfall','P shortfall'),
        ('NonliableDefendantBurden','Nonliable defendant burden','D nonliable'),
        ('LiableDefendantExcessBurden','Liable defendant excess burden','D liable excess'),
        ('GrossOutcomeError','Gross outcome error','Gross error'),
        ('RealLitigationExpenditures','Real litigation expenditures','Real costs')]

def number(v):
    if not math.isfinite(v):raise ValueError('Nonfinite welfare value')
    return ('0.000'+(r'$^{\dagger}$' if v!=0 else '')) if abs(v)<.0005 else f'{v:.3f}'

def risk(p):
    if p['AlphaP']==p['AlphaD']==0:return 'RN'
    if p['AlphaP']==p['AlphaD']:return f'RA ({p["AlphaP"]:g})'
    return f'P {p["AlphaP"]:g}, D {p["AlphaD"]:g}'

def specification(p):
    family='Baseline' if p['IsExternalImport'] else p['Family']+' / '+p['Variant']
    return family+'; cost '+f'{p["CostMultiplier"]:g}'

def build(catalog_path,welfare_wave,output,article_selection=False):
    catalog_path,welfare_wave,output=[pathlib.Path(p).resolve() for p in (catalog_path,welfare_wave,output)]
    if not output.is_relative_to(ROOT/'reporting'):raise ValueError('Isolated reporting output required')
    catalog=read(catalog_path);wave=read(welfare_wave)
    if wave['Passed'] is not True or wave['AlternativeTruthMapsIncluded'] is not False:raise ValueError('Expected validated baseline decompositions')
    for f in catalog['Outputs']:verify(f)
    calculations=[]
    for validation in wave['Validated']:
        v=read(verify(validation))
        if v['Passed'] is not True:raise ValueError('Unvalidated decomposition')
        for f in v['Outputs']:verify(f)
        d=read(pathlib.Path(validation['Path']).parent/'decomposition.json')
        calculations.append(dict(Validation=validation,Id=d['Id'],Components=d['Components']))
    data=read(catalog_path.parent/'welfare-levels-and-differences.json');cases={c['CaseId']:c for c in catalog['Cases']}
    rows=sorted(cases.values(),key=lambda c:(specification(c['Parameters']),risk(c['Parameters']),c['Parameters']['FeeRule']))
    if article_selection:
        rows=[c for c in rows if c['Parameters']['FeeRule']!='trial-only' or c['Parameters']['CostMultiplier']==1]
    expected_primary=74 if article_selection else 82
    comparisons=[]
    for index,pair in enumerate(sorted(data['SignedFeeComparisons'],key=lambda p:p['American']),1):
        calc=next(c for c in calculations if c['Id']==pair['American']+'--to--'+pair['Complete'])
        comparisons.append(dict(Code=f'C{index:02}',**pair,Decomposition=calc))
    if len(comparisons)!=wave['CompletedPairs']:raise ValueError('Catalog and decomposition coverage differ')
    output.mkdir(parents=True,exist_ok=False);sources=output/'Sources';sources.mkdir()
    save_new(sources/'welfare-data.json',dict(Schema='baseline-welfare-overview-v1',CreatedUtc=utc(),
        Catalog=identity(catalog_path),WelfareWave=identity(welfare_wave),Cases=rows,Comparisons=comparisons,
        PendingPrimary=catalog['MissingAuditedCaseIds'],PendingFeeComparisons=data['PendingFeeComparisons'],
        Units='Damages = 1; population weighting over potential disputes',DisplayDecimals=3,
        Difference='British minus American, calculated before rounding',NoCombinedWelfareIndex=True,
        TruthMapping='Identity only; alternative strengths unresolved',ArticleSelection=article_selection,ExpectedPrimary=expected_primary,Complete=len(rows)==expected_primary))
    for name in ('welfare_overview.py','individual_strategy_sources.py','article_release.py','resource_accounting.py'):
        shutil.copy2(ROOT/'scripts'/name,sources/name)
    lines=[r'\documentclass[10pt]{article}',r'\usepackage[paperwidth=11in,paperheight=8.5in,margin=.45in,footskip=16pt]{geometry}',
        r'\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{booktabs,longtable,array,pgfplots}',
        r'\pgfplotsset{compat=1.18}\setlength{\parindent}{0pt}',r'\begin{document}',
        r'{\LARGE\bfseries Baseline welfare: completed primary profiles}\par\medskip',
        tex(f'Coverage: {len(rows)} of {expected_primary} article-selected primary cases; {len(comparisons)} of 36 American/British comparisons. Pending cases are listed in the source data.')+r'\par\smallskip',
        r'These are five separate monetary measures, in damages units and weighted over potential disputes. They do not form an additive welfare index. '+
        r'The truth relationship is the baseline identity map. Alternative truth assumptions are not included.\par\smallskip',
        r'RN denotes risk neutrality; RA denotes symmetric CARA risk aversion (alpha in parentheses). Asymmetric cases state each party\textquotesingle s alpha. '+
        r'American and British are the main rules. Trial-only fee shifting appears as a separate ordinary-cost extension.\par\smallskip',
        r'Levels use the established truth-prior weighting of truth-conditional outcomes; direct replay truth mass is retained separately in the source catalog. '+
        r'Values are displayed to three decimals; calculations and comparisons use unrounded data. $\dagger$ marks a nonzero value that rounds to zero.\par\medskip',
        r'\small\setlength{\tabcolsep}{4pt}',
        r'\begin{longtable}{@{}p{3.0in}llrrrrr@{}}',
        r'\toprule Specification & Risk & Fee & P shortfall & D nonliable & D liable excess & Gross error & Real costs\\\midrule\endfirsthead',
        r'\toprule Specification & Risk & Fee & P shortfall & D nonliable & D liable excess & Gross error & Real costs\\\midrule\endhead',
        r'\bottomrule\endfoot']
    for c in rows:
        p=c['Parameters'];level=c['Welfare']['Headline']
        lines.append(' & '.join([tex(specification(p)),tex(risk(p)),tex({'complete':'British','american':'American','trial-only':'Trial only'}[p['FeeRule']])]+[number(level[f]) for f,_,_ in FIELDS])+r'\\')
    lines += [r'\end{longtable}\normalsize',r'\newpage',r'{\LARGE\bfseries Matched fee comparisons}\par\medskip',
        r'Every difference is British minus American under the same specification, costs and risk preferences. '+
        r'Signed magnitudes are shown without combining unlike cases or interpreting their frequency as a probability. '+
        r'Each listed pair has passed the four-corner rule/behavior decomposition and complete endpoint checks.\par\medskip',
        r'\small\begin{longtable}{@{}lp{3.0in}lrrrrr@{}}',
        r'\toprule Code & Specification & Risk & P shortfall & D nonliable & D liable excess & Gross error & Real costs\\\midrule\endfirsthead',
        r'\toprule Code & Specification & Risk & P shortfall & D nonliable & D liable excess & Gross error & Real costs\\\midrule\endhead',
        r'\bottomrule\endfoot']
    for c in comparisons:
        p=cases[c['American']]['Parameters']
        lines.append(' & '.join([c['Code'],tex(specification(p)),tex(risk(p))]+[number(c['CompleteMinusAmerican'][f]) for f,_,_ in FIELDS])+r'\\')
    lines += [r'\end{longtable}\normalsize']
    for field,label,_ in FIELDS:
        values=[c['CompleteMinusAmerican'][field] for c in comparisons]
        bound=max(.002,max(abs(v) for v in values)*1.3)
        tick=10**math.floor(math.log10(bound/3))
        tick=max(.001,next(f*tick for f in (1,2,5,10) if f*tick>=bound/3))
        bound=math.ceil(bound/tick)*tick
        ticks=[i*tick for i in range(-math.floor(bound/tick),math.floor(bound/tick)+1)]
        lines += [r'\newpage',r'{\LARGE\bfseries '+tex(label)+r'}\par\smallskip',
            r'British minus American, using unrounded values. Codes identify the preceding matched-comparison table. '+
            r'Blue: negative; orange: positive. This is one monetary measure, not a combined policy ranking.\par\medskip',
            r'\begin{center}\begin{tikzpicture}\begin{axis}[width=9.7in,height=6.25in,',
            f'xmin={-bound:.17g},xmax={bound:.17g},ymin=.5,ymax={len(comparisons)+.5},y dir=reverse,',
            'ytick={'+','.join(str(i) for i in range(1,len(comparisons)+1))+'},',
            'yticklabels={'+','.join(c['Code'] for c in comparisons)+'},',
            'xtick={'+','.join(f'{v:.17g}' for v in ticks)+'},',
            r'xticklabel style={/pgf/number format/fixed,/pgf/number format/precision=3,/pgf/number format/fixed zerofill},',
            r'xlabel={Difference in damages units},ylabel={Matched comparison},grid=major,clip=false]',
            r'\addplot[gray,thin] coordinates {(0,.5) (0,'+str(len(comparisons)+.5)+')};']
        for i,v in enumerate(values,1):
            color='blue!65!black' if v<0 else 'orange!85!black' if v>0 else 'black'
            lines.append(r'\addplot[only marks,mark=*,mark size=2.2pt,color='+color+f'] coordinates {{({v:.17g},{i})}};')
            anchor='west' if v>=0 else 'east';sign=1 if v>=0 else -1
            lines.append(r'\node[font=\small,anchor='+anchor+f'] at (axis cs:{v+sign*bound*.016:.17g},{i}) {{{number(v)}}};')
        lines += [r'\end{axis}\end{tikzpicture}\end{center}']
    lines.append(r'\end{document}');(sources/'welfare-overview.tex').write_text('\n'.join(lines),encoding='utf-8')
    resource=nonreporting_reservations();reserved=resource['Total']
    for p in (ROOT/'reporting').glob('*-worker.json'):
        if not (r:=read(p)).get('FinishedUtc'):reserved+=r['ComputeWorkers']
    if reserved+1>32:raise ValueError('No capacity to render overview')
    def command(name,argv):
        subprocess.run([sys.executable,str(ROOT/'scripts/run_recorded.py'),output.name+'-'+name,*argv],cwd=ROOT,check=True)
    command('pdf',['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(output),str(sources/'welfare-overview.tex')])
    command('pdf-pass2',['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(output),str(sources/'welfare-overview.tex')])
    png=ROOT/'work'/output.name;png.mkdir(exist_ok=False)
    command('png',['pdftoppm','-r','130','-png',str(output/'welfare-overview.pdf'),str(png/'page')])
    save_new(output/'manifest.json',dict(Schema='baseline-welfare-overview-exhibit-v1',CreatedUtc=utc(),
        Catalog=identity(catalog_path),WelfareWave=identity(welfare_wave),Cases=len(rows),Comparisons=len(comparisons),
        ExpectedPrimary=expected_primary,ArticleSelection=article_selection,ExpectedComparisons=36,Complete=False,AlternativeTruthMapsIncluded=False,
        PDF=identity(output/'welfare-overview.pdf'),Pages=[identity(p) for p in sorted(png.glob('page-*.png'))],
        Sources=[identity(p) for p in sorted(sources.iterdir())],OtherComputeReservations=reserved,VisualQAPending=True,SolvesStarted=0))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--catalog',required=True);p.add_argument('--welfare-wave',required=True);p.add_argument('--output',required=True);p.add_argument('--article-selection',action='store_true')
    a=p.parse_args();build(a.catalog,a.welfare_wave,a.output,a.article_selection)
