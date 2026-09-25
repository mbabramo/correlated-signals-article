"""Make factual substitutions and explicit editorial marks without rewriting analysis."""
import csv, pathlib, re, shutil
from article_release import ROOT, ARTICLE, identity, read, save_new, utc

WORK=ROOT/'work/manuscript-marked-20260925-v3'
STAGE=ROOT/'article-staging/Article-collection-20260925-v4'
SOURCE=ARTICLE/'Article and bibliography/corr_signals.tex'
WORK.mkdir(parents=True,exist_ok=False)
man=WORK/'Article and bibliography';man.mkdir()
original=SOURCE.read_text(encoding='utf-8-sig');text=re.sub(r'(?m)^[ \t]+$','',original);edits=[];flags=[]
def change(old,new,reason):
    global text
    assert text.count(old)==1,(old[:100],text.count(old))
    text=text.replace(old,new);edits.append(dict(Before=old,After=new,Reason=reason))
def flag(prefix,reason):
    global text
    paragraphs=text.split('\n\n');matches=[i for i,p in enumerate(paragraphs) if p.lstrip().startswith(prefix)]
    assert len(matches)==1,(prefix,len(matches))
    i=matches[0];before=paragraphs[i]
    paragraphs[i]='\\revisionnote{'+reason+'}{%\n'+before.strip()+'%\n}'
    text='\n\n'.join(paragraphs);flags.append(dict(StartsWith=prefix,Reason=reason,OriginalPassage=before))
def flag_sentence(sentence,reason):
    global text
    assert text.count(sentence)==1,sentence[:100]
    text=text.replace(sentence,'\\revisionnote{'+reason+'}{'+sentence+'}')
    flags.append(dict(OriginalPassage=sentence,Reason=reason))

change('Litigants make file, answer, offer, and quit decisions.','Litigants make file, answer, agreement-to-bargain, offer, and quit decisions.','Agreement is explicit in every current primary game.')
change('The ten-offer specifications in the present article have 45,211 nodes, while the fifteen-offer extension has 97,211 nodes.',
       'The baseline ten-signal, ten-offer specification in the present article has 47,611 nodes, while the eight-signal, fifteen-offer extension has 63,753 nodes.',
       'Frozen FinalArticleCaseTests.cs asserts the full unreduced tree counts 47,611 and 63,753.')
change('The solver uses rational arithmetic.','The primary solver uses rational arithmetic.','The multiple-start supplement uses separately validated floating-point arithmetic.')
change('Complete fee-shifting adds reimbursement','The British rule adds reimbursement','Use the agreed British label for complete fee shifting in the rule definition.')
change('reports the dispositions of potential disputes under the three fee-shifting rules with risk neutrality and ordinary costs.',
       'reports the dispositions of potential disputes under the American and British rules with risk neutrality and ordinary costs.','Figure 3 now compares American and British.')
change('(As a robustness check, an extension uses $|\\mathcal{O}|=15$ for a core subset of parameters while retaining the same signal sets.)',
       '(The grid robustness checks use 8 signals and 15 offers, 12 signals and 8 offers, and 8 signals and 8 offers.)','Approved frozen grid definitions.')
change('under the three fee-shifting rules, as well as how risk preferences affect utility.',
       'under the American and British rules and the trial-only extension, as well as how risk preferences affect utility.','Current article comparison and extension scope.')
change('In a framing where all costs are avoidable, $c_{file} = c_{answer} = 0$ and $c_{trial}=0.30$. In a framing where all costs are sunk, $c_{file} = c_{answer} = 0.30$ and $c_{trial}=0.0$ .',
       'With later costs, $c_{file} = c_{answer} = 0.075$ and $c_{trial}=0.225$. With earlier costs, $c_{file} = c_{answer} = 0.225$ and $c_{trial}=0.075$.','User-approved executed timing specifications.')
change('occurring in $88.1\\%$ of cases.','occurring in $95.9\\%$ of cases.','Audited American risk-averse primary settlement: 0.9589946146.')
change('The search requested 50 starting profiles for each fee-rule and risk-preference combination, although some searches yielded fewer verified solutions.',
       'The search requested 50 starting profiles for each of the four American/British and risk-preference combinations (200 starts), of which 199 passed the approximate acceptance criteria.',
       'Current completed 200-start catalog; accepted profiles are not counted as distinct exact equilibria.')
change('settlement ranged from $13.8\\%$ to $92.7\\%$.','settlement ranged from $13.8\\%$ to $95.9\\%$.','Current American RA accepted-profile range in Table 6.')
change('expenditures ranged from $0.181$ to $0.336$','expenditures ranged from $0.182$ to $0.336$','Current accepted American RA min 0.18154673856 and max 0.33562143579, rounded to three decimals.')
change('the gross outcome range was $0.276$ to $0.373$','the gross outcome range was $0.276$ to $0.399$','Current accepted American RA min 0.27623480547 and max 0.39890577602.')

