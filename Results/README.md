# Current production results

`CS004` holds the non-multiple-equilibrium output from the clean production run. The multiple-equilibrium output is in [Supplemental materials/CS004ME](../Supplemental%20materials/CS004ME/).

The main plan has 134 option sets: 13 specifications times five cost levels times two fee rules, plus four fifteen-offer sensitivity cases at cost multiplier 1. The fifteen-offer cases cover the baseline and moderate symmetric risk aversion under American and British rules, with signals held fixed.

## Files to start with

- `CS004/CS004 numerical results.csv`: aggregate report, including specification metadata, filters, participation, offers, dispositions, expenditures, and net-outcome measures.
- `CS004/CS004 Combined costbreakdown.csv`: combined cost-breakdown data.
- `CS004/CS004 run manifest.json`: plan definition, source and binary provenance, validation status, and reused fifteen-offer equilibrium hashes.
- `CS004/*-InformationSetActions.csv`: information-set reach, off-path status, equilibrium action probabilities, conditional utilities, and losses relative to the best action.
- `CS004/*-equ.csv`, individual numerical CSVs, `.efg` files, task logs, and `Process Logs`: underlying strategies, reports, games, and solver diagnostics.

## Diagram organization

The CS004 root contains six diagram families for each of its 134 cases: filing/answering, offers, light/dark cost breakdown, and light/dark stage costs. It therefore contains 804 individual PDFs and matching TeX files.

`CS004/Aggregated Data` contains 338 aggregate PDFs and matching TeX sources. `Single Row` compares cases at the principal cost multiplier, 1. `All Rows` shows the five cost levels. There are 14 single-row variations and 12 all-rows variations; the two fifteen-offer comparisons have no full cost sweep.

The literal `Risk Neutral` grouping directory does not mean that every comparison panel is risk neutral. Read the panel labels and specification metadata, especially in the moderate-risk-aversion comparisons.

The standard `Accuracy and Expenditures` charts contain two ex ante monetary measures and expenditures. The numerical report additionally contains the three conditional perspectives and Net Outcome Fidelity Loss; their publication display must still be prepared. Stage-cost labels also require review.

## Import provenance

See [Provenance](Provenance/) for the original suite manifest and diagram inventory, plus `article import manifest.json`. The latter records every source path, article-repository path, byte count, and SHA-256 hash, and all excluded files with reasons.

The model repository's source run was preserved. LaTeX `.aux`/`.log` files and completed coordinator state were not imported; solver and worker `.txt` logs were retained. The three generic one-time signal illustrations were excluded because they do not describe the revised principal model.
