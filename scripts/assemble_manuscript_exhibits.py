"""Assemble numbered manuscript exhibits from the canonical results and separate analyses."""
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SUPP=ROOT/'Supplemental materials'
RESULTS=ROOT/'Results'
MECHANISMS=SUPP/'Equilibrium strategy changes'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,text):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf-8',newline='\n')
def wrapper(body,width='16cm'):
    return (r'\documentclass[10pt,border=5pt,varwidth='+width+r']{standalone}'+'\n'+
            r'\usepackage[T1]{fontenc}\usepackage{lmodern,booktabs,tabularx,array,microtype}'+'\n'+
            r'\begin{document}\begin{minipage}{'+width+r'}\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.2}'+'\n'+
            body+'\n'+r'\end{minipage}\end{document}'+'\n')
def artifact_path(source,extension):
    if source.parent==MECHANISMS/'Sources/Tex':
        directory=(MECHANISMS/'Tables' if extension in ['.pdf','.png'] else
                   MECHANISMS/'Sources/Json' if extension=='.json' else
                   MECHANISMS/'Sources' if extension=='.txt' else source.parent)
        return directory/(source.stem+extension)
    return (source.parent.parent/(source.stem+extension)
            if source.parent.name=='Sources' and extension in ['.pdf','.png'] else source.with_suffix(extension))

def compile_tex(path):
    with tempfile.TemporaryDirectory(prefix='acesim-main-') as tmp:
        for _ in range(2):
            result=subprocess.run(['lualatex','--interaction=nonstopmode','--halt-on-error','--jobname=exhibit',
                                   '--output-directory='+tmp,str(path)],cwd=path.parent,capture_output=True)
            if result.returncode:raise RuntimeError(result.stdout.decode(errors='replace')[-3500:])
        pdf=Path(tmp)/'exhibit.pdf'
        subprocess.run(['pdftoppm','-png','-singlefile','-r','150',str(pdf),str(Path(tmp)/'exhibit')],check=True,capture_output=True)
        for ext in ['.pdf','.png']:
            destination=artifact_path(path,ext);destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(Path(tmp)/('exhibit'+ext),destination)

def primitives():
    source=SUPP/'Game tree diagrams/Sources/model-primitives.tex'
    body=r'''\begin{tabularx}{\linewidth}{@{}p{3cm}X@{}}
\toprule Primitive & Core comparison \\ \midrule
Common merits & $Q\sim U[0,1]$; $T\mid Q\sim\mathrm{Bernoulli}(Q)$; $\Pr(T=1)=0.5$ \\
Private information & One noisy merits signal per party; 10 signal bins each \\
Signal noise & $\sigma_P=\sigma_D=\sigma_C=0.20$ \\
Adjudication & Two court-signal bins; fixed damages $d=1$ \\
Initial wealth & $w_P=w_D=10$ \\
Filing and answering & Endogenous; cost $0.15$ for each acting party \\
Trial & Additional cost $0.15$ per party; no additional bargaining cost \\
Exit & Parties commit before offers to continue or exit if bargaining fails \\
Bargaining & One simultaneous round; 10 offers $0.05,0.15,\ldots,0.95$; midpoint settlement if demand $\leq$ offer \\
Preferences & Risk neutral or symmetric CARA, $\alpha=2$ \\
Cost comparisons & Common cost multipliers $0.25,0.5,1,2,4$ \\
Integration & 64-point Gauss--Legendre integration over continuous merits \\
\bottomrule\end{tabularx}\par\medskip
\begin{tabularx}{\linewidth}{@{}Xccc@{}}
\toprule Fee trigger & American & \shortstack{Trial\\Fee-Shifting} & \shortstack{Complete\\Fee-Shifting} \\ \midrule
After trial & Own costs & Loser pays & Loser pays \\
Initial nonanswer & Own costs & Own costs & D pays P's fees \\
Later P abandonment & Own costs & Own costs & P pays D's fees \\
Later D default & Own costs & Own costs & D pays P's fees \\
Settlement & Own costs & Own costs & Own costs \\
\bottomrule\end{tabularx}'''
    write(source,wrapper(body))
    caption=('Model primitives and the three core fee rules. Stage costs shown at cost multiplier 1; the same multiplier scales all costs. '
             'Signals are conditionally independent given exact Q and correlated unconditionally. Parties observe their own signal, '
             'not Q, true liability or the court signal. Exit reimbursements cover incurred, unsaved expenses; future trial costs are '
             'not incurred on exit. Nonanswer reimburses the plaintiff\'s incurred filing expense under Complete Fee-Shifting. '
             'Unfiled disputes incur no litigation costs. Settlement uses the model\'s inclusive transfer with each party bearing its own costs. '
             'Mutual give-up is allocated equally between abandonment and default. The rules are precise model treatments, '
             'not complete descriptions of national procedural systems.')
    write(source.with_suffix('.txt'),caption+'\n')
    summaries=[RESULTS/'Run records/Retained study'/f'{p} numerical results.csv' for p in ['CS004','CS006EF']]
    write(source.with_suffix('.json'),json.dumps({'Sources':[{'Path':str(p.relative_to(ROOT)),'Sha256':sha(p)} for p in summaries],
        'Caption':caption},indent=2)+'\n')
    compile_tex(source)
    return source

