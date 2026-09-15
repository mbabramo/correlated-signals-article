# risk-neutral-american-cost-1: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-1__Fee-American`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward | 0.014632 | 0.115654 | 1 | 2.49999E-10 | Coordinate search converged within improvement tolerance |
| reverse (selected) | 0.014632 | 0.115654 | 1 | 2.49999E-10 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **3.5527137E-15**, D **2.4999913E-10** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 19.105276 | 37.317924 | 8.344081 | 35.232720 | 0.000000 |
| forward | 19.105276 | 37.317924 | 8.344081 | 35.232720 | 0.000000 |
| reverse | 19.105276 | 37.317924 | 8.344081 | 35.232720 | 0.000000 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.35 | continue | 0.75: 100% | 0.45: 5.914%; 0.55: 12.741%; 0.65: 19.568%; 0.75: 26.395%; 0.85: 27.59%; 0.95: 7.791% | 1.000 -> 5.231 |
| P | P Offer | 0.45 | continue | 0.75: 100% | 0.55: 7.384%; 0.65: 16.758%; 0.75: 26.133%; 0.85: 32.382%; 0.95: 17.343% | 1.000 -> 4.533 |
| P | P Offer | 0.55 | continue | 0.85: 100% | 0.65: 10.77%; 0.75: 22.411%; 0.85: 35.596%; 0.95: 31.224% | 1.000 -> 3.692 |
| P | P Offer | 0.65 | continue | 0.85: 100% | 0.65: 2.752%; 0.75: 15.796%; 0.85: 36.008%; 0.95: 45.444% | 1.000 -> 3.054 |
| P | P Offer | 0.75 | continue | 0.95: 100% | 0.75: 9.549%; 0.85: 34.446%; 0.95: 56.005% | 1.000 -> 2.499 |
| P | P Offer | 0.85 | continue | 0.95: 100% | 0.75: 7.176%; 0.85: 32.582%; 0.95: 60.242% | 1.000 -> 2.363 |
| P | P Offer | 0.95 | continue | 0.95: 100% | 0.65: 0.769%; 0.75: 9.876%; 0.85: 31.492%; 0.95: 57.863% | 1.000 -> 2.577 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
