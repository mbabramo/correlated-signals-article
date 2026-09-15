# risk-averse-trial-cost-2: equilibrium-preserving mixing

Source specification: `Specification-ModerateRiskAversion__Cost-2__Fee-British`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.085106 | 0.123272 | 2 | 2.49884E-10 | Coordinate search converged within improvement tolerance |
| reverse | 0.085106 | 0.122797 | 7 | 2.55113E-10 | Sweep limit reached |

Selected profile's unrestricted best-response gains: P **2.4988367E-10**, D **2.1134383E-10** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 28.431000 | 41.200891 | 19.091316 | 0.354500 | 10.922292 |
| forward | 28.431000 | 41.200891 | 19.091317 | 0.354500 | 10.922292 |
| reverse | 28.431000 | 41.200891 | 19.091317 | 0.354500 | 10.922292 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.75 | continue | 0.55: 32.457%; 0.65: 45.005%; 0.75: 22.538% | 0.55: 11.499%; 0.65: 16.787%; 0.75: 23.905%; 0.85: 23.905%; 0.95: 23.905% | 2.887 -> 4.829 |
| P | P Offer | 0.85 | continue | 0.75: 48.967%; 0.85: 51.033% | 0.55: 11.832%; 0.65: 16.913%; 0.75: 23.752%; 0.85: 23.752%; 0.95: 23.752% | 2.000 -> 4.842 |
| P | P Offer | 0.95 | continue | 0.85: 100% | 0.55: 14.299%; 0.65: 17.845%; 0.75: 22.619%; 0.85: 22.619%; 0.95: 22.619% | 1.000 -> 4.925 |
| D | D Offer | 0.05 | continue | 0.05: 27.891%; 0.15: 72.109% | 0.05: 33.333%; 0.15: 33.333%; 0.25: 33.333% | 1.807 -> 3.000 |
| D | D Offer | 0.15 | continue | 0.15: 20.748%; 0.25: 48.117%; 0.35: 31.135% | 0.05: 25%; 0.15: 25%; 0.25: 25%; 0.35: 25% | 2.834 -> 4.000 |
| D | D Offer | 0.55 | exit | 0.45: 100% | 0.45: 100%; 0.55: 0% | 1.000 -> 1.000 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
