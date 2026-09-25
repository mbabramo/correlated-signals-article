"""Editable three-page strategy exhibits from one independently audited profile.

All saved probabilities are retained. Off-path policies are explicitly distinguished
from reached conditional behavior. Only exact zeros receive empty heatmap labels.
"""
import argparse
import json
import pathlib
import shutil
import sys

from article_release import ROOT, identity, read, save_new, utc, verify
from build_profile_catalog import validate_profile, risk_label


def tex(value):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
                    '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(c, c) for c in str(value))


def printed(value):
    if value is None:
        return 'undefined'
    # Never print a nonzero probability as zero.
    return f'{value:.4g}' if value != 0 else '0'


def title(case):
    fee = {'american': 'American', 'complete': 'British', 'trial-only': 'Trial-only fee shifting'}[case['FeeRule']]
    family = 'Standard model' if case['IsExternalImport'] else case['Family'] + ' / ' + case['Variant']
    return f'{family}; {fee}; {risk_label(case)}; cost multiplier {case["CostMultiplier"]:g}'


def probability_plot(rows, heading):
    rows = sorted(rows, key=lambda r: r['Signal'])
    if not rows or len({row['Signal'] for row in rows}) != len(rows):
        raise ValueError('Expected exactly one policy for each signal in this panel')
    n = len(rows)
    points, off_path = [], []
    for row in rows:
        if row['Actions'] != ['Yes', 'No']:
            raise ValueError('The displayed Yes probability requires explicit Yes/No action labels')
        value = row['Probabilities'][0]
        pair = f'({row["Signal"]},{value:.17g})'
        (points if row['Reach'] > 0 else off_path).append(pair)
    return (r'\begin{tikzpicture}\begin{axis}[' +
            f'width=4.85in,height=2.5in,title={{{tex(heading)}}},' +
            f'xmin=.5,xmax={n + .5:g},ymin=0,ymax=1,xtick={{1,...,{n}}},ytick={{0,.25,.5,.75,1}},' +
            r'xlabel={Private signal},ylabel={Probability of Yes},grid=major,' +
            r'tick label style={font=\small},label style={font=\small},title style={font=\normalsize},clip=false]' + '\n' +
            r'\addplot[only marks,mark=*,mark size=2pt,color=navy] coordinates {' + ' '.join(points) + '};\n' +
            r'\addplot[only marks,mark=o,mark size=2.4pt,color=gray] coordinates {' + ' '.join(off_path) + '};\n' +
            r'\end{axis}\end{tikzpicture}')


def offer_matrix(rows, offers, heading, wide=False):
    rows = sorted(rows, key=lambda r: r['Signal'])
    if not rows or len(rows) != len({r['Signal'] for r in rows}):
        raise ValueError('Expected one complete offer distribution per signal/commitment')
    n, m = len(rows), len(offers)
    labels = [str(r['Signal']) + ('*' if r['Reach'] == 0 else '') for r in rows]
    lines = [r'\begin{tikzpicture}\begin{axis}[',
             f'width={10.0 if wide else 4.85}in,height=2.55in,title={{{tex(heading)}}},',
             f'xmin=.5,xmax={m+.5:g},ymin=.5,ymax={n+.5:g},y dir=reverse,',
             f'xtick={{1,...,{m}}},xticklabels={{{",".join(f"{v:.3g}" for v in offers)}}},',
             f'ytick={{1,...,{n}}},yticklabels={{{",".join(labels)}}},',
             r'xlabel={Offer (damages = 1)},ylabel={Private signal},',
             r'tick label style={font=\scriptsize},label style={font=\small},title style={font=\normalsize},',
             r'colormap={policy}{color(0cm)=(white);color(1cm)=(navy)},point meta min=0,point meta max=1,',
             r'axis on top,clip=false]',
             r'\addplot[matrix plot*,mesh/cols=' + str(m) + r',point meta=explicit] table[meta=p] {', 'x y p']
    for y, row in enumerate(rows, 1):
        # The production action-label formatter prints offers to two decimals.
        # Coordinates were independently audited; plot their full declared support,
        # checking labels against that display convention rather than rounded game values.
        display_offers = [float(f'{value:.2f}') for value in offers]
        if len(row['Probabilities']) != m or [float(s) for s in row['Actions']] != display_offers:
            raise ValueError('Offer action labels do not match the fixed complete support')
        for x, p in enumerate(row['Probabilities'], 1):
            lines.append(f'{x} {y} {p:.17g}')
    lines.append('};')
    for y, row in enumerate(rows, 1):
        for x, p in enumerate(row['Probabilities'], 1):
            if p == 0:
                continue
            color = 'white' if p >= .55 else 'black'
            label = printed(p)
            if 'e' in label:
                mantissa, exponent = label.split('e')
                label = '$' + mantissa + r'\!\times\!10^{' + str(int(exponent)) + '}$'
            font = r'\tiny' if m > 10 and not wide else r'\scriptsize'
            lines.append(r'\node[font=' + font + ',text=' + color + f'] at (axis cs:{x},{y}) {{{label}}};')
    lines.append(r'\end{axis}\end{tikzpicture}')
    return '\n'.join(lines)


