# risk-neutral-trial-cost-0.5: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-0.5__Fee-British`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.005972 | 0.025803 | 1 | 2.49987E-11 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **-1.7763568E-15**, D **2.499867E-11** (reported utility units). Acceptance limit: 1E-10. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 8.045000 | 28.308267 | 19.524268 | 44.122465 | 0.000000 |
| forward | 8.045000 | 28.308267 | 19.524268 | 44.122465 | 0.000000 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.35 | continue | 0.85: 100% | 0.75: 1.113%; 0.85: 33.336%; 0.95: 65.551% | 1.000 -> 2.000 |
| P | P Offer | 0.45 | continue | 0.85: 16.794%; 0.95: 83.206% | 0.85: 24.45%; 0.95: 75.55% | 1.572 -> 1.744 |
| P | P Offer | 0.55 | continue | 0.95: 100% | 0.85: 13.431%; 0.95: 86.569% | 1.000 -> 1.484 |
| P | P Offer | 0.65 | continue | 0.95: 100% | 0.85: 3.034%; 0.95: 96.966% | 1.000 -> 1.146 |
| P | P Offer | 0.95 | continue | 0.95: 100% | 0.85: 4.596%; 0.95: 95.404% | 1.000 -> 1.205 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
