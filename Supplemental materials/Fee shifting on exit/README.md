# Fee liability on unilateral exit: completed comparisons

All ten CS006EF cases are complete and validated. The new trigger reimburses
incurred expenses on initial nonanswer and later unilateral abandonment/default,
as well as trial. Filing, answering, and later exit remain voluntary. Settlement
retains the inclusive transfer and each party's own expenses. No future trial
expenses are charged on exit. Both parties are either risk neutral or CARA alpha 2;
the five cost multipliers are 0.25, 0.5, 1, 2, and 4.

## Comparison exhibits

- [Ordinary-cost dispositions](ordinary-cost-dispositions.pdf): risk neutrality
  and risk aversion, each comparing trial-only fees with the broader trigger.
- [Risk-neutral dispositions](risk-neutral-dispositions.pdf) and
  [risk-averse dispositions](moderate-risk-aversion-dispositions.pdf): all five costs.
- [Risk-neutral strategies](risk-neutral-selection-offers.pdf) and
  [risk-averse strategies](moderate-risk-aversion-selection-offers.pdf): filing,
  answering, and offers at ordinary costs. Continue and abandon/default histories
  are separate panels. Equal-size markers show mixed offer support; exact mixing
  probabilities remain in the JSON and strategy tables. Blank histories are off path.
- [Risk-neutral monetary outcomes](risk-neutral-monetary-outcomes.pdf) and
  [risk-averse monetary outcomes](moderate-risk-aversion-monetary-outcomes.pdf):
  expenditures, three population-weighted truth-relative components, fidelity loss,
  and net transfer. American controls are also shown.
- [Strategy diagnostics](<Equilibrium strategy changes/README.md>): four matched
  trigger contrasts at costs 1 and 4, with full calculations, residuals, and sensitivity
  flags; six PDFs include individual tables and ordinary/high-cost bundles.

There are seven comparison diagrams and sixty individual case diagrams, plus
six strategy PDFs. The latter are four comparisons in two additional bundles,
not six independent interventions. The individual diagrams are in
`../../Results/Exit fee extension/Individual simulations`.

## Denominators and interpretation

`matched-comparisons.csv` contains thirty All/Only Eq rows: ten new cases and
twenty archived controls. Headline dispositions and monetary values are per
potential dispute. `D Answers` is joint filing and answering. The three monetary
contributions are weighted by the truth-state probabilities. Fidelity loss is not
social welfare; fee reimbursement is a transfer, not real expenditure. Lines join
the five computed costs and do not establish results between them.

The broader trigger greatly increases ordinary-cost settlement, especially under
risk aversion, and reverses the old settlement-versus-withdrawal characterization
of the preference comparison under fees. Its expenditure effects vary with costs.
At cost 4 the selected risk-averse extension equilibrium has no filing; conditional
post-filing statistics are undefined. Initial nonanswer liability and later-exit
liability change jointly. Separating them, widening fee-inclusive offer support,
and applying the original focused tables' additional mixed-equilibrium intersection
checks to the extension remain further work, not completed robustness evidence.

## Reproduction and provenance

Numerical source: clean ACESim4 commit `5b76d5fd`. The ten solves and aggregation
are separate from historical CS004/CS004ME production. No original equilibria were
copied or rerun. Results and verified import hashes are in
`../../Results/Exit fee extension/Run documentation`.

Final chart source: `fad9f102`. Generate this collection with
`dotnet LitigCharts/bin/Release/net9.0/LitigCharts.dll exit-fees --request <exit-fees.request.json>`
from ACESim4, supplying this request's absolute path. `chart-inventory.json`
records the input/output hashes. The article's dispositions/publication/all targets
also regenerate the three disposition comparisons through `article-diagrams.json`.
The extension has its own individual-chart directory; the historical individual
diagram count remains 804.

The strategy request has its own `equilibrium-changes` command and manifest.
It retains tie, unvisited-opponent completion, intermediate-reach, and endpoint-selection
qualifications. Unlike the original focused article tables, it does not apply the
further intersection across equilibrium-preserving mixed representatives.
