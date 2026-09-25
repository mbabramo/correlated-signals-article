"""Five separate four-corner welfare decomposition tables from validated calculations."""
import argparse,pathlib,shutil,subprocess,sys
from article_release import ROOT,identity,read,save_new,utc,verify
from build_profile_catalog import close
from individual_strategy_sources import tex,printed
from welfare_overview import FIELDS,specification,risk

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--overview',required=True,type=pathlib.Path);p.add_argument('--output',required=True,type=pathlib.Path);a=p.parse_args()
overview_path,output=a.overview.resolve(),a.output.resolve();overview=read(overview_path)
if not output.is_relative_to(ROOT/'reporting'):raise ValueError('Isolated output required')
for f in overview['Sources']:verify(f)
data=read(overview_path.parent/'Sources/welfare-data.json');pairs=data['Comparisons'];cases={c['CaseId']:c for c in data['Cases']}
for pair in pairs:
    validation=read(verify(pair['Decomposition']['Validation']))
    if not validation['Passed']:raise ValueError('Unvalidated welfare pair')
    for f in validation['Outputs']:verify(f)
    for field,label,_ in FIELDS:
        c=pair['Decomposition']['Components'][label]
        aa,ca,ac,cc=[c[k] for k in ('AmericanWithAmericanProfile','CompleteWithAmericanProfile','AmericanWithCompleteProfile','CompleteWithCompleteProfile')]
        close((ca-aa+cc-ac)/2,c['MechanicalRuleEffect'],'symmetric mechanical rule effect')
        close((ac-aa+cc-ca)/2,c['BehavioralEffect'],'symmetric behavioral effect')
        close(cc-aa,c['TotalDifference'],'endpoint difference')
        close(c['MechanicalRuleEffect']+c['BehavioralEffect'],c['TotalDifference'],'decomposition identity')
        close(c['TotalDifference'],pair['CompleteMinusAmerican'][field],'overview difference identity')
output.mkdir(parents=True,exist_ok=False);sources=output/'Sources';sources.mkdir()
save_new(sources/'decomposition-exhibit-data.json',dict(Schema='four-corner-welfare-exhibit-data-v1',CreatedUtc=utc(),Overview=identity(overview_path),
    Comparisons=pairs,Cases=cases,ExpectedComparisons=36,Complete=len(pairs)==36,TruthMapping='identity',
    Definition='Symmetric average over the two possible orders of replacing the fee rule and the full equilibrium profile. Five separate monetary measures; no combined index.'))
lines=[r'\documentclass[10pt]{article}',r'\usepackage[paperwidth=11in,paperheight=8.5in,margin=.5in,footskip=16pt]{geometry}',
    r'\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{booktabs,longtable,array,amsmath}',r'\setlength{\parindent}{0pt}\begin{document}',
    r'{\LARGE\bfseries Welfare decompositions: rule and behavior}\par\medskip',
    tex(f'{len(pairs)} of 36 American/British pairs are available. Each pair uses independently audited full profiles, including agreement and off-path actions. Alternative truth maps are not included.')+r'\par\smallskip',
    r'Write $W_{rs}$ for welfare evaluated under rule $r$ with the complete profile solved under rule $s$; $A$ denotes American and $C$ denotes British. '+
    r'The mixed corners are evaluations of fixed profiles, not new equilibria. The two effects average the two replacement orders:\par',
    r'\[R=\tfrac12[(W_{CA}-W_{AA})+(W_{CC}-W_{AC})],\qquad B=\tfrac12[(W_{AC}-W_{AA})+(W_{CC}-W_{CA})].\]',
    r'The signed total is $\Delta=W_{CC}-W_{AA}=R+B$. No equilibrium-selection inference follows from this accounting decomposition. '+
    r'All five measures use their existing monetary definitions and population weighting. They are not combined.\par\medskip',
    r'\small\begin{longtable}{@{}lp{5.4in}l@{}}\toprule Code & Matched specification and cost & Risk\\\midrule\endfirsthead',
    r'\toprule Code & Matched specification and cost & Risk\\\midrule\endhead\bottomrule\endfoot']
for pair in pairs:
    c=cases[pair['American']]['Parameters'];lines.append(' & '.join([tex(pair['Code']),tex(specification(c)),tex(risk(c))])+r'\\')
lines.append(r'\end{longtable}\normalsize')
for field,label,_ in FIELDS:
    lines += [r'\newpage',r'{\LARGE\bfseries '+tex(label)+r'}\par\medskip',
        r'Each row is one matched American/British comparison from the preceding key. Monetary units are damages = 1. '+
        r'$R$ is the mechanical rule effect; $B$ the behavioral effect; $\Delta$ British minus American. '+
        r'Four significant figures are shown; all calculations use the retained unrounded corners. Tiny nonzero residuals are printed, not clipped.\par\medskip',
        r'\small\setlength{\tabcolsep}{6pt}\begin{longtable}{@{}lrrrrrrrr@{}}',
        r'\toprule Code & $W_{AA}$ & $W_{CA}$ & $W_{AC}$ & $W_{CC}$ & $R$ & $B$ & $\Delta$ & Residual\\\midrule\endfirsthead',
        r'\toprule Code & $W_{AA}$ & $W_{CA}$ & $W_{AC}$ & $W_{CC}$ & $R$ & $B$ & $\Delta$ & Residual\\\midrule\endhead\bottomrule\endfoot']
    for pair in pairs:
        c=pair['Decomposition']['Components'][label]
        lines.append(' & '.join([tex(pair['Code'])]+[tex(printed(c[k])) for k in (
            'AmericanWithAmericanProfile','CompleteWithAmericanProfile','AmericanWithCompleteProfile','CompleteWithCompleteProfile',
            'MechanicalRuleEffect','BehavioralEffect','TotalDifference','Residual')])+r'\\[1pt]')
    lines.append(r'\end{longtable}\normalsize')
lines.append(r'\end{document}');(sources/'welfare-decompositions.tex').write_text('\n'.join(lines),encoding='utf-8')
for name in ('welfare_decomposition_exhibits.py','article_release.py','build_profile_catalog.py','individual_strategy_sources.py','welfare_overview.py','resource_accounting.py'):
    shutil.copy2(ROOT/'scripts'/name,sources/name)
def command(name,args):
    with (output/(name+'.worker.log')).open('xb') as log:
        child=subprocess.run([sys.executable,str(ROOT/'scripts/run_recorded.py'),output.name+'-'+name,*args],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    if child.returncode:raise RuntimeError(name+' failed')
for i in range(2):command('pdf-'+str(i),['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(output),str(sources/'welfare-decompositions.tex')])
pages=output/'pages';pages.mkdir();command('png',['pdftoppm','-r','130','-png',str(output/'welfare-decompositions.pdf'),str(pages/'page')])
save_new(output/'result.json',dict(Schema='welfare-decomposition-exhibits-v1',Passed=True,CreatedUtc=utc(),Overview=identity(overview_path),
    Comparisons=len(pairs),ExpectedComparisons=36,Complete=len(pairs)==36,AlternativeTruthMapsIncluded=False,SolvesStarted=0,ReplaysStarted=0,
    PDF=identity(output/'welfare-decompositions.pdf'),Pages=[identity(f) for f in sorted(pages.glob('page-*.png'))],
    Sources=[identity(f) for f in sorted(sources.iterdir())],VisualQAPending=True))
print(f'Rendered five independent welfare decomposition tables for {len(pairs)} pairs; visual review pending.')