flag_sentence("The effects of fee shifting depend markedly on whether fee shifting is triggered only at trial or also by nonanswer or pretrial withdrawal. Complete fee shifting induces defendants to answer whenever sued and can thereby discourage filing, worsening meritorious plaintiffs' recovery relative to trial-only fee shifting while benefiting nonliable defendants under risk neutrality.",
              'Abstract findings describe the old game. The current British profiles do not have universal answering; revise the summary using the agreement-enabled results.')
for prefix,reason in [
 ('The comparison of fee-shifting rules illustrates','The old fee-rule mechanism and welfare conclusion are superseded; use the current American--British comparison and agreement channel.'),
 ('This is not a just so story','The decomposition method remains relevant, but the asserted answering mechanism must be checked against the new selected decompositions.'),
 ('The wrinkle added by extending fee shifting','The universal-answering claim, including its claimed robustness, is contradicted by the current primary and multiple-start results.'),
 ('The bargaining protocol used is','The sequence now includes simultaneous agreement decisions, whose outcomes are observed before offers; offers occur only when both agree. Add that stage and explain refusal.'),
 ('Figure \\ref{fig:worked-equilibrium-path} illustrates','The worked path has been regenerated. Information-set numbers, the mixed filing example and descriptions of its panels must be read from the new figure.'),
 ('This part reports the principal results','The main comparison is four American/British cases, with trial-only shifting at cost 1 as an extension. The old participation conclusions no longer hold.'),
 ('The fee-shifting results may seem even more puzzling','These conditional trial rates, entry rates and the three-rule interpretation come from the previous profiles; they do not describe the current figures.'),
 ("For many signals, the parties' strategies",'The signal thresholds, offer levels and universal answering described here are superseded; use the current Figure 4, including agreement choices.'),
 ('The one-sided nature of settlements','The current British risk-neutral primary profile has no settlement. The old account of British settlements at 0.95 must be revised.'),
 ('To better appreciate the logic','Table 2 now uses the selected agreement-enabled decompositions. The old trial-only example and its stated direct contribution must be replaced or relocated.'),
 ('With the change from trial to complete','This old decomposition and universal-answering mechanism are superseded by the current selected contrasts.'),
 ('Consider first the effect of adding risk aversion','The settlement percentage has been corrected, but the offer thresholds, focal actions and causal attributions still describe the previous equilibrium.'),
 ('When risk aversion is added to the trial','The trial-only comparison is now an extension, and the stated actions and attribution must be reconciled with the current Table 3.'),
 ('Yet the most revealing decomposition','The old panel-D interpretation and universal-answering claim do not describe the current table or British risk-averse profile.'),
 ('When the meritorious plaintiff falls short','These trial-only versus complete-shifting rankings and the answering explanation refer to the old profiles. Reassess the claims using Figure 7 and current decompositions.'),
 ('Third, the parameters $\\sigma_P$','Private-signal noise and court noise are varied separately in the executed cases; this sentence currently implies a joint variation.'),
 ('Fourth, the distributions of truth and merits','Truth-conditioned latent merits is retired from the current collection. Calibrated direct binary uses the revised calibration target; distinguish merits variations from any still-undecided truth-map sensitivity.'),
 ('Fifth, the sensitivity of the offer grid','The executed grids are 8/15, 12/8 and 8/8 signals/offers, not 10/15. Two British risk-averse rows are still pending in the recorded collection.'),
 ('The noise, merits, and cost-timing alternatives','Extensions now use cost multiplier 1 and American/British comparisons. The previous full crossing with five costs and three rules is no longer the run plan.'),
 ('Table \\ref{tab:robustness-outcomes} provides','Table 5 now reports British-minus-American differences, not sign counts over 46 settings. Replace this interpretation and its universal-answering claims; two grid contrasts remain pending.'),
 ('The computational model developed here complements','The concluding universal-answering mechanism and trial-only welfare ranking are superseded. Preserve the general framing but reassess those conclusions using current results.')]:flag(prefix,reason)

flag_sentence('Because complete fee-shifting promotes defendant answering with both risk neutrality and risk aversion, the effects of fee-shifting on the average plaintiff and the defendant are not identical.',
              'The current British profiles have lower conditional answering than the American profiles; the old explanation is not supported.')
flag_sentence('The exercise produced 21, 11, and 15 profiles for the three fee-shifting rules under risk neutrality, and 12, 19, and 7 under risk aversion.',
              'These are obsolete search/group counts. The current four-case search accepted 50, 50, 50 and 49 starts; distinct-profile counts require an explicit grouping criterion and tolerance.')
flag_sentence('As shown in Table \\ref{tab:multiple-equilibria}, the multiple equilibria under risk neutrality all produced the same dispositions breakdown within each fee-shifting rule.',
              'The current risk-neutral searches show outcome variation. These are accepted approximate profiles, not a proof of distinct exact equilibria or their likelihood.')
