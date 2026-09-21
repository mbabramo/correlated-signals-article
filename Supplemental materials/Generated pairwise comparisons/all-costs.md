# Pairwise fee-rule comparisons: all costs

Each cell reports **decreases / ties / increases** in the outcome when moving from the first fee rule to the second. The comparison is second minus first. A decrease in a named party's shortfall or burden benefits that party; it does not by itself establish an overall welfare ranking.

Included cost multipliers: **0.25, 0.5, 1, 2, 4**. Included source cases: **276**.

## Risk neutral

Every cell totals **46 matched settings**.

| Outcome | American -> Trial | American -> Complete | Trial -> Complete |
|---|---:|---:|---:|
| Meritorious-plaintiff shortfall | 35 / 2 / 9 | 23 / 1 / 22 | 2 / 15 / 29 |
| Nonliable-defendant burden | 44 / 2 / 0 | 42 / 1 / 3 | 19 / 15 / 12 |
| Liable-defendant excess burden | 2 / 2 / 42 | 1 / 1 / 44 | 0 / 15 / 31 |
| Total expenditures | 40 / 6 / 0 | 25 / 5 / 16 | 4 / 15 / 27 |
| Gross outcome error | 26 / 6 / 14 | 16 / 5 / 25 | 2 / 15 / 29 |
| Filing share | 15 / 27 / 4 | 29 / 17 / 0 | 27 / 18 / 1 |
| Answering share | 20 / 19 / 7 | 3 / 16 / 27 | 0 / 15 / 31 |

## Risk averse

Every cell totals **46 matched settings**.

| Outcome | American -> Trial | American -> Complete | Trial -> Complete |
|---|---:|---:|---:|
| Meritorious-plaintiff shortfall | 35 / 2 / 9 | 20 / 3 / 23 | 2 / 8 / 36 |
| Nonliable-defendant burden | 28 / 2 / 16 | 33 / 3 / 10 | 18 / 8 / 20 |
| Liable-defendant excess burden | 16 / 7 / 23 | 10 / 6 / 30 | 12 / 13 / 21 |
| Total expenditures | 26 / 5 / 15 | 26 / 7 / 13 | 15 / 12 / 19 |
| Gross outcome error | 26 / 7 / 13 | 17 / 6 / 23 | 2 / 12 / 32 |
| Filing share | 14 / 22 / 10 | 18 / 25 / 3 | 13 / 24 / 9 |
| Answering share | 15 / 20 / 11 | 7 / 23 / 16 | 3 / 19 / 24 |

## Scope and accounting

Comparisons hold model family, cost and preferences fixed. A family available at fewer costs contributes only its available matched settings; the fifteen-offer case is retained whenever cost 1 is included. Denominators are calculated from the selected source rows.

Differences with absolute value at most **0.00001** count as ties. The tolerance is in damages per potential dispute for monetary outcomes and in probability units for filing and answering. With the default tolerance, the probability threshold is 0.001 percentage points. Values are compared before display rounding.

The three burden columns use population-weighted contributions, not the conditional diagnostic columns. The truth prior is held fixed within each comparison, so rescaling to the corresponding truth-conditional averages preserves the sign of each difference. The tie tolerance here is applied to the population-weighted values. Expenditures use real litigation costs; gross outcome error is before legal costs and separate fee transfers. These five measures are distinct and are not summed.

Filing and answering are shares of all potential disputes. Answering counts disputes that are filed and answered, including those ending in later default. It is not conditional on filing and is not one minus the nonanswer share. This script compares aggregate shares; it does not inspect individual answering strategies or infer a causal mechanism.

The counts describe selected equilibria on the retained parameter grid, not empirical frequencies or all possible equilibria. The separate multiple-start study remains a distinct sensitivity exercise and is not pooled into these counts.

Source: `Results/Aggregated Data/Sources/welfare-outcomes.csv`. Companion counts and comparison CSVs retain the denominators, individual values, differences, and option-set identifiers. The provenance JSON records source and generator hashes and the cost selection.
