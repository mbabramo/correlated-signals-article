# Generated pairwise fee-rule comparisons

These comparisons summarize the saved routine parameter study, separately for
risk neutrality and risk aversion, across all three pairs of fee-shifting rules.
Each cell reports **decreases / ties / increases** in the named outcome when
moving from the first rule to the second; the absolute tie tolerance is 0.00001.
Filing share and answering share both use all potential disputes as their
denominator. Answering share counts disputes that are filed and answered.

- [All costs](all-costs.md): 46 matched settings per risk preference.
- [Excluding costs 0.25 and 4](filtered-costs.md): 28 matched settings per risk
  preference, including the fifteen-offer case at cost 1.
- [Selected-cost case details](filtered-costs-case-details.md): identifies the
  model families and costs behind the less frequent direction, with ties
  separately listed. The full-grid version is in all-costs-case-details.md.

Companion CSVs preserve source values, differences, classifications and counts.
The provenance JSON files identify input data, code, cost selection and hashes.
The [answering-strategy audit](Sources/answering-strategy-audit.json) checks all
920 answering information sets in the 92 routine Complete Fee-Shifting cases,
including off-path information sets. It is separate from the aggregate
answering-share comparisons and the multiple-start equilibrium study.

Run these commands from ACESim4:

```powershell
python -B scripts/build_fee_rule_comparisons.py --article-directory "C:/Users/Admin/source/repos/correlated-signals-article"
python -B scripts/verify_complete_answering.py --article-directory "C:/Users/Admin/source/repos/correlated-signals-article"
```

Both read the article's saved results. See ACESim4's
`scripts/Fee-rule-comparisons.md` for definitions, options and validation.
The comprehensive figures and welfare tables are in
[Results/Aggregated Data](<../../Results/Aggregated Data/README.md>).
The all-cost publication table is [Table 5](<../../Tables/Table 5 - Overall results summary.pdf>).