def source(audit, profile):
    metrics = validate_profile(audit, profile)
    case = audit['Case']
    rows = profile['Strategies']

    def select(decision, own_exit=None):
        result = [row for row in rows if row['Decision'] == decision and row['OwnExit'] == own_exit]
        if len(result) != case['Signals']:
            raise ValueError('Missing complete signal/decision policies: ' + decision)
        return result

    header = r'\noindent{\Large\bfseries ' + tex(title(case)) + r'}\par\smallskip' + '\n' + \
             r'{\footnotesize Case: \texttt{' + tex(case['Id']) + r'}. Primary profile 1; agreement enabled.}\par\medskip' + '\n'
    lines = [r'\documentclass[10pt]{article}',
             r'\usepackage[paperwidth=11in,paperheight=8.5in,margin=.4in,footskip=16pt]{geometry}',
             r'\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{pgfplots}\usepackage{booktabs}',
             r'\pgfplotsset{compat=1.18}\definecolor{navy}{RGB}{25,69,102}',
             r'\pagestyle{plain}\setlength{\parindent}{0pt}', r'\begin{document}', header,
             r'{\large\bfseries Filing, answering and private exit commitments}\par\smallskip',
             r'Filled dots: reached conditional policy. Hollow gray dots: saved off-path policy; the conditional event is undefined.\par',
             r'Exit commitments occur privately before the simultaneous agreement decisions.\par\medskip',
             r'\begin{tabular}{@{}cc@{}}',
             probability_plot(select('PFile'), 'Plaintiff: file') + '&' + probability_plot(select('DAnswer'), 'Defendant: answer given filing') + r'\\',
             probability_plot(select('PAbandon'), 'Plaintiff: commit to abandon if bargaining fails') + '&' + probability_plot(select('DDefault'), 'Defendant: commit to default if bargaining fails'),
             r'\end{tabular}\par\smallskip',
             r'{\small Filing: ' + printed(metrics['Filing']) + '; joint filing/answering: ' + printed(metrics['JointFileAnswer']) +
             '; answering given filing: ' + printed(metrics['AnsweringGivenFiling']) + '.}\n',
             r'\newpage', header,
             r'{\large\bfseries Agreement conditional on private signal and own exit commitment}\par\smallskip',
             r'Both parties choose without observing the other party\textquotesingle s agreement choice or private exit commitment.\par',
             r'Offers occur only if both agree. Refusal activates the original commitment-dependent outcomes.\par\medskip',
             r'\begin{tabular}{@{}cc@{}}',
             probability_plot(select('PAgreeToBargain', 1), 'Plaintiff agrees | committed to abandon') + '&' +
             probability_plot(select('DAgreeToBargain', 1), 'Defendant agrees | committed to default') + r'\\',
             probability_plot(select('PAgreeToBargain', 2), 'Plaintiff agrees | committed to continue') + '&' +
             probability_plot(select('DAgreeToBargain', 2), 'Defendant agrees | committed to contest'),
             r'\end{tabular}\par\smallskip',
             r'{\small Joint agreement-stage reach: ' + printed(metrics['AgreementStageReach']) + r'. Conditional joint outcomes: both agree ' +
             printed(metrics['BothAgreeGivenStage']) + '; only P declines ' + printed(metrics['OnlyPlaintiffDeclinesGivenStage']) +
             '; only D declines ' + printed(metrics['OnlyDefendantDeclinesGivenStage']) + '; both decline ' + printed(metrics['BothDeclineGivenStage']) +
             r'. These use the full joint signal/history distribution. Hollow dots retain saved off-path policies.}',
             ]
    offer_header = [r'\newpage', header,
        r'{\large\bfseries Complete mixed offer distributions}\par\smallskip',
        r'Rows show the saved policy at each private signal and own commitment, after both parties agree to bargain.\par',
        r'An asterisk marks an unreachable information set: its saved completion is shown, but no reached conditional distribution exists.\par\medskip']
    legend = [r'{\small Color and cell labels show action probabilities (white = 0; darkest blue = 1). Empty cell labels mean exact zero.',
        r'Every positive entry is printed, including arbitrarily small probabilities. Full precision is retained in the editable TeX and profile JSON.}']
    if len(case['Offers']) > 10:
        for decision, label, first, second in [('POffer','Plaintiff','abandon','continue'),('DOffer','Defendant','default','contest')]:
            lines += offer_header + [offer_matrix(select(decision,1),case['Offers'],label+' | committed to '+first,wide=True),
                r'\par\medskip',offer_matrix(select(decision,2),case['Offers'],label+' | committed to '+second,wide=True),
                r'\par\smallskip'] + legend
    else:
        lines += offer_header + [r'\begin{tabular}{@{}cc@{}}',
            offer_matrix(select('POffer', 1), case['Offers'], 'Plaintiff | committed to abandon') + '&' +
            offer_matrix(select('DOffer', 1), case['Offers'], 'Defendant | committed to default') + r'\\',
            offer_matrix(select('POffer', 2), case['Offers'], 'Plaintiff | committed to continue') + '&' +
            offer_matrix(select('DOffer', 2), case['Offers'], 'Defendant | committed to contest'),
            r'\end{tabular}\par\smallskip'] + legend
    lines.append(r'\end{document}')
    return '\n'.join(lines)


