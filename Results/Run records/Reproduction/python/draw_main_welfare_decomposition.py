"""Render the ten validated main welfare contrasts without starting any solver."""
import argparse
import csv
import pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FuncFormatter
from article_release import identity, read, save_new, utc, verify

FIELDS = [
    ('Meritorious plaintiff shortfall', 'MeritoriousPlaintiffShortfall', 'Meritorious plaintiff\nshortfall'),
    ('Nonliable defendant burden', 'NonliableDefendantBurden', 'Nonliable defendant\nburden'),
    ('Liable defendant excess burden', 'LiableDefendantExcessBurden', 'Liable defendant\nexcess burden'),
    ('Gross outcome error', 'GrossOutcomeError', 'Gross outcome\nerror'),
    ('Real litigation expenditures', 'RealLitigationExpenditures', 'Real litigation\nexpenditures'),
]
COSTS = [.25, .5, 1, 2, 4]
SERIES = [('MechanicalRuleEffect', 'Mechanical rule effect', '#d18429', 's'),
          ('BehavioralEffect', 'Behavioral effect', '#168b91', 'o'),
          ('TotalDifference', 'Total difference', '#242c3a', 'D')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=pathlib.Path, required=True)
    parser.add_argument('--wave', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    catalog, wave = read(args.catalog), read(args.wave)
    assert wave['Passed'] and verify(wave['Catalog']) == args.catalog.resolve()
    cases = {c['CaseId']: c for c in catalog['Cases']}
    rows, selected, sources = [], {}, []
    max_residual = 0
    max_zero_mechanical_residual = 0
    for item in wave['Validated']:
        validation_path = verify(item)
        validation = read(validation_path)
        assert validation['Passed'] and validation['CompleteEndpointValuesIdentical']
        request_path = verify(validation['Request'])
        request = read(request_path)
        a, b = request['American']['Case'], request['Complete']['Case']
        if a['OriginalOptionName'] is None or b['OriginalOptionName'] is None:
            continue
        assert a['FeeRule'] == 'american' and b['FeeRule'] == 'complete'
        assert a['AlphaP'] == a['AlphaD'] == b['AlphaP'] == b['AlphaD']
        assert a['CostMultiplier'] == b['CostMultiplier']
        key = (a['AlphaP'], a['CostMultiplier'])
        assert key not in selected and key[0] in [0, 2] and key[1] in COSTS
        verified_outputs = [verify(f) for f in validation['Outputs']]
        data_path, = [p for p in verified_outputs if p.name == 'decomposition.json']
        data = read(data_path)
        assert data['Passed'] and data['Id'] == request['Id']
        assert request['TruthMapExponents'] == [1.0]
        for path, sha in data['Inputs'].items():
            verify(dict(Path=path, Sha256=sha))
        selected[key] = data['Components']
        sources.append(dict(Validation=identity(validation_path), Request=identity(request_path),
                            Decomposition=identity(data_path)))
        for label, field, _ in FIELDS:
            component = data['Components'][label]
            aa = component['AmericanWithAmericanProfile']
            ba = component['CompleteWithAmericanProfile']
            ab = component['AmericanWithCompleteProfile']
            bb = component['CompleteWithCompleteProfile']
            assert aa == cases[a['Id']]['Welfare']['Headline'][field]
            assert bb == cases[b['Id']]['Welfare']['Headline'][field]
            expected = {'MechanicalRuleEffect': .5 * ((ba-aa)+(bb-ab)),
                        'BehavioralEffect': .5 * ((ab-aa)+(bb-ba)),
                        'TotalDifference': bb-aa}
            for name, value in expected.items():
                assert abs(component[name] - value) <= 1e-10
            residual = component['MechanicalRuleEffect'] + component['BehavioralEffect'] - component['TotalDifference']
            assert abs(residual) <= 1e-10
            max_residual = max(max_residual, abs(residual))
            if field in ['GrossOutcomeError', 'RealLitigationExpenditures']:
                # Existing reports use double accumulation; retain the actual
                # stored value, including any rounding residue, in CSV/plots.
                assert abs(component['MechanicalRuleEffect']) <= 1e-10
                max_zero_mechanical_residual = max(max_zero_mechanical_residual, abs(component['MechanicalRuleEffect']))
            rows.append(dict(Risk='Risk neutral' if key[0] == 0 else 'Risk averse',
                             CostMultiplier=key[1], Measure=label, AmericanCase=a['Id'], BritishCase=b['Id'],
                             **component))
    assert set(selected) == {(risk, cost) for risk in [0, 2] for cost in COSTS}
    args.output.mkdir(parents=True, exist_ok=False)
    with (args.output/'welfare-decomposition.csv').open('x', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.spines.left': False})
    fig, axes = plt.subplots(2, 5, figsize=(16, 10.7))
    fig.subplots_adjust(left=.075, right=.975, top=.81, bottom=.16, wspace=.26, hspace=.45)
    fig.suptitle('Why outcomes differ: British minus American', x=.075, ha='left', y=.984,
                 fontsize=20, weight='bold')
    fig.text(.075, .945, 'Mechanical fee-rule effects and behavioral changes across the full main cost comparison', fontsize=12)
    legend = [Line2D([0], [0], color=color, marker=marker, linestyle='', markersize=7, label=label)
              for _, label, color, marker in SERIES]
    fig.legend(handles=legend, loc='upper left', bbox_to_anchor=(.069, .925), ncol=3, frameon=False)
    for ri, risk in enumerate([0, 2]):
        for j, (label, _, title) in enumerate(FIELDS):
            ax = axes[ri, j]
            values = [components[label][name] for components in selected.values() for name, *_ in SERIES]
            bound = max(abs(v) for v in values) * 1.15
            ax.set_xlim(-bound, bound)
            ax.set_ylim(4.6, -.6)
            ax.set_yticks(range(5), [f'×{v:g}' for v in COSTS] if j == 0 else [])
            ax.set_title(title, fontsize=11, pad=10)
            ax.xaxis.set_major_locator(MaxNLocator(5, symmetric=True))
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}' if abs(x)>1e-10 else '0'))
            ax.grid(axis='x', alpha=.15)
            ax.set_axisbelow(True)
            for i, cost in enumerate(COSTS):
                ax.axhspan(i-.48, i+.48, color='#f1f4f5' if i % 2 == 0 else 'white', zorder=0)
                for k, (name, _, color, marker) in enumerate(SERIES):
                    value = selected[(risk, cost)][label][name]
                    y = i + (k-1)*.24
                    ax.plot([0, value], [y, y], color=color, lw=1.2, alpha=.7, zorder=2)
                    ax.scatter(value, y, c=color, marker=marker, s=30, zorder=3)
            ax.axvline(0, color='#848a90', linewidth=.85, zorder=1)
            ax.tick_params(axis='y', length=0)
            ax.tick_params(axis='x', labelsize=9)
            if j == 0:
                ax.set_ylabel('Cost multiplier', labelpad=10)
        axes[ri, 0].text(0, 1.26, 'Risk neutral' if risk == 0 else 'Risk averse (CARA α = 2)',
                         transform=axes[ri, 0].transAxes, fontsize=15, weight='bold')
    fig.text(.075, .105, 'Negative values: lower under British. Positive values: higher under British. Components sum to the total.', fontsize=10)
    fig.text(.075, .073, 'Symmetric decomposition: average each effect over both orders of changing the rule and the complete strategy profile.\nMechanical effects hold behavior fixed; behavioral effects hold the rule fixed. Gross error and real expenditures have zero mechanical effect.', fontsize=9, linespacing=1.5)
    fig.text(.075, .025, 'All 20 selected exact profiles audited; 10 matched contrasts. Monetary units: damages = 1. Identity truth mapping.\nWithin a measure, both risk panels use the same scale. This is a welfare decomposition, not a multiple-equilibrium search.', fontsize=9, color='#444444')
    for extension in ['png', 'svg']:
        fig.savefig(args.output/f'welfare-decomposition.{extension}', dpi=160)
    plt.close(fig)
    save_new(args.output/'manifest.json', dict(Schema='main-welfare-decomposition-figure-v1', CreatedUtc=utc(),
             Catalog=identity(args.catalog), Wave=identity(args.wave), Generator=identity(__file__),
             SourceContrasts=sources, Pairs=10, MeasuresPerPair=5, Rows=len(rows),
             ExactEndpointValuesIdentical=True, AdditiveCheckTolerance=1e-10, MaxAbsoluteResidual=max_residual,
             MechanicalZeroCheckTolerance=1e-10, MaxMechanicalZeroResidual=max_zero_mechanical_residual,
             ReportValuesUnchanged=True, TruthMapExponents=[1.0], SolvesStarted=0,
             Files=[identity(p) for p in sorted(args.output.iterdir()) if p.is_file()]))
    print(f'Validated and rendered {len(rows)} unrounded decomposition rows: {args.output}')


if __name__ == '__main__':
    main()
