# Multiple equilibria

The cost-1 floating-point search completed 200 starts across American/British and risk-neutral/risk-averse cases. 199 passed the approved acceptance criteria; British risk-averse start 12 did not. These are accepted profiles, not 199 distinct exact equilibria.

[Welfare outcomes figure](Multiple%20equilibrium%20welfare%20outcomes.pdf) plots all five welfare measures for every accepted profile. [Disposition ranges](Sources/disposition-ranges.json) remain available numerically. Each row is a start index, not a matched equilibrium pair or ranking; repeated outcomes are retained. Grouping by complete strategies, reached strategies and outcomes is retained separately in Sources/catalog.json. Tolerance-based groups are descriptive, not proof of mathematical identity, nor estimates of equilibrium likelihood.

All full profiles, audit results, failed-attempt accounting, full-precision outcomes and grouping thresholds are retained. Exact primary profiles and approximate acceptance bands remain distinct.

[Automated tremble-sensitivity report](../../Results/Aggregated%20Data/Equilibrium%20sensitivity/Report.md) gives per-profile tests, group summaries and welfare-reversal comparisons for the 199 accepted profiles and four exact primary benchmarks. It measures unilateral incentives to adjust under small opponent mistakes, not equilibrium likelihood. The single Results regeneration command rebuilds this report and runs its independent checks.
