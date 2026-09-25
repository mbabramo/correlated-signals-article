"""Preserve the six established figure/table roles using frozen audited inputs.

Rendering only: no solves, altered probabilities, profile transplants or new audits.
All scalar calculations retain source precision in JSON; printed values round only.
"""
import argparse, csv, itertools, math, pathlib, shutil, subprocess, textwrap
from collections import defaultdict
from article_release import ROOT, identity, read, save_new, utc, verify
from build_profile_catalog import validate_profile, close, MEASURES

TASK = pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to')
CAT = ROOT/'reporting/audited-primary-catalog-v13/catalog.json'
GROUP = ROOT/'reporting/approximate-stable-200-grouping-v1/catalog.json'
SELECT = TASK/'outputs/Main-strategic-mechanisms-v1/selections.json'
MLABELS = ['Meritorious-plaintiff shortfall','Nonliable-defendant burden','Liable-defendant excess burden',
           'Gross outcome error','Real litigation expenditures']
MABBR = ['P shortfall','D nonliable','D excess','Gross error','Real costs']
RULES = [('american','American'),('complete','British')]
LABELS = ['P files','D answers','P commits to exit','D commits to exit','P agrees','D agrees','P offer','D offer']
FIELDS = ['Direct','Entry','Offers','Exit','Agreement']
DISP_KEYS = ['PDoesntFile','DDoesntAnswer','SettlesBR1','PAbandonsBR1','DDefaultsBR1','P Loses','P Wins']
DISP_LABELS = ['Not filed','Not answered','Settled','P abandons','D defaults','P loses at trial','P wins at trial']

def number(v, digits=3, signed=False):
    return format(v, ('+' if signed else '')+f'.{digits}f')

