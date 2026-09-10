# Revised publication figures

This is the sole directory for the revised manuscript's publication figures. The old PDFs and duplicate PNGs were removed after checkpoint commit `7e92fc01e1d7ff92bf0b07dbe80ac9ff021ce7b3`. The empty `Updated figures` folder is retired.

The new publication figures have not yet been prepared. Current generated research diagrams and their TeX sources are available in [Results/CS004](../Results/CS004/) and [Supplemental materials/CS004ME](../Supplemental%20materials/CS004ME/). Do not treat the old manuscript's now-missing figure references as current illustrations.

## Planned figures and their sources

| Proposed publication file | Content | Source and remaining work |
|---|---|---|
| `fig01-model-and-timing.pdf` | Timeline, truth/continuous merits/signals, and a short worked path | Draw from the current model definition. The generic hidden-state/liability/damages PDFs do not describe the new baseline and were excluded from this import. |
| `fig02-participation.pdf` | Baseline filing and answering by signal under both fee rules | Use baseline cost-1 American/British `-fileans` diagrams and action CSVs. Prepare directly labeled points/lines or bars with clear conditioning. |
| `fig03-offers.pdf` | Baseline offer support by signal under both fee rules | Use the same cases' `-offers` diagrams and action CSVs. Preserve mixing and off-path distinctions; choose an illustrative action-payoff comparison. |
| `fig04-dispositions.pdf` | Baseline, moderate risk aversion, mandatory entry, and mandatory entry with no later exit | Use CS004 numerical rows at cost 1. Assemble American/British comparisons with readable disposition categories and explicit mutual-give-up allocation. |

Baseline source stems, relative to `Results/CS004`:

- `CS004 Specification-Baseline__Cost-1__Fee-American`
- `CS004 Specification-Baseline__Cost-1__Fee-British`

Append ` -fileans.pdf`, ` -offers.pdf`, or ` -InformationSetActions.csv`. Matching diagram sources end in `.tex`. Preserve exact CSV probabilities when preparing new plots; the PDF labels are rounded.

Current aggregate disposition comparisons are under `Aggregated Data/<specification>/Risk Neutral/Single Row`. This grouping directory name does not override each panel's risk-aversion specification.

The three-perspective monetary-outcome presentation belongs in the planned main table and, if useful, a supplemental plot. The existing aggregate `Accuracy and Expenditures` charts show only two ex ante monetary measures plus expenditures; the additional required columns are already in `CS004 numerical results.csv`.

Keep each final figure's source script/TeX and source-row mapping alongside the PDF. Replacing manuscript figure references remains part of the article revision.