def mechanisms():
    provenance=[]
    def comparison_row(contrast,decision,signal):
        p=MECHANISMS/'Sources/Tex'/(contrast+'.tex')
        data_path=MECHANISMS/'Sources/Json'/(contrast+'.json')
        data=read(data_path)
        if data['Contrast']['Id']!=contrast:raise ValueError('Mismatched directed comparison')
        for source in data['Inputs']:
            if sha(Path(source['Path'])).lower()!=source['Sha256'].lower():raise ValueError('Changed calculation request')
        limits=[float(x) for x in signal.split('--')];low,high=limits[0],limits[-1]
        rows=[r for r in data['SelectedRows'] if r['Decision'].lower()==decision.lower()
              and low-1e-8<=r['SignalValue']<=high+1e-8]
        if not rows or any(r['Metric']!='decision probability' or r['CounterfactualUndefined'] for r in rows):
            raise ValueError((contrast,decision,signal,'Missing defined binary-policy selection'))
        if abs(min(r['SignalValue'] for r in rows)-low)>1e-8 or abs(max(r['SignalValue'] for r in rows)-high)>1e-8:
            raise ValueError('Incomplete selected signal range')
        a=rows[0]['Allocation'];columns=['Original','Target','Direct','Entry','Offers','Exit','SelectionResidual']
        if any(abs(r['Allocation'][k]-a[k])>1e-6 for r in rows for k in columns):
            raise ValueError('Selected signals do not share the same numerical row')
        if any(r['UnreachedCoalitions']!=rows[0]['UnreachedCoalitions'] for r in rows):
            raise ValueError('Selected signals have different intermediate reach patterns')
        def number(v,signed=False):
            if abs(v)<.05:v=0
            return ('+' if signed and v>0 else '')+f'{v:.1f}'.rstrip('0').rstrip('.')
        label=decision+(r'$^{*}$' if rows[0]['UnreachedCoalitions'] else '')
        endpoints='$'+number(a['Original'])+r'\%\to '+number(a['Target'])+r'\%$'
        flags=sum(r['TieSensitive'] or r['CompletionSensitive'] for r in rows)
        sensitive='No' if flags==0 else 'Yes' if flags==len(rows) else 'At some signals'
        line=' & '.join([label,signal,endpoints]+['$'+number(a[k],True)+'$' for k in columns[2:]]+[sensitive])+r'\\'
        provenance.append({'Path':str(p.relative_to(ROOT)),'Sha256':sha(p),'SelectedLine':line,
                           'DataPath':str(data_path.relative_to(ROOT)),
                           'DataSha256':sha(data_path),
                           'SelectedCoordinates':[{'Key':r['Key'],'Action':r['Action']} for r in rows],
                           'Validation':'Strict conditional action-loss or offsetting-effect selection in the saved equilibria; residual and sensitivity retained.'})
        return line
    panels=[
        ('American to Trial Fee-Shifting; risk neutral',[
            comparison_row('american-to-trial-risk-neutral-cost-1','P files','0.25')]),
        ('Trial to Complete Fee-Shifting; risk neutral',[
            comparison_row('trial-to-complete-risk-neutral-cost-1','D answers','0.65--0.95'),
            comparison_row('trial-to-complete-risk-neutral-cost-1','P files','0.25')]),
        ('Trial to Complete Fee-Shifting; risk averse',[
            comparison_row('trial-to-complete-risk-averse-cost-1','D answers','0.75')]),
        ('American to Complete Fee-Shifting; risk neutral',[
            comparison_row('american-to-complete-risk-neutral-cost-1','P files','0.25')]),
        ('Risk neutral to risk averse; American',[
            comparison_row('risk-neutral-to-risk-averse-american-cost-1','P files','0.25'),
            comparison_row('risk-neutral-to-risk-averse-american-cost-1','P files','0.35')])]
    body=r'''\begin{tabularx}{\linewidth}{@{}lcc*{5}{>{\centering\arraybackslash}X}c@{}}
\toprule Decision & Signal & Original $\to$ Target & Direct & \shortstack{Opponent\\entry} & \shortstack{Opponent\\offers} & \shortstack{Opponent\\exit} & Residual & Sensitive \\'''
    for label,rows in panels:
        body+='\n'+r'\midrule\multicolumn{9}{@{}l}{\textit{'+label+r'}}\\[2pt]'+'\n'+'\n'.join(rows)
    body+='\n'+r'\bottomrule\end{tabularx}'
    source=MECHANISMS/'Sources/Tex/selected-strategy-mechanisms.tex'
    # Use one common percentage-point notation in the caption and keep numeric columns compact.
    body=body.replace(r'\,\mathrm{pp}','')
    write(source,wrapper(body,'18cm'))
    caption=('Selected equilibrium strategy changes at cost multiplier 1. Endpoints are probabilities at the indicated own-signal information sets; '
             'all five contribution columns are percentage points. Direct applies the rule or preference change first while holding opponents\' policies fixed. '
             'Opponent entry, offers and exit average marginal contributions over all six replacement orders. Residual is retained explicitly. '
             'The last row shows an unchanged filing policy with offsetting direct and opponent effects. These are counterfactual decompositions of selected '
             'equilibria, not observed adjustment paths or identified causal effects. Sensitive flags recorded tie or off-path completion sensitivity. '
             'Every selected coordinate satisfies the strict conditional action-loss or offsetting-effect criterion in the saved equilibrium profiles. '
             'Tie and off-path completion sensitivity checks and endpoint residuals remain explicit; the decomposition need not be invariant across other equilibria. '
             'Full policies, reach, unrounded allocations and provenance for all 90 directed core comparisons are in the supplemental JSON.')
    write(artifact_path(source,'.txt'),caption+'\n')
    write(artifact_path(source,'.json'),json.dumps({'Caption':caption,'SelectedSources':provenance},indent=2)+'\n')
    compile_tex(source)
    return source

