"""Restore the article's Latin Modern/TikZ presentation from audited data.

Main strategy panels omit only exactly zero-reach information sets. Every
positive-probability supported action at a reached set is drawn. Full profiles,
including off-path completion, remain in the companion JSON and supplements.
"""
import math, pathlib, re, shutil, subprocess
from article_release import ROOT, identity, read, verify, save_new
from build_profile_catalog import close, MEASURES

PREAMBLE = r'''\documentclass[10pt,tikz,border=5pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,booktabs,array,tabularx,microtype,tikz}
\usetikzlibrary{patterns,patterns.meta,shapes.geometric,arrows.meta,calc,positioning}
\begin{document}
'''
RULES = [('american', 'American'), ('complete', 'British')]

def escape(value):
    return ''.join({'&':r'\&','%':r'\%','_':r'\_','#':r'\#',
                    '>':r'$\to$','×':r'$\times$','α':r'$\alpha$'}.get(c,c) for c in str(value))

def compile_tex(out, folder, title, tex):
    source=out/folder/'Sources'/(title+'.tex');source.write_text(tex,encoding='utf-8')
    work=out/'render-work'/title;work.mkdir(parents=True)
    command=['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(work),str(source)]
    p=subprocess.run(command,cwd=work,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    (work/'stdout.log').write_bytes(p.stdout);(work/'stderr.log').write_bytes(p.stderr)
    save_new(work/'command.json',dict(Command=command,ReturnCode=p.returncode,Source=identity(source)))
    if p.returncode:raise RuntimeError('TeX failed: '+str(work/'stdout.log'))
    target=out/folder/(title+'.pdf');shutil.copy2(work/(title+'.pdf'),target)
    return target

def table_pdf(out,title,sections,widths,headings,notes,fontsize=9):
    """No embedded table names, page numbers or verbose validation footnotes."""
    from pypdf import PdfWriter
    pieces=[];bodies=[]
    save_new(out/'Tables'/'Sources'/(title+'.layout.json'),dict(Headings=headings,Sections=sections,EmbeddedTitle=False,Typeface='Latin Modern'))
    for n,(subtitle,rows) in enumerate(sections,1):
        # Preserve a readable manuscript-sized table, not landscape office pages.
        w=18.4 if len(headings)>7 else 16.25
        sizes=[max(0.55,(w-.22*len(widths))*v/sum(widths)) for v in widths]
        if title.startswith(('Table 2','Table 3')):sizes=[2.6,1.15,.7,1.15,2.3,2.35,1.15,1.15,1.15,1.15,1.15]
        total=sum(sizes)+.22*len(widths)
        cols='@{}'+''.join((r'>{\raggedright\arraybackslash}' if i==0 or title.startswith('Table 1') else r'>{\centering\arraybackslash}')+f'p{{{v:.3f}cm}}' for i,v in enumerate(sizes))+'@{}'
        body=[f'\\begin{{minipage}}{{{total:.3f}cm}}',r'\small',r'\setlength{\tabcolsep}{3pt}',r'\renewcommand{\arraystretch}{1.25}']
        if subtitle and not title.startswith('Table 1'):body += [r'\noindent\textbf{'+escape(subtitle)+r'}\par\smallskip']
        body += [r'\begin{tabular}{'+cols+'}',r'\toprule', ' & '.join(r'\textbf{'+escape(x)+'}' for x in headings)+r'\\\midrule']
        for row in rows:
            if all(x=='Pending' for x in row[1:]):body.append(escape(row[0])+f' & \\multicolumn{{{len(row)-1}}}{{c}}{{Pending}}'+r'\\')
            else:body.append(' & '.join(escape(x) for x in row)+r'\\')
        body += [r'\bottomrule\end{tabular}']
        # Essential units only; explanatory captions belong in the .txt sidecar.
        short = ('Action/reach: percent. Contributions: percentage points. C/E: continue/exit.' if title.startswith(('Table 2','Table 3')) else
                 'Percent of potential disputes; primary denotes the exact single-start profile.' if title.startswith('Table 6') else '')
        if short:body += [r'\par\smallskip{\footnotesize '+escape(short)+'}']
        body += [r'\end{minipage}'];bodies.append('\n'.join(body))
        name=title+(f' - panel {n}' if len(sections)>1 else '')
        pieces.append(compile_tex(out,'Tables',name,PREAMBLE.replace('[10pt,tikz,border=5pt]','[10pt,border=5pt]')+bodies[-1]+'\n'+r'\end{document}'))
    if len(pieces)>1:
        writer=PdfWriter()
        for p in pieces:writer.append(str(p))
        with (out/'Tables'/(title+'.pdf')).open('wb') as f:writer.write(f)
        # The standalone sources for every panel remain editable and reproducible.
        (out/'Tables'/'Sources'/(title+'.tex')).write_text('% Compile each panel source independently; merge in the listed order.\n'+
            '\n'.join('% '+p.stem+'.tex' for p in pieces)+'\n',encoding='utf-8')
        for p in pieces:p.unlink()  # Generated intermediate panel PDFs only.

def marker_geometry(rule,probability=1,diameter=5):
    """Common enclosed area, including the diamond's outer black stroke edge.

    Filled circle: A=pi*r^2. Square diamond: A=2*h_outer^2.
    A miter-joined stroke of width w adds w/sqrt(2) to its half diagonal.
    Every length, including stroke/halo width, scales by sqrt(probability).
    The white contrast halo is background, not probability-bearing marker area.
    """
    if rule not in ('american','complete') or not 0<probability<=1:raise ValueError('Invalid marker')
    area=math.pi*(diameter/2)**2*probability
    scale=math.sqrt(probability)
    if rule=='american':return dict(Shape='circle',Probability=probability,AreaPt2=area,RadiusPt=math.sqrt(area/math.pi))
    width=.35*scale;outer=math.sqrt(area/2)
    return dict(Shape='diamond',Probability=probability,AreaPt2=area,OuterHalfDiagonalPt=outer,
        PathHalfDiagonalPt=outer-width/math.sqrt(2),StrokeWidthPt=width,HaloWidthPt=1.0*scale)

def mark(x,y,rule,probability=1,diameter=5):
    g=marker_geometry(rule,probability,diameter)
    prefix=f'\\begin{{scope}}[shift={{({x:.8f},{y:.8f})}}]'
    if rule=='american':path=f'\\fill[black] (0pt,0pt) circle[radius={g["RadiusPt"]:.9f}pt];'
    else:
        h=g['PathHalfDiagonalPt'];w=g['StrokeWidthPt'];halo=g['HaloWidthPt']
        path=(f'\\draw[draw=black,line width={w:.9f}pt,line join=miter,miter limit=10,'+
              f'preaction={{draw=white,line width={halo:.9f}pt,line join=miter}}] '+
              f'(0pt,{h:.9f}pt)--({h:.9f}pt,0pt)--(0pt,{-h:.9f}pt)--({-h:.9f}pt,0pt)--cycle;')
    return prefix+path+r'\end{scope}'

def strategy_figure(out,title,risk,profiles,core,record):
    sets=[(('PFile','DAnswer'),('Filing','Answering'),None)]
    if risk=='ra':sets.append((('PAbandon','DDefault'),('Commit to abandon','Commit to default'),None))
    sets += [(('PAgreeToBargain','DAgreeToBargain'),('Agree to bargain: plaintiff','Agree to bargain: defendant'),'history'),
             (('POffer','DOffer'),('Plaintiff demand','Defendant offer'),'offer')]
    rows=len(sets);h=4.7;lines=[r'\begin{tikzpicture}[font=\small]'];points=[];omitted=[]
    for row,(decisions,titles,kind) in enumerate(sets):
        for col,decision in enumerate(decisions):
            x0=1.0+col*8.5;y0=(rows-1-row)*h+1.0
            lines += [f'\\node[anchor=west,font=\\bfseries] at ({x0},{y0+3.45}) {{({chr(97+row*2+col)}) {titles[col]}}};',
                      f'\\begin{{scope}}[shift={{({x0},{y0})}},x=6.7cm,y=2.95cm]']
            for y in (0,.25,.5,.75,1):lines += [f'\\draw[black!15] (0,{y})--(1,{y});',f'\\node[anchor=east,font=\\footnotesize] at (-.025,{y}) {{{y:g}}};']
            lines.append(r'\draw (0,1)--(0,0)--(1,0);')
            for s in range(1,11):lines.append(f'\\node[anchor=north,font=\\scriptsize] at ({(s-.5)/10:.2f},-.04) {{{(s-.5)/10:.2f}}};')
            # A white halo makes the open diamond legible over a coincident circle.
            for rule in ('american','complete'):
                p=profiles[f'baseline__standard__{rule}__{risk}__cost-1']
                rr=[r for r in p['Strategies'] if r['Decision']==decision]
                for r in rr:
                    if r['Reach']==0:omitted.append(dict(Rule=rule,Decision=decision,Row=r));continue
                    x=(r['Signal']-.5)/10
                    if kind=='offer':
                        for action,pr in zip(r['Actions'],r['Probabilities']):
                            if pr>0:
                                y=float(action);lines.append(mark(x,y,rule,pr))
                                points.append(dict(Rule=rule,Decision=decision,Signal=r['Signal'],OwnExit=r['OwnExit'],Action=action,Probability=pr,Reach=r['Reach'],X=x,Y=y,MarkerAreaWeight=pr))
                    else:
                        pr=r['Probabilities'][r['Actions'].index('Yes')];lines.append(mark(x,pr,rule))
                        points.append(dict(Rule=rule,Decision=decision,Signal=r['Signal'],OwnExit=r['OwnExit'],Action='Yes',Probability=pr,Reach=r['Reach'],X=x,Y=pr,MarkerAreaWeight=1))
            lines += [r'\end{scope}',f'\\node at ({x0+3.35},{y0-.67}) {{'+('Plaintiff' if col==0 else 'Defendant')+' signal};',
                      f'\\node[rotate=90] at ({x0-1.03},{y0+1.48}) {{'+('Offer' if kind=='offer' else 'Probability')+'};']
    lines += [mark(1.25,-.45,'american'),r'\node[anchor=west] at (1.5,-.45) {American};',
              mark(4.0,-.45,'complete'),r'\node[anchor=west] at (4.25,-.45) {British};',
              r'\node[anchor=west,font=\footnotesize,align=left] at (6.2,-.45) {For mixed offer strategies: area $\propto$ action probability.};']
    lines.append(r'\end{tikzpicture}')
    compile_tex(out,'Figures',title,PREAMBLE+'\n'.join(lines)+r'\end{document}')
    # Exact representation checks: no off-path rows drawn; every reached support included.
    assert all(p['Reach']>0 for p in points)
    for rule in ('american','complete'):
        p=profiles[f'baseline__standard__{rule}__{risk}__cost-1']
        for r in p['Strategies']:
            if r['Decision'] in ('POffer','DOffer') and r['Reach']>0:
                got=[a for a in points if (a['Rule'],a['Decision'],a['Signal'],a['OwnExit'])==(rule,r['Decision'],r['Signal'],r['OwnExit'])]
                assert [(a['Action'],a['Probability']) for a in got]==[(a,v) for a,v in zip(r['Actions'],r['Probabilities']) if v>0]
    record('Figures',title,dict(Cases=[core(risk,r) for r,_ in RULES],Profiles=[profiles[core(risk,r)['CaseId']] for r,_ in RULES],
        DisplayedPoints=points,OmittedZeroReach=omitted,ExactPositiveSupportVerified=True,
        MarkerGeometry=[dict(Rule=p['Rule'],Decision=p['Decision'],Signal=p['Signal'],OwnExit=p['OwnExit'],Action=p['Action'],
            **marker_geometry(p['Rule'],p['MarkerAreaWeight'])) for p in points],
        MarkerAreaConvention='Same enclosed area for equal probabilities across both shapes; includes diamond outer black stroke edge, excludes background contrast halo.'),
        'American (filled circles) and British (open diamonds), cost multiplier 1. Blank positions are unreached. '+
        ('All reached exit commitments are to continue; their redundant panels are omitted. ' if risk=='rn' else 'Commitment panels distinguish exit from continuation histories. ')+
        'Agreement and offers condition on own commitment. Reached offer support is shown without averaging. For mixed offer strategies, enclosed marker area is proportional to action probability on a common scale across circles and diamonds; the background contrast halo is excluded. Complete policies, including unreached completion, remain in Sources and individual simulation reports.')

def dispositions(out,title,risk,profiles,core,record,report_dispositions):
    ds=[report_dispositions(profiles[core(risk,r)['CaseId']]) for r,_ in RULES]
    styles=[r'preaction={fill=white,draw=none},pattern={Dots[distance=4pt,radius=.35pt]},pattern color=black',
            r'preaction={fill=black,draw=none},pattern={Dots[distance=2.8pt,radius=.35pt]},pattern color=white',
            'fill=black!50',r'preaction={fill=white,draw=none},pattern=north east lines,pattern color=black',
            r'preaction={fill=black,draw=none},pattern=north east lines,pattern color=white','fill=white','fill=black']
    labels=list(ds[0]);lines=[r'\begin{tikzpicture}[font=\small]']
    for v in range(0,101,20):
        x=2+v*.13;lines += [f'\\draw[black!15] ({x},.5)--({x},2.4);',f'\\node[anchor=north] at ({x},.4) {{{v}\\%}};']
    for k,(_,label) in enumerate(RULES):
        y=2-k*.9;left=2;lines.append(f'\\node[anchor=east] at (1.8,{y}) {{{label}}};')
        for j,name in enumerate(labels):
            value=ds[k][name];right=left+value*13
            if value>0:lines.append(f'\\path[{styles[j]},draw=black,line width=.25pt] ({left:.8f},{y-.26}) rectangle ({right:.8f},{y+.26});')
            if value>=.035:
                dark=j in (1,4,6);lines.append(f'\\node[text={"white" if dark else "black"},fill={"black" if dark else "white"},font=\\footnotesize,inner sep=1pt] at ({(left+right)/2:.8f},{y}) {{{value*100:.1f}}};')
            left=right
    lines.append(r'\node at (8.5,-.25) {Potential disputes};')
    for j,label in enumerate(labels):
        x=(j%3)*5.1;y=-1-(j//3)*.57
        lines += [f'\\path[{styles[j]},draw=black,line width=.25pt] ({x},{y-.13}) rectangle ({x+.45},{y+.13});',f'\\node[anchor=west] at ({x+.56},{y}) {{{label}}};']
    lines.append(r'\end{tikzpicture}');compile_tex(out,'Figures',title,PREAMBLE+'\n'.join(lines)+r'\end{document}')
    record('Figures',title,dict(Cases=[core(risk,r)['CaseId'] for r,_ in RULES],Dispositions=ds,PatternStyles=styles),
        'Terminal dispositions at cost multiplier 1, as shares of all potential disputes. White-background patterns denote pro-defendant outcomes; black-background patterns denote pro-plaintiff outcomes; settlements are gray. Agreement refusal invokes the chosen commitments or trial and is not an additional disposition.')

def worked_path(out,record,core):
    source=ROOT/'reporting/worked-path-restored-v1/Sources/worked equilibrium paths.json';data=read(source)
    paths={p['Name']:p for p in data['Paths']};macros={}
    def st(p,d):return next(s for s in paths[p]['Steps'] if s['Decision']==d)
    def ac(p,d,a):return next(x for x in st(p,d)['Actions'] if x['Action']==a)
    def num(k,v,d=3):macros[k]=f'{v:.{d}f}'
    def info(k,p,d):macros[k]=str(st(p,d)['InformationSetNumber'])
    def utility(k,p,d,a):num(k,ac(p,d,a)['ConditionalActingPlayerUtility'])
    def outcome(p,c=None):return next(o for o in paths[p]['Outcomes'] if o['CourtSignal']==c)
    def pair(k,p,c=None):o=outcome(p,c);macros[k]=f"{o['PlaintiffNetMonetaryPayoff']:.2f},\\,{o['DefendantNetMonetaryPayoff']:.2f}"
    for p in ('trial','settlement','adjacent-defendant-signal'):
        assert paths[p]['EquilibriumProbability']>0
        close(math.prod(ac(p,s['Decision'],s['SelectedAction'])['Probability'] for s in paths[p]['Steps']),paths[p]['EquilibriumProbability'],'path probability')
    for p in ('trial','settlement'):
        for d in ('PAbandon','DDefault','PAgreeToBargain','DAgreeToBargain'):
            assert ac(p,d,2 if d in ('PAbandon','DDefault') else 1)['Probability']==1
    for d,ps in [('PFile',('trial','adjacent-defendant-signal')),('DAnswer',('trial','settlement')),('DDefault',('trial','settlement')),('DAgreeToBargain',('trial','settlement')),('DOffer',('trial','settlement','lower-demand-deviation'))]:
        assert len({st(p,d)['InformationSetNumber'] for p in ps})==1
    for k,p,d in [('FileMainInfo','trial','PFile'),('FileMixedInfo','settlement','PFile'),('AnswerInfo','trial','DAnswer'),('PExitMainInfo','trial','PAbandon'),('PExitMixedInfo','settlement','PAbandon'),('DExitInfo','trial','DDefault'),('DemandMainInfo','trial','POffer'),('DemandMixedInfo','settlement','POffer'),('OfferInfo','trial','DOffer'),('PAgreeMainInfo','trial','PAgreeToBargain'),('PAgreeMixedInfo','settlement','PAgreeToBargain'),('DAgreeInfo','trial','DAgreeToBargain')]:info(k,p,d)
    for k,p,d,a in [('SignalMainProbability','trial','PLiabilitySignal',4),('SignalMixedProbability','settlement','PLiabilitySignal',3),('DSignalMainProbability','trial','DLiabilitySignal',3),('DSignalAdjacentProbability','trial','DLiabilitySignal',4),('DSignalMixedProbability','settlement','DLiabilitySignal',3),('FileMixedProbability','settlement','PFile',1),('NoFileMixedProbability','settlement','PFile',2)]:num(k,ac(p,d,a)['Probability'])
    for k,p,d,a in [('FileMainUtility','trial','PFile',1),('NoFileMainUtility','trial','PFile',2),('FileMixedUtility','settlement','PFile',1),('NoFileMixedUtility','settlement','PFile',2),('AnswerUtility','trial','DAnswer',1),('NoAnswerUtility','trial','DAnswer',2),('DemandMainUtility','trial','POffer',8),('DemandLowDeviationUtility','trial','POffer',1),('DemandMixedUtility','settlement','POffer',1),('OfferUtility','trial','DOffer',1),('OfferHighUtility','trial','DOffer',8)]:utility(k,p,d,a)
    for k,p,d,a in [('DemandMainValue','trial','POffer',8),('DemandLowValue','settlement','POffer',1),('OfferValue','trial','DOffer',1)]:num(k,float(ac(p,d,a)['Label']),2)
    for k,p,c in [('NoFilingPayoff','no-filing',None),('NoAnswerPayoff','no-answer-deviation',None),('SettlementPayoff','settlement',None),('LowDeviationPayoff','lower-demand-deviation',None),('HighDeviationPayoff','higher-offer-deviation',None),('TrialWinPayoff','trial',2),('TrialLosePayoff','trial',1)]:pair(k,p,c)
    for k,c in [('CourtWinProbability',2),('CourtLoseProbability',1)]:num(k,outcome('trial',c)['ConditionalProbability'])
    original=ROOT/'source/LitigCharts/WorkedPathDiagram.cs';text=original.read_text(encoding='utf-8-sig').split('Layout = """',1)[1].split('""";',1)[0]
    # Insert a compact agreement strip between commitments and the original offers.
    split=text.index('% (b)');tail=text[text.index('% (c)'):]
    top=text[:split]
    mid=r'''
\node[stage] at (-.1,-7.15) {(b) Private exit commitments and agreement to bargain};
'''
    for suffix,y,start,nextname,style,pinfo in [('h',-8.5,'A',r'A\(^{\prime}\)','main','Main'),('l',-10.7,'B',r'B\(^{\prime}\)','branch','Mixed')]:
        nodes=[('start',.15,'cont',start),('pex',1.35,'player',r'$P_{\PExit'+pinfo+r'Info}$'),('dex',4.5,'player',r'$D_{\DExitInfo}$'),('pag',7.7,'player',r'$P_{\PAgree'+pinfo+r'Info}$'),('dag',11.3,'player',r'$D_{\DAgreeInfo}$'),('end',15.6,'cont',nextname)]
        for name,x,kind,label in nodes:mid+=f'\\node[{kind}] ({name}{suffix}) at ({x},{y}) {{{label}}};\n'
        for a,b,label in [('start','pex',''),('pex','dex','No P exit'),('dex','pag','No D exit'),('pag','dag','P agrees'),('dag','end','D agrees')]:mid+=f'\\draw[{style}] ({a}{suffix}) -- node[lab,above] {{{label}}} ({b}{suffix});\n'
        for name,x,label in [('pex',1.35,'Exit'),('dex',4.5,'Exit'),('pag',7.7,'Refuse'),('dag',11.3,'Refuse')]:mid+=f'\\draw[deviation] ({name}{suffix}) -- ({x+.55},{y-.85}) node[lab,right] {{{label}: $p=0$ $\\cdots$}};\n'
    mid+=r'\draw[infoset] (dexh)--(dexl);\draw[infoset] (dagh)--(dagl);'+'\n'
    # Reuse the original offer strip geometry; commitments are already above.
    old=text[split:text.index('% (c)')]
    old=old[old.index(r'\node[stage]'):]
    old=old.replace('(b) Exit commitments and simultaneous offers','(c) Simultaneous offers')
    old=old.replace(r'\node[player] (pexh) at (1.35,-8.75) {$P_{\PExitMainInfo}$};','').replace(r'\node[player] (dexh) at (4.5,-8.75) {$D_{\DExitInfo}$};','')
    old=old.replace(r'\node[player] (pexl) at (1.35,-13.05) {$P_{\PExitMixedInfo}$};','').replace(r'\node[player] (dexl) at (4.5,-13.05) {$D_{\DExitInfo}$};','')
    old='\n'.join(line for line in old.splitlines() if not any(n in line for n in ('pexh','pexl','dexh','dexl')))
    old=old.replace(r'{A};',r'{A\(^{\prime}\)};').replace(r'{B};',r'{B\(^{\prime}\)};')
    old+=r'\draw[main] (astart)--(poh);\draw[branch] (bstart)--(pol);'+'\n'
    # Remove left dead space in this strip, retaining room for utilities/deviations.
    old=old.replace('(7.7,-8.75)','(3,-8.75)').replace('(7.7,-13.05)','(3,-13.05)').replace('(7.9,-9.8)','(3.2,-9.8)').replace('(8.1,-14.05)','(3.4,-14.05)')
    old=old.replace('(11.3,-8.75)','(9.5,-8.75)').replace('(11.3,-13.05)','(9.5,-13.05)')
    def lower_coords(s,offset):return re.sub(r'\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)',lambda m:'('+m[1]+','+f'{float(m[2])-offset:g}'+')',s)
    old=lower_coords(old,5.6)
    tail=lower_coords(tail,5.6).replace('(c) Trial and net monetary outcomes','(d) Trial and net monetary outcomes')
    text=top+mid+old+tail
    bindings='\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in sorted(macros.items()))
    text=text.replace('% INSERT_EXTRACTED_VALUES',bindings)
    title='Figure 2 - Worked equilibrium path';compile_tex(out,'Figures',title,text)
    record('Figures',title,dict(Case=core('rn','american'),Extraction=identity(source),Paths=data,LayoutSource=identity(original),VerifiedInformationSetLinks=True),
        'An actual American-rule risk-neutral equilibrium history at cost 1, with adjacent signal histories and zero-probability deviations. Solid branches have positive probability; the thick path reaches trial after unsuccessful offers. Both parties agree to bargain. Dotted links connect the same information set, so sequential drawing does not imply observation. Utilities condition on each player\'s information set; monetary payoffs are changes in wealth. Omitted branches remain in the game and are not renormalized.')

def welfare_figure(out,catalog,record):
    title='Figure 7 - Welfare outcomes';costs=[.25,.5,1,2,4]
    cs={(c['Parameters']['AlphaP'],c['Parameters']['CostMultiplier'],c['Parameters']['FeeRule']):c for c in catalog['Cases']
        if c['Parameters']['OriginalOptionName'] and c['Parameters']['FeeRule'] in ('american','complete') and c['Parameters']['AlphaP']==c['Parameters']['AlphaD']}
    assert len(cs)==20
    labels=[r'Meritorious plaintiff\\shortfall',r'Nonliable defendant\\burden',r'Liable defendant\\excess burden',r'Gross outcome\\error',r'Real litigation\\expenditures']
    lines=[r'\begin{tikzpicture}[font=\small]'];values=[]
    for ri,alpha in enumerate((0,2)):
        top=13-ri*7
        lines.append(f'\\node[anchor=west,font=\\bfseries] at (1.0,{top+.6}) {{'+('Risk neutral' if alpha==0 else 'Risk averse')+'};')
        for j,(field,label) in enumerate(zip(MEASURES,labels)):
            x0=1.15+j*3.15;bound=max(c['Welfare']['Headline'][field] for c in cs.values())*1.08
            # Round upper limit up to a readable common scale within both risk panels.
            step=10**math.floor(math.log10(bound))/2;bound=math.ceil(bound/step)*step
            lines.append(f'\\node[align=center,font=\\footnotesize] at ({x0+1.35},{top-.05}) {{{label}}};')
            for i,cost in enumerate(costs):
                y=top-1-i*.83
                if j==0:lines.append(f'\\node[anchor=east] at ({x0-.18},{y}) {{$\\times {cost:g}$}};')
                lines.append(f'\\fill[black!{4 if i%2==0 else 0}] ({x0},{y-.35}) rectangle ({x0+2.7},{y+.35});')
                for k,rule in enumerate(('complete','american')):
                    value=cs[alpha,cost,rule]['Welfare']['Headline'][field];x=x0+2.7*value/bound;yy=y+(.11 if rule=='american' else -.11)
                    lines.append(mark(x,yy,rule,diameter=3.5));values.append(dict(Case=cs[alpha,cost,rule]['CaseId'],Measure=field,Value=value,AxisMaximum=bound))
            y=top-4.75;lines.append(f'\\draw ({x0},{y})--({x0+2.7},{y});')
            for frac in (0,.5,1):
                anchor={0:'north west',.5:'north',1:'north east'}[frac]
                lines.append(f'\\node[anchor={anchor},font=\\footnotesize,inner xsep=0pt] at ({x0+2.7*frac},{y-.08}) {{{bound*frac:.2f}}};')
    lines += [mark(5.5,.3,'american',diameter=3.5),r'\node[anchor=west] at (5.85,.3) {American};',
              mark(10,.3,'complete',diameter=3.5),r'\node[anchor=west] at (10.3,.3) {British};',r'\end{tikzpicture}']
    compile_tex(out,'Figures',title,PREAMBLE+'\n'.join(lines)+r'\end{document}')
    record('Figures',title,dict(Cases=list(cs.values()),PlottedValues=values,MainProfiles=20,Replaces='Table 4 - Welfare outcomes',
        MarkerGeometry={r:marker_geometry(r,diameter=3.5) for r,_ in RULES}),
        'Five monetary outcomes under the American and British rules, by cost multiplier and risk preference. Each dot is the selected exact single-start equilibrium; all 20 main cases are present. Horizontal scales match between risk panels within each outcome column. Welfare measures are distinct and are not summed. This figure replaces Table 4 in Welfare Analysis; the mechanical/behavioral decomposition remains in the associated supplemental materials.')

def render_figures(out,catalog,profiles,core,record,inputs,report_dispositions):
    signalpath=ROOT/'reporting/final-signal-collection-v2/result.json';signals=read(signalpath)
    signal=next(a for a in signals['Artifacts'] if a['CaseId']==core('rn','american')['CaseId'] and a['FileStem']=='Continuous merits - party - bw')
    title='Figure 1 - Information structure'
    shutil.copy2(verify(signal['PDF']),out/'Figures'/(title+'.pdf'));shutil.copy2(verify(signal['TeX']),out/'Figures'/'Sources'/(title+'.tex'))
    record('Figures',title,read(verify(signal['Data'])),verify(signal['Caption']).read_text(encoding='utf-8'));inputs.append(identity(signalpath))
    worked_path(out,record,core)
    for risk,dispidx,stratidx in [('rn',3,4),('ra',5,6)]:
        dispositions(out,f'Figure {dispidx} - '+('Dispositions' if risk=='rn' else 'Risk-averse dispositions'),risk,profiles,core,record,report_dispositions)
        strategy_figure(out,f'Figure {stratidx} - '+('Participation and offers' if risk=='rn' else 'Risk-averse participation and offers'),risk,profiles,core,record)
    welfare_figure(out,catalog,record)
    inputs.append(identity(__file__))
    shutil.copy2(__file__,out/'Figures'/'Sources'/pathlib.Path(__file__).name)
    shutil.copy2(__file__,out/'Tables'/'Sources'/pathlib.Path(__file__).name)
