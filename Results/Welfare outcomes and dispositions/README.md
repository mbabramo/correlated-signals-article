# Welfare outcomes and dispositions

144 saved cases; 56 cost/specification groups, each with a separate welfare-outcomes table and disposition chart.
Baseline contains the three fee rules crossed with risk neutrality/risk aversion, one pair per cost.
Extensions receive exactly the same formats for their available cases. Absence of complete fee-shifting results
in an extension is not imputed; the inventory below records coverage. Generating a saved extension does not
select it for the manuscript (in particular, the historical participation restrictions remain outside the main comparison).

Each PDF contains only its table or chart. Cost multipliers and extension names are in paths/filenames, not in the artwork.
Table headings and numeric cells are centered; fee labels are left aligned. There are no titles, captions, notes or combined packets.
PDF and PNG are insertion-ready; TeX is standalone and can be compiled directly. JSON and CSV retain the numerical data.
Captions and explanatory text belong in the manuscript or here.

## Definitions

American: each side bears its own legal expenses. Trial Fee-Shifting: loser-pays after trial.
Complete Fee-Shifting: loser-pays after trial, initial nonanswer, and later unilateral exit.
Risk averse denotes symmetric CARA alpha 2 unless a different alpha is explicitly identified.
All displayed measures and disposition shares average over all potential disputes, including unfiled disputes.
The three net monetary measures are prior-weighted meritorious-plaintiff recovery shortfall,
nonliable-defendant burden, and liable-defendant excess burden above deserved damages. They include legal costs and fee transfers.
Total expenditures count real resource costs and exclude transfers. Values are in damages units and shown to four decimals.

Gross outcome error is E[|R-T|], averaged over all potential disputes. R is the base payment before legal costs and separately awarded fee transfers; T is true liability and damages equal one. Since payments lie in [0,1], error equals pi(1-E[R|T=1])+(1-pi)E[R|T=0]. Conditional means are intermediate calculations, not conditional headline outcomes. The configured truth prior is also used for the three net-burden contributions. Source reports are rounded. Fee rules still affect error through equilibrium behavior. The five measures are distinct, not additive welfare components.

Settlements use their truth-specific probabilities and means; an undefined zero-probability mean remains null in the audit.
Mutual give-up is allocated once, half to abandonment and half to default. Disposition bars preserve saved probabilities
without renormalization. Trial wins/losses concern court findings, not true liability.
The checks reconcile saved summary/detail records, truth-weighted transfers, monetary components, stage costs, and disposition totals.

## Regeneration

After equilibrium determination and report generation, run the normal LitigCharts diagram command with the article configuration:

```text
dotnet run --project LitigCharts -c Release -- diagrams results --config <article>/article-diagrams.json
```

The same exhibits are included in `diagrams all`, `diagrams publication`, and `diagrams dispositions`.
Use `diagrams welfare-outcomes` to regenerate just these tables and charts. `--list` writes nothing;
`--sources-only` writes TeX/data; `--compile-only` recompiles the inventoried TeX without reading reports.
`--output-root` and `--jobs` work as for other diagrams. No command determines equilibria or changes reports.
The request's Inputs list points to numerical summaries and matching individual reports. Every saved specification
and cost in those sources is discovered automatically, including future results added to those batches.
A new report batch needs one Inputs entry; it does not need separate figure or table selections.
Changing any primitive beyond preferences/fee rule within a group is rejected rather than silently pooled.

## Available comparisons

