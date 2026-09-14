# Current production results

This folder holds the main clean production output. The multiple-equilibrium output is in [Supplemental materials/Multiple equilibria](../Supplemental%20materials/Multiple%20equilibria/). There is no additional coded-name folder around the main results.

The main plan has 134 option sets: 13 specifications times five cost levels times two fee rules, plus four fifteen-offer sensitivity cases at cost multiplier 1. The fifteen-offer cases cover the baseline and moderate symmetric risk aversion under American and British rules, with signals held fixed.

## Files to start with

- `CS004 numerical results.csv`: aggregate report, including specification metadata, filters, participation, offers, dispositions, expenditures, and net-outcome measures.
- `CS004 Combined costbreakdown.csv`: combined cost-breakdown data.
- `Run documentation/CS004 run manifest.json`: plan definition, source and binary versions, validation status, and reused fifteen-offer equilibrium hashes.
- `Individual simulations/*-InformationSetActions.csv`: information-set reach, off-path status, equilibrium action probabilities, conditional utilities, and losses relative to the best action.
- `Individual simulations/*-equ.csv`, individual numerical CSVs, `.efg` files, and task logs: underlying strategies, reports, games, and solver diagnostics.
- `Process Logs`: worker logs from the coordinated production run.

The preserved filename prefix `CS004` is the production run identifier, not a separate model or required folder name.

## Reporting and the fee-trigger extension

Use `Filter = All` for headline disposition probabilities and expected monetary
outcomes per potential dispute. `D Answers` is the joint probability of filing
and answering. The three truth-conditional monetary perspectives must be weighted
by their truth-state probabilities before displaying their contributions alongside
the unconditional Net Outcome Fidelity Loss. Conditional summaries remain useful
for mechanism checks and comparisons with an explicitly selected empirical sample.

The separate [Exit fee extension](<Exit fee extension/>) contains the ten CS006EF
cases with reimbursement of incurred fees on trial and unilateral exit, including
initial nonanswer. The original `CS004` results retain their trial-contingent fee
trigger and original provenance. Matched comparative figures and data are in
[Fee shifting on exit](<../Supplemental materials/Fee shifting on exit/>).

## Diagram organization

`Individual simulations` contains six diagram families for each of the 134 cases: filing/answering, offers, light/dark cost breakdown, and light/dark stage costs. It therefore contains 804 individual PDFs and matching TeX files.

`Aggregated Data` contains 338 aggregate PDFs and matching TeX sources. `Single Row` compares cases at the principal cost multiplier, 1. `All Rows` shows the five cost levels. There are 14 single-row variations and 12 all-rows variations; the two fifteen-offer comparisons have no full cost sweep.

The literal `Risk Neutral` grouping directory does not mean that every comparison panel is risk neutral. Read the panel labels and specification metadata, especially in the moderate-risk-aversion comparisons.

The standard `Accuracy and Expenditures` charts contain two ex ante monetary measures and expenditures. The numerical report additionally contains the three conditional perspectives and Net Outcome Fidelity Loss; their publication display must still be prepared. Stage-cost labels also require review.

## Run documentation

See [Run documentation](Run%20documentation/) for the original suite manifest and diagram inventory, plus `article import manifest.json`. These records say which code produced the results, which plans completed, and whether any file has changed. The import manifest records every source path, current article-repository path, byte count, and SHA-256 hash, and all excluded files with reasons.

The model repository's source run was preserved. LaTeX `.aux`/`.log` files and completed coordinator state were not imported; solver and worker `.txt` logs were retained. The three generic one-time signal illustrations were excluded because they do not describe the revised principal model.