for start,reason in [
 (r'\textit{Note:} Direct changes','The channel definitions now include agreement. The zero-contribution and numerical sensitivity examples describe the old selected rows.'),
 (r'\textit{Note:} Panels A--C','Panel identities, selected histories and the stated zero remainder/tie sensitivities must match the new three-page Table 3.')]:
    [line]=[line for line in text.splitlines() if line.strip().startswith(start)]
    flag_sentence(line,reason)

# Mechanical exhibit changes: retain labels/section locations and show every PDF page.
text=text.replace(r'Table \ref{tab:welfare-outcomes}',r'Figure \ref{fig:welfare-outcomes}')
old='''\\begin{table}[H]
    \\centering
    \\caption{Welfare outcomes under risk neutrality and risk aversion}
    \\label{tab:welfare-outcomes}
    \\includegraphics[width=\\linewidth]{../Tables/Table 4 - Welfare outcomes.pdf}
\\end{table}'''
new='''\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\linewidth]{../Figures/Figure 7 - Welfare outcomes.pdf}
    \\caption{Welfare outcomes by cost multiplier under risk neutrality and risk aversion}
    \\label{fig:welfare-outcomes}
\\end{figure}'''
change(old,new,'The approved Figure 7 replaces Table 4 in the existing Welfare Analysis location.')
change(r'\caption{Relative size of outcome variables}',r'\caption{Outcome differences: British minus American}','Current Table 5 shows differences rather than old sign-count statistics.')
manifest=read(STAGE/'Results/Run records/numbered-exhibits-manifest.json')
for title,label,caption in [
 ('Table 3 - Risk-averse strategy changes','tab:risk-averse-strategy-changes','Selected strategy changes involving risk aversion'),
 ('Table 5 - Overall results summary','tab:robustness-outcomes','Outcome differences: British minus American'),
 ('Table 6 - Disposition ranges','tab:multiple-equilibria','Range of disposition results under multiple equilibria')]:
    art=next(a for a in manifest['Artifacts'] if a['Title']==title);count=len(art['Pages'])
    pattern=re.compile(r'\\begin\{table\}\[H\](?:(?!\\end\{table\}).)*?\\label\{'+re.escape(label)+r'\}(?:(?!\\end\{table\}).)*?\\end\{table\}',re.S)
    found=pattern.findall(text);assert len(found)==1
    before=found[0];notes=before.split(r'\par\smallskip',1)[1].rsplit(r'\end{table}',1)[0] if r'\par\smallskip' in before else ''
    chunks=[]
    for n in range(1,count+1):
        chunks.append(('\\setcounter{table}{4}\n' if title.startswith('Table 5') and n==1 else '')+r'\begin{table}[H]'+'\n'+
            (r'\ContinuedFloat'+'\n' if n>1 else '')+r'\centering'+'\n'+r'\caption{'+caption+(' (continued)' if n>1 else '')+'}\n'+
            (r'\label{'+label+'}\n' if n==1 else '')+r'\includegraphics[page='+str(n)+r',width=\linewidth,height=0.71\textheight,keepaspectratio]{../Tables/'+title+'.pdf}\n'+
            (r'\par\smallskip'+notes if n==count and notes else '')+r'\end{table}')
    change(before,'\n\n'.join(chunks),'Embed all '+str(count)+' pages of the existing numbered table without changing its role.')

definition=r'''% Editorial revision marks: author prose is retained, not rewritten.
\newcommand{\revisionnote}[2]{\begingroup\itshape\textbf{[Update needed: #1]} #2\endgroup}
'''
text=text.replace(r'\begin{document}',definition+'\n'+r'\begin{document}',1)
text=text.replace(r'\maketitle',r'\maketitle'+'\n\n'+r'\noindent\textit{Editorial markings: italic passages labeled ``Update needed'' retain text requiring author revision. Only directly supported factual values and exhibit references have been updated.}',1)
assert text.count(r'\revisionnote{')==len(flags)
(man/'corr_signals.tex').write_text(text,encoding='utf-8')
for name in ('corr_signals.bib','corr_signals.bbl'):shutil.copy2(SOURCE.parent/name,man/name)
for folder in ('Figures','Tables'):
    (WORK/folder).mkdir()
    for p in (STAGE/folder).glob('*.pdf'):shutil.copy2(p,WORK/folder/p.name)
save_new(WORK/'manuscript-change-log.json',dict(CreatedUtc=utc(),Original=identity(SOURCE),Revised=identity(man/'corr_signals.tex'),FactualAndMechanicalChanges=edits,EditorialFlags=flags,
    Evidence=[identity(ROOT/'reporting/audited-primary-catalog-v13/catalog.json'),identity(ROOT/'reporting/approximate-stable-200-grouping-v1/catalog.json'),identity(ROOT/'source/ACESimTest/GameTests/FinalArticleCaseTests.cs'),identity(STAGE/'Results/Run records/numbered-exhibits-manifest.json')],
    AuthorNarrativeRewritten=False,SubstantiveConclusionsUpdated=False,PendingComparisonsPreserved=True))
print(f'Prepared {len(edits)} factual/mechanical substitutions and {len(flags)} explicit editorial flags.')
