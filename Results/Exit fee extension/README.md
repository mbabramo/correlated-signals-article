# Fee liability on unilateral exit

These ten CS006EF cases extend the archived CS004 results. Filing, answering,
and later exit remain voluntary. Each case shifts incurred costs at trial,
on later abandonment/default, and on initial nonanswer. Settlement retains
the existing inclusive transfer and each party's own expenses; unincurred
trial expenses are never charged on exit. The five existing cost levels are
crossed with risk neutrality and symmetric CARA alpha 2.

`CS006EF numerical results.csv` contains one unconditional row per new case.
The full and signal-filtered reports remain available for diagnostics. The
specification-comparisons file compares risk preferences within the extension;
the comparisons with original trial-only fees are in the supplemental charts.

The source run was completed and aggregated from clean code commit `5b76d5fd`.
See Run documentation for the original manifest and verified import hashes.
Original CS004 and CS004ME equilibria were neither copied nor rerun. Original
control rows retain their original provenance; this is not a new 144-case solve.

Charts, matched comparisons, requests, and strategy diagnostics are in
`Supplemental materials/Fee shifting on exit`. The routine suite now includes
this extension; `--plan exit-fees` runs it independently. See ACESim4's
`scripts/Exit-fee-extension.md` for commands and the endpoint rules.