def assemble():
    t1=primitives();t3=mechanisms()
    specs=[
        ('Figures','Figure 1 - Information structure',SUPP/'Liability signals diagrams/Continuous merits - party - bw.tex'),
        ('Figures','Figure 2 - Worked equilibrium path',SUPP/'Game tree diagrams/worked equilibrium path.tex'),
        ('Figures','Figure 3 - Participation and offers',RESULTS/'Aggregated Data/Baseline/Risk Neutral/Sources/cost-1-participation-and-offers.tex'),
        ('Figures','Figure 4 - Dispositions',RESULTS/'Aggregated Data/Baseline/Risk Comparison/Sources/cost-1-dispositions.tex'),
        ('Tables','Table 1 - Model primitives',t1),
        ('Tables','Table 2 - Welfare outcomes',RESULTS/'Aggregated Data/Baseline/Risk Comparison/Sources/cost-1-welfare-outcomes.tex'),
        ('Tables','Table 3 - Strategy mechanisms',t3)]
    manifest=[]
    for folder,stem,source in specs:
        output=ROOT/folder
        for ext in ['.pdf','.png','.tex','.json','.txt']:
            origin=artifact_path(source,ext)
            if stem.startswith('Figure 2') and ext=='.json':
                origin=SUPP/'Game tree diagrams/worked equilibrium paths.json'
            if not origin.exists():continue
            target=(output if ext in ['.pdf','.png'] else output/'Sources')/(stem+ext)
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(origin,target)
            manifest.append({'Exhibit':stem,'Source':str(origin.relative_to(ROOT)),'Output':str(target.relative_to(ROOT)),'Sha256':sha(target)})
        caption=None
        if stem.startswith('Figure 3'):
            caption=read(source.with_suffix('.json'))['Caption']+' All three core rules are shown under risk neutrality, cost multiplier 1, standard noise 0.20 and the ten-offer grid.'
        elif stem.startswith('Figure 4'):
            caption=('Disposition of potential disputes under the three core fee rules, with risk neutrality and symmetric CARA alpha 2, at cost multiplier 1. '
                     'All cases use standard noise 0.20 and ten offers. Each bar uses the full population, including unfiled disputes. '
                     'Categories are mutually exclusive; mutual give-up is allocated once, equally to later abandonment and default. '
                     'Trial outcomes denote court findings rather than true liability. Complete Fee-Shifting covers trial, initial nonanswer and later unilateral exit; '
                     'Trial Fee-Shifting covers trial only. Differences compare selected equilibria and do not track individual disputes across rules.')
        elif stem.startswith('Table 2'):
            caption=('Welfare outcomes per potential dispute at cost multiplier 1, standard noise 0.20 and ten offers. '
                     'Risk averse denotes symmetric CARA alpha 2. The first three columns are the prior-weighted meritorious-plaintiff net recovery shortfall, '
                     'nonliable-defendant net burden, and liable-defendant excess net burden above deserved damages; each includes legal costs and fee transfers. '
                     'Gross outcome error is E[|R-T|], where R is the base payment before legal costs and separately awarded fee transfers, T is true liability, and damages equal one. '
                     'Real expenditures exclude transfers. All measures include unfiled disputes. These five measures are distinct and should not be added together. '
                     'Displayed values are rounded to four decimals; source precision and calculations remain in JSON and CSV.')
        if caption:
            target=output/'Sources'/(stem+'.txt');write(target,caption+'\n')
            manifest.append({'Exhibit':stem,'Source':'Manuscript caption specification in scripts/assemble_manuscript_exhibits.py',
                             'Output':str(target.relative_to(ROOT)),'Sha256':sha(target)})
    write(ROOT/'manuscript-exhibits.json',json.dumps({'Exhibits':manifest},indent=2)+'\n')
    for folder in ['Figures','Tables']:
        lines=['# Numbered main '+folder.lower(),'',
            'PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text. Captions and costs are not added inside the research artwork.','',
            '| Exhibit | Canonical source |','|---|---|']
        for selected_folder,stem,source in specs:
            if selected_folder!=folder:continue
            canonical=artifact_path(source,'.pdf')
            lines.append(f'| [{stem}](<{stem}.pdf>) | [{canonical.stem}](<../{canonical.relative_to(ROOT).as_posix()}>) |')
        lines+=['','Regenerate with `python scripts/assemble_manuscript_exhibits.py` from the article repository. The script uses saved results and separate diagnostic calculations; it does not determine equilibria. `manuscript-exhibits.json` records the source/output hashes. After importing a new Results collection, rerun assembly to refresh these copies.','',
            'The revision plan retains four main figures and three main tables. Numbered online appendices, manuscript insertion and submission-proof review remain separate writing and packaging work.']
        write(ROOT/folder/'README.md','\n'.join(lines)+'\n')
    print('Assembled four numbered figures and three numbered tables.')

if __name__=='__main__':assemble()