def report_dispositions(profile):
    with verify(profile['ReplayReport']).open(newline='',encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    row=next(x for x in rows if x['Filter']=='All')
    values=[float(row[k]) for k in DISP_KEYS]
    # Printed replay CSV uses the existing 1e-5 numeric audit tolerance.
    expected=[1-profile['Metrics']['Filing'], profile['Metrics']['Filing']-profile['Metrics']['JointFileAnswer'],
              profile['Metrics']['Settlement'],profile['Metrics']['Abandonment'],profile['Metrics']['Default']]
    assert all(abs(a-b)<=1e-5 for a,b in zip(values,expected))
    assert abs(values[-1]+values[-2]-profile['Metrics']['Trial'])<=1e-5
    assert abs(sum(values)-1)<=1e-5
    return dict(zip(DISP_LABELS,values))

def strategy_rows(profile, decision, own=None):
    rows=sorted([r for r in profile['Strategies'] if r['Decision']==decision and r['OwnExit']==own],key=lambda x:x['Signal'])
    assert [r['Signal'] for r in rows]==list(range(1,11))
    return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=pathlib.Path);args=parser.parse_args()
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    for d in ('Figures','Tables'):(out/d/'Sources').mkdir(parents=True)
    (out/'review-pages').mkdir()
    catalog=read(CAT);case_by_id={c['CaseId']:c for c in catalog['Cases']};profiles={};inputs=[identity(CAT),identity(GROUP),identity(SELECT)]
    for case in catalog['Cases']:
        profile=read(verify(case['CompleteProfile']));audit=read(verify(case['Audit']));validate_profile(audit,profile)
        profiles[case['CaseId']]=profile;inputs.extend([case['CompleteProfile'],case['Audit']])
    def core(risk,rule):return case_by_id[f'baseline__standard__{rule}__{risk}__cost-1']
    def cp(risk,rule):return profiles[core(risk,rule)['CaseId']]
    artifacts=[]
    def record(folder,title,data,caption):
        path=out/folder/'Sources'/title
        save_new(path.with_suffix('.json'),data)
        path.with_suffix('.txt').write_text(caption+'\n',encoding='utf-8')
        artifacts.append(dict(Title=title,Folder=folder,PDF=identity(out/folder/(title+'.pdf')),
            Data=identity(path.with_suffix('.json')),Caption=identity(path.with_suffix('.txt'))))
    from article_presentation import render_figures, table_pdf
    render_figures(out,catalog,profiles,core,record,inputs,report_dispositions)
    def simple_table(title,sections,widths,headings,notes,fontsize=9):
        table_pdf(out,title,sections,widths,headings,notes,fontsize)

    title='Table 1 - Model primitives';b=core('rn','american')['Parameters']
    primitives=[['Merits and truth','Q is uniform on [0,1]; true liability T | Q is Bernoulli(Q).'],
       ['Signals',f"{b['Signals']} private signal bins per party; party noise {b['PartySigma']}; court noise {b['CourtSigma']}; two court findings."],
       ['Damages and wealth','Damages 1; initial wealth 10 per party. Monetary quantities are in units of damages.'],
       ['Preferences','Risk neutral or symmetric CARA risk aversion with alpha = 2.'],
       ['Costs',f"Filing / answering: {b['EntryCost']} each; additional trial costs: {b['TrialCost']} each; ordinary multiplier 1."],
       ['Private exit commitments','After filing and answering, each party commits whether to exit if bargaining fails.'],
       ['Agreement and offers','Simultaneous agreement; offers only if both agree. Separate information sets; own commitment is remembered.'],
       ['Offer actions',', '.join(f'{v:.2f}' for v in b['Offers'])+'; overlapping offers settle at their midpoint.'],
       ['Unsuccessful bargaining','Apply private exit commitments: abandonment, default, mutual-exit lottery, or trial. Refusal is not a terminal disposition.'],
       ['Fee rules','American: own costs. British: loser pays at trial and the specified unilateral exits. Trial-only fee shifting is a separate cost-1 extension.']]
    simple_table(title,[('Baseline specification; case-specific departures are reported in the robustness materials',primitives)],[156,620],['Primitive','Value / interpretation'],['Continuous merits are integrated. The signal, agreement and offer decisions retain their distinct information sets and original timing.'],8.7)
    record('Tables',title,dict(Baseline=core('rn','american'),Rows=primitives),'Baseline model primitives. Monetary values are in units of damages. The American/British comparison is the main specification; trial-only fee shifting appears only as an extension at ordinary costs.')

    selections=read(SELECT)
    for idx,indices,name in [(2,[0],'Strategy mechanisms'),(3,[1,2,3],'Risk-averse strategy changes')]:
        title=f'Table {idx} - {name}';panels=[selections['Panels'][i] for i in indices];sections=[]
        for panel in panels:
            rows=[]
            for label,row in zip(LABELS,panel['Rows']):
                assert row['Eligible'];history='--' if row['ExitCommitment'] is None else ('E' if row['ExitCommitment']==1 else 'C')
                rows.append([label,f"{row['Signal']:.2f}",history,row['Action'],f"{100*row['SourceProbability']:.1f} > {100*row['TargetProbability']:.1f}",f"{100*row['SourceReach']:.2f} > {100*row['TargetReach']:.2f}",*[('--' if row['CounterfactualUndefined'] else number(row['Allocation'][f],1,True)) for f in FIELDS]])
            sections.append((panel['Title'],rows))
        simple_table(title,sections,[93,32,27,35,71,79,48,48,48,48,48],
            ['Decision','Signal','Own exit','Action','Action %','Reach %','Direct','Entry','Offers','Exit','Agree'],[
            'One information set per decision family: largest absolute action-probability change among histories reached at both endpoints; stable ties.',
            'Action/reach: source > target. E/C: committed exit/continue. Contributions average all 24 replacement orders; full reconciliation remains in Sources.',
            'Complete supports, reach probabilities, hybrid values and diagnostic sensitivities accompany the full tables in Equilibrium strategy changes.'],7.4)
        record('Tables',title,dict(Source=identity(SELECT),Panels=panels),
            'Selected strategic-response decompositions at cost multiplier 1. The fixed selection rule retains eligible zero-change rows. Direct reoptimizes own continuation after changing the rule/preferences; opponent-entry, offer, exit and agreement contributions average all 24 replacement orders. The full reconciliation and diagnostics are retained in Sources; they are omitted from the display. These selected information sets are illustrations, not population-average causal effects.')

    title='Table 5 - Overall results summary';records=[];sections=[]
    inv=read(ROOT/'planning/Revised plan data/equilibrium-inventory.plan.json')['cases']
    for risk in ('rn','ra'):
        alpha=0 if risk=='rn' else 2;rows=[]
        order={'baseline':0,'cost-multiplier':0,'cost-timing':1,'private-noise':2,'court-noise':3,'grid':4,'merits-distribution':5,'direct-binary':6}
        ordered=sorted(inv,key=lambda x:(order.get(x['case_id'].split('__')[0],9), x['cost_multiplier'] if 'cost_multiplier' in x else x['case_id']))
        for item in ordered:
            if item['fee_rule']!='complete' or item['alpha_p']!=alpha or item['alpha_d']!=alpha:continue
            bid=item['case_id'];aid=bid.replace('__complete__','__american__')
            if 'cost-' not in bid:raise ValueError(bid)
            bcase=case_by_id.get(bid);acase=case_by_id.get(aid)
            bits=bid.split('__');label=(f'Cost multiplier {bits[-1][5:].replace("p",".")}' if bits[0] in ('baseline','cost-multiplier') else {
                'merits-distribution':'Merits: '+bits[1].replace('-',' '),
                'private-noise':'Private noise '+bits[1].replace('sigma-','').replace('p','.'),
                'court-noise':'Court noise '+bits[1].replace('sigma-','').replace('p','.'),
                'cost-timing':'Costs: '+bits[1].replace('-',' '),
                'grid':'Grid: '+bits[1].replace('signals-','').replace('-offers-',' signals / ')+' offers',
                'direct-binary':'Calibrated direct binary'}.get(bits[0],bits[0]+': '+bits[1]))
            if acase and bcase:
                diffs=[bcase['Welfare']['Headline'][k]-acase['Welfare']['Headline'][k] for k in MEASURES]
                trial=100*(bcase['ParticipationAndDispositions']['Trial']-acase['ParticipationAndDispositions']['Trial'])
                settle=100*(bcase['ParticipationAndDispositions']['Settlement']-acase['ParticipationAndDispositions']['Settlement'])
                rows.append([label,*[number(v,3,True) for v in diffs],number(trial,1,True),number(settle,1,True)])
                records.append(dict(American=aid,British=bid,Status='audited',Differences=dict(zip(MEASURES,diffs)),TrialPercentagePoints=trial,SettlementPercentagePoints=settle))
            else:
                rows.append([label,*['Pending']*7]);records.append(dict(American=aid,British=bid,Status='pending',Missing=[i for i in (aid,bid) if i not in case_by_id]))
        c=next(c for c in catalog['Cases'] if c['Parameters']['FeeRule']=='trial-only' and c['Parameters']['CostMultiplier']==1 and c['Parameters']['AlphaP']==(0 if risk=='rn' else 2));a=core(risk,'american')
        diffs=[c['Welfare']['Headline'][k]-a['Welfare']['Headline'][k] for k in MEASURES];trial=100*(c['ParticipationAndDispositions']['Trial']-a['ParticipationAndDispositions']['Trial']);settle=100*(c['ParticipationAndDispositions']['Settlement']-a['ParticipationAndDispositions']['Settlement'])
        trialrow=['Trial-only fee shifting',*[number(v,3,True) for v in diffs],number(trial,1,True),number(settle,1,True)];records.append(dict(American=a['CaseId'],TrialOnly=c['CaseId'],Status='audited',Differences=dict(zip(MEASURES,diffs)),TrialPercentagePoints=trial,SettlementPercentagePoints=settle))
        after=max(i for i,row in enumerate(rows) if row[0].startswith('Costs:'))+1
        rows.insert(after,trialrow)
        # Asymmetric preference cases do not belong under symmetric RN/RA headings.
        for start in range(0,len(rows),24):sections.append((('Risk neutral' if risk=='rn' else 'Symmetric risk aversion')+' | continuation' if start else ('Risk neutral' if risk=='rn' else 'Symmetric risk aversion')+' | British minus American',rows[start:start+24]))
    extra=[]
    for c in catalog['Cases']:
        p=c['Parameters']
        if p['Family']=='asymmetric-risk' and p['FeeRule']=='complete':
            a=case_by_id[c['CaseId'].replace('__complete__','__american__')];diffs=[c['Welfare']['Headline'][k]-a['Welfare']['Headline'][k] for k in MEASURES]
            trial=100*(c['ParticipationAndDispositions']['Trial']-a['ParticipationAndDispositions']['Trial']);settle=100*(c['ParticipationAndDispositions']['Settlement']-a['ParticipationAndDispositions']['Settlement'])
            extra.append([{'p-only-ra':'Plaintiff-only risk aversion','d-only-ra':'Defendant-only risk aversion'}[p['Variant']],*[number(v,3,True) for v in diffs],number(trial,1,True),number(settle,1,True)]);records.append(dict(American=a['CaseId'],British=c['CaseId'],Status='audited',Differences=dict(zip(MEASURES,diffs)),TrialPercentagePoints=trial,SettlementPercentagePoints=settle))
    sections.append(('Asymmetric risk aversion | British minus American',extra))
    simple_table(title,sections,[254,76,76,73,73,73,75,75],['Specification',*MABBR,'Trial (pp)','Settle (pp)'],[
        'Positive numbers mean a larger value under the shifting rule. Columns are different measures, not counts of signs or a combined welfare ranking.',
        'Non-cost extensions use cost multiplier 1. RN/RA use alpha 0/2; asymmetric rows state which party is risk averse. Full levels are in Sources.',
        'Pending denotes the two running British risk-averse grid profiles. No missing value is replaced by zero or an earlier model result.'],7.5)
    record('Tables',title,dict(Catalog=identity(CAT),Comparisons=records,Cases=[c for c in catalog['Cases'] if c['Parameters']['FeeRule']!='trial-only' or c['Parameters']['CostMultiplier']==1],Complete=not any(r['Status']=='pending' for r in records)),
        'Signed shifts relative to the matched American-rule equilibrium in the revised design. Monetary columns use damages; trial and settlement use percentage points among all potential disputes. Trial-only fee shifting is confined to the ordinary-cost extension. The two missing grid comparisons remain explicitly pending; this table is staged, not ready for complete-collection publication.')

    title='Table 6 - Disposition ranges';group=read(GROUP);assert group['Complete'] and group['RequestedStarts']==200 and group['AcceptedStarts']==199
    accepted=defaultdict(list)
    for attempt in group['Attempts']:
        if attempt['Accepted']:
            p=read(verify(attempt['Profile']));accepted[attempt['Case']].append(p)
    metrics=['Filing','JointFileAnswer','Settlement','Abandonment','Default','Trial'];labels=['Files','Files and answers','Settles','P abandons','D defaults','Trial'];ranges=[];sections=[]
    for risk in ('rn','ra'):
        rows=[]
        for key,label in zip(metrics,labels):
            cells=[]
            for rule,_ in RULES:
                caseid=core(risk,rule)['CaseId'];vals=[100*p['Metrics'][key] for p in accepted[caseid]]
                lo,hi=min(vals),max(vals);base=100*cp(risk,rule)['Metrics'][key];cells.extend([number(base,2),number(lo,2)+' - '+number(hi,2)])
                ranges.append(dict(CaseId=caseid,Metric=key,Accepted=len(vals),MinimumPercent=lo,MaximumPercent=hi,ExactPrimaryPercent=base))
            rows.append([label,*cells])
        sections.append((('Risk neutral: 50 American / 50 British accepted' if risk=='rn' else 'Risk averse: 50 American / 49 British accepted')+' | 50 attempted starts per setting',rows))
    supplement=out/'Supplemental materials/Multiple equilibria/Sources'
    supplement.mkdir(parents=True)
    save_new(supplement/'disposition-ranges.json',dict(Grouping=identity(GROUP),Ranges=ranges,Attempts=200,Accepted=199))
    from multiple_welfare_figure import generate
    artifacts.append(generate(out,write_manifest=False))

    for artifact in artifacts:
        pdf=pathlib.Path(artifact['PDF']['Path']);stem=artifact['Title'];pages=out/'review-pages'/stem;pages.mkdir()
        command=['pdftoppm','-r','135','-png',str(pdf),str(pages/'page')]
        subprocess.run(command,check=True,creationflags=subprocess.CREATE_NO_WINDOW,capture_output=True)
        pngs=sorted(pages.glob('page-*.png'));assert pngs
        artifact['Pages']=[identity(p) for p in pngs];artifact['RenderCommand']=command
        for i,p in enumerate(pngs):shutil.copy2(p,out/artifact['Folder']/(stem+('' if len(pngs)==1 else f' - page {i+1}')+'.png'))
    import pdfplumber
    for a in artifacts:
        with pdfplumber.open(a['PDF']['Path']) as pdf:
            for p in pdf.pages:
                assert all(c['x0']>=-.1 and c['x1']<=p.width+.1 and c['top']>=-.1 and c['bottom']<=p.height+.1 for c in p.chars),a['Title']
    for folder in ('Figures','Tables'):
        shutil.copy2(__file__,out/folder/'Sources'/pathlib.Path(__file__).name)
    save_new(out/'manifest.json',dict(Schema='preserved-numbered-article-exhibits-v1',CreatedUtc=utc(),Generator=identity(__file__),Inputs=inputs,
        Artifacts=artifacts,NumberedFigures=8,NumberedTables=4,PrimaryProfiles=80,ExpectedProfiles=82,AutomatedChecksPassed=True,VisualReviewPending=True,
        SolvesStarted=0,ScientificReplayJobsStarted=0,CompleteArticle=False,MissingProfiles=catalog['MissingAuditedCaseIds']))
    (out/'README.md').write_text('# Numbered article exhibits\n\nEight figures and four tables retain the article order. Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria. Other file numbers are preserved to avoid unrelated cross-reference changes. Sources include unrounded data, complete policies and captions. Disposition ranges remain in the supplement. The two missing grid comparisons in Table 5 are explicitly pending. No manuscript, user repository or running job was changed.\n\n'+ '\n'.join('- ['+a['Title']+']('+a['Folder']+'/'+a['Title']+'.pdf)' for a in artifacts)+'\n',encoding='utf-8')
    print(f'Prepared {len(artifacts)} numbered exhibits; visual review pending; two grid comparisons remain pending.')

if __name__=='__main__':main()
