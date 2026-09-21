# Pairwise fee-rule comparisons: selected costs

Each cell reports **decreases / ties / increases** in the outcome when moving from the first fee rule to the second. The comparison is second minus first. A decrease in a named party's shortfall or burden benefits that party; it does not by itself establish an overall welfare ranking.

Included cost multipliers: **0.5, 1, 2**. Included source cases: **168**.
Excluded cost multipliers: **0.25, 4**.

## Risk neutral

Every cell totals **28 matched settings**.

| Outcome | American -> Trial | American -> Complete | Trial -> Complete |
|---|---:|---:|---:|
| Meritorious-plaintiff shortfall | 25 / 0 / 3 | 14 / 0 / 14 | 2 / 5 / 21 |
| Nonliable-defendant burden | 28 / 0 / 0 | 26 / 0 / 2 | 15 / 5 / 8 |
| Liable-defendant excess burden | 2 / 0 / 26 | 1 / 0 / 27 | 0 / 5 / 23 |
| Total expenditures | 26 / 2 / 0 | 15 / 2 / 11 | 3 / 5 / 20 |
| Gross outcome error | 17 / 2 / 9 | 7 / 2 / 19 | 1 / 5 / 22 |
| Filing share | 9 / 16 / 3 | 21 / 7 / 0 | 19 / 8 / 1 |
| Answering share | 14 / 8 / 6 | 2 / 6 / 20 | 0 / 5 / 23 |

## Risk averse

Every cell totals **28 matched settings**.

| Outcome | American -> Trial | American -> Complete | Trial -> Complete |
|---|---:|---:|---:|
| Meritorious-plaintiff shortfall | 20 / 1 / 7 | 12 / 0 / 16 | 1 / 4 / 23 |
| Nonliable-defendant burden | 20 / 1 / 7 | 20 / 0 / 8 | 9 / 4 / 15 |
| Liable-defendant excess burden | 11 / 3 / 14 | 6 / 3 / 19 | 5 / 6 / 17 |
| Total expenditures | 21 / 2 / 5 | 17 / 3 / 8 | 4 / 6 / 18 |
| Gross outcome error | 15 / 3 / 10 | 9 / 3 / 16 | 0 / 6 / 22 |
| Filing share | 14 / 10 / 4 | 13 / 13 / 2 | 6 / 13 / 9 |
| Answering share | 14 / 7 / 7 | 5 / 11 / 12 | 1 / 7 / 20 |

## Scope and accounting

Comparisons hold model family, cost and preferences fixed. A family available at fewer costs contributes only its available matched settings; the fifteen-offer case is retained whenever cost 1 is included. Denominators are calculated from the selected source rows.

Differences with absolute value at most **0.00001** count as ties. The tolerance is in damages per potential dispute for monetary outcomes and in probability units for filing and answering. With the default tolerance, the probability threshold is 0.001 percentage points. Values are compared before display rounding.

The three burden columns use population-weighted contributions, not the conditional diagnostic columns. The truth prior is held fixed within each comparison, so rescaling to the corresponding truth-conditional averages preserves the sign of each difference. The tie tolerance here is applied to the population-weighted values. Expenditures use real litigation costs; gross outcome error is before legal costs and separate fee transfers. These five measures are distinct and are not summed.

Filing and answering are shares of all potential disputes. Answering counts disputes that are filed and answered, including those ending in later default. It is not conditional on filing and is not one minus the nonanswer share. This script compares aggregate shares; it does not inspect individual answering strategies or infer a causal mechanism.

The counts describe selected equilibria on the retained parameter grid, not empirical frequencies or all possible equilibria. The separate multiple-start study remains a distinct sensitivity exercise and is not pooled into these counts.

Source: `Results/Aggregated Data/Sources/welfare-outcomes.csv`. Companion counts and comparison CSVs retain the denominators, individual values, differences, and option-set identifiers. The provenance JSON records source and generator hashes and the cost selection.