def build(catalog_path, case_id, output):
    catalog_path, output = pathlib.Path(catalog_path).resolve(), pathlib.Path(output).resolve()
    if not output.is_relative_to(ROOT / 'reporting') or output == ROOT / 'reporting':
        raise ValueError('Keep exhibit preparation isolated')
    catalog = read(catalog_path)
    if catalog['Schema'] != 'audited-exact-primary-catalog-v1':
        raise ValueError('Expected audited primary catalog')
    case = next(c for c in catalog['Cases'] if c['CaseId'] == case_id)
    audit_path, profile_path = verify(case['Audit']), verify(case['CompleteProfile'])
    audit, profile = read(audit_path), read(profile_path)
    for file in audit['Outputs']:
        verify(file)
    content = source(audit, profile)
    output.mkdir(parents=True, exist_ok=False)
    sources = output / 'Sources'
    sources.mkdir()
    (sources / 'strategy.tex').write_text(content, encoding='utf-8', newline='\n')
    shutil.copy2(profile_path, sources / 'complete-profile.json')
    shutil.copy2(audit_path, sources / 'individual-audit.json')
    # Frozen generator copies preserve the exact authoring implementation.
    for name in ('individual_strategy_sources.py', 'build_profile_catalog.py', 'article_release.py'):
        shutil.copy2(ROOT / 'scripts' / name, sources / name)
    save_new(output / 'source-manifest.json', dict(Schema='complete-primary-strategy-exhibit-v1', CreatedUtc=utc(),
        CaseId=case_id, Catalog=identity(catalog_path), Audit=case['Audit'], CompleteProfile=case['CompleteProfile'],
        CompleteInformationSets=len(profile['Strategies']), CompleteActionEntries=sum(len(r['Probabilities']) for r in profile['Strategies']),
        ProbabilityCutoff=None, OffPathPoliciesRetained=True, JointOutcomesFromFullHistoryDistribution=True,
        ExpectedPages=4 if len(audit['Case']['Offers']) > 10 else 3, Command=sys.argv, Cwd=str(pathlib.Path.cwd()),
        Files=[identity(path) for path in sorted(sources.iterdir())], RenderingAndVisualQAPending=True, SolvesStarted=0))
    print(json.dumps(dict(CaseId=case_id, ExpectedPages=4 if len(audit['Case']['Offers']) > 10 else 3, Output=str(output), SolvesStarted=0)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', required=True, type=pathlib.Path)
    parser.add_argument('--case', required=True)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    args = parser.parse_args()
    build(args.catalog, args.case, args.output)
