# risk-neutral-british-cost-1: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-1__Fee-British`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward | 0.000000 | 0.086896 | 1 | 2.49996E-10 | Coordinate search converged within improvement tolerance |
| reverse (selected) | 0.000000 | 0.086896 | 1 | 2.49996E-10 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **0**, D **2.4999558E-10** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 17.813000 | 38.305533 | 18.260998 | 25.620469 | 0.000000 |
| forward | 17.813000 | 38.305533 | 18.260998 | 25.620469 | 0.000000 |
| reverse | 17.813000 | 38.305533 | 18.260998 | 25.620469 | 0.000000 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.45 | continue | 0.75: 100% | 0.55: 1.281%; 0.65: 9.08%; 0.75: 16.879%; 0.85: 24.681%; 0.95: 48.079% | 1.000 -> 3.566 |
| P | P Offer | 0.55 | continue | 0.85: 100% | 0.65: 5.63%; 0.75: 15.314%; 0.85: 25.001%; 0.95: 54.055% | 1.000 -> 3.091 |
| P | P Offer | 0.65 | continue | 0.95: 100% | 0.65: 3.295%; 0.75: 14.147%; 0.85: 25.002%; 0.95: 57.557% | 1.000 -> 2.868 |
| P | P Offer | 0.75 | continue | 0.95: 100% | 0.65: 3.181%; 0.75: 14.09%; 0.85: 25.002%; 0.95: 57.727% | 1.000 -> 2.856 |
| P | P Offer | 0.85 | continue | 0.95: 100% | 0.65: 5.538%; 0.75: 15.268%; 0.85: 25.001%; 0.95: 54.193% | 1.000 -> 3.083 |
| P | P Offer | 0.95 | continue | 0.95: 100% | 0.55: 1.815%; 0.65: 9.392%; 0.75: 16.968%; 0.85: 24.547%; 0.95: 47.278% | 1.000 -> 3.650 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
