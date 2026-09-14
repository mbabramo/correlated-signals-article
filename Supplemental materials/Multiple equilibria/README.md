# Multiple-equilibrium robustness

This directory replaces the previous `Robustness checks` material with the completed clean production output at numerical commit `31d0f17836435a2b1a7cc3fc52a6dfcec0db3565`. The preserved filename prefix `CS004ME` is the solver's identifier for this multiple-equilibrium run.

Both cases use the principal baseline, cost multiplier 1, ten offers, ten party signals, and two court signals. One case uses the American fee rule and the other Trial Fee-Shifting (trial only). Complete Fee-Shifting was not tested in this separate study.

| Fee rule | Requested priors | Attempted solves | Inexact attempts | Exact attempts | Verified recoveries | Distinct retained profiles |
|---|---:|---:|---:|---:|---:|---:|
| American | 50 | 99 | 49 | 50 | 50 | 21 |
| Trial Fee-Shifting | 50 | 99 | 49 | 50 | 50 | 11 |

## Reading order

1. `CS004ME equilibrium ranges.csv`: outcome minima, means, maxima, ranges, standard deviations, and coefficients of variation by fee regime.
2. `CS004ME equilibrium outcomes.csv`: one row for each retained profile, with recoveries, verification, exploitability, participation, bargaining, disposition, expenditure, and monetary-outcome measures.
3. `*-EquilibriumRecoveries.csv`: recovery counts, verification status, and exact normalized-vector distinctness information.
4. `*-Eq*-InformationSetActions.csv`: every action's equilibrium probability, reach/off-path status, conditional utility, and loss relative to the best action, for each retained equilibrium.
5. `CS004ME run manifest.json`, `.efg`, equilibrium files, task logs, and `Process Logs`: reproduction and solver details.

There are 32 retained profiles and 32 action-value reports. The 216 PDF/TeX pairs comprise six diagram families for those profiles and the additional Avg/Corr diagnostics. The main production output is in `../../Results`.

The retained profiles have identical headline lifecycle and monetary outcomes at reported precision, with meaningful variation principally in plaintiff mean demands. Tiny nonzero standard deviations at floating-point precision should not be described as substantive dispersion. Recovery shares are computational diagnostics, not behavioral equilibrium-selection probabilities; the exercise does not enumerate all equilibria or establish uniqueness.

Use the current range/outcome tables to prepare the appendix exhibits. The older small-tree coefficient-of-variation and cross-tree correlation figures were removed rather than reused for this different design.

The local `CS004ME run manifest.json` preserves the original production/build provenance. This completed separate workflow was retained during the September 14 routine-study rebuild. To run a new multiple-start study intentionally, use `--plan multiple-equilibria`; it is not part of the default retained suite.