| Family | Cost | Cases | Available fee rules |
|---|---:|---:|---|
| all-costs-avoidable | 0.25 | 2 | American, Trial Fee-Shifting |
| all-costs-avoidable | 0.5 | 2 | American, Trial Fee-Shifting |
| all-costs-avoidable | 1 | 2 | American, Trial Fee-Shifting |
| all-costs-avoidable | 2 | 2 | American, Trial Fee-Shifting |
| all-costs-avoidable | 4 | 2 | American, Trial Fee-Shifting |
| all-costs-sunk | 0.25 | 2 | American, Trial Fee-Shifting |
| all-costs-sunk | 0.5 | 2 | American, Trial Fee-Shifting |
| all-costs-sunk | 1 | 2 | American, Trial Fee-Shifting |
| all-costs-sunk | 2 | 2 | American, Trial Fee-Shifting |
| all-costs-sunk | 4 | 2 | American, Trial Fee-Shifting |
| baseline | 0.25 | 6 | American, Trial Fee-Shifting, Complete Fee-Shifting |
| baseline | 0.5 | 6 | American, Trial Fee-Shifting, Complete Fee-Shifting |
| baseline | 1 | 6 | American, Trial Fee-Shifting, Complete Fee-Shifting |
| baseline | 2 | 6 | American, Trial Fee-Shifting, Complete Fee-Shifting |
| baseline | 4 | 6 | American, Trial Fee-Shifting, Complete Fee-Shifting |
| baseline-offers-15 | 1 | 4 | American, Trial Fee-Shifting |
| center-weighted-continuous-merits | 0.25 | 2 | American, Trial Fee-Shifting |
| center-weighted-continuous-merits | 0.5 | 2 | American, Trial Fee-Shifting |
| center-weighted-continuous-merits | 1 | 2 | American, Trial Fee-Shifting |
| center-weighted-continuous-merits | 2 | 2 | American, Trial Fee-Shifting |
| center-weighted-continuous-merits | 4 | 2 | American, Trial Fee-Shifting |
| direct-binary-state-signals | 0.25 | 2 | American, Trial Fee-Shifting |
| direct-binary-state-signals | 0.5 | 2 | American, Trial Fee-Shifting |
| direct-binary-state-signals | 1 | 2 | American, Trial Fee-Shifting |
| direct-binary-state-signals | 2 | 2 | American, Trial Fee-Shifting |
| direct-binary-state-signals | 4 | 2 | American, Trial Fee-Shifting |
| high-noise | 0.25 | 2 | American, Trial Fee-Shifting |
| high-noise | 0.5 | 2 | American, Trial Fee-Shifting |
| high-noise | 1 | 2 | American, Trial Fee-Shifting |
| high-noise | 2 | 2 | American, Trial Fee-Shifting |
| high-noise | 4 | 2 | American, Trial Fee-Shifting |
| low-noise | 0.25 | 4 | American, Trial Fee-Shifting |
| low-noise | 0.5 | 4 | American, Trial Fee-Shifting |
| low-noise | 1 | 4 | American, Trial Fee-Shifting |
| low-noise | 2 | 4 | American, Trial Fee-Shifting |
| low-noise | 4 | 4 | American, Trial Fee-Shifting |
| mandatory-filing-and-answering | 0.25 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-and-answering | 0.5 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-and-answering | 1 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-and-answering | 2 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-and-answering | 4 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-answering-no-exit | 0.25 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-answering-no-exit | 0.5 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-answering-no-exit | 1 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-answering-no-exit | 2 | 2 | American, Trial Fee-Shifting |
| mandatory-filing-answering-no-exit | 4 | 2 | American, Trial Fee-Shifting |
| polarized-continuous-merits | 0.25 | 2 | American, Trial Fee-Shifting |
| polarized-continuous-merits | 0.5 | 2 | American, Trial Fee-Shifting |
| polarized-continuous-merits | 1 | 2 | American, Trial Fee-Shifting |
| polarized-continuous-merits | 2 | 2 | American, Trial Fee-Shifting |
| polarized-continuous-merits | 4 | 2 | American, Trial Fee-Shifting |
| truth-conditioned-latent-merits | 0.25 | 2 | American, Trial Fee-Shifting |
| truth-conditioned-latent-merits | 0.5 | 2 | American, Trial Fee-Shifting |
| truth-conditioned-latent-merits | 1 | 2 | American, Trial Fee-Shifting |
| truth-conditioned-latent-merits | 2 | 2 | American, Trial Fee-Shifting |
| truth-conditioned-latent-merits | 4 | 2 | American, Trial Fee-Shifting |
