# risk-neutral-complete-cost-1: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-1__Fee-British__ExitFees-AllUnilateralExits`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward | 0.000000 | 0.063566 | 1 | 2.50001E-10 | Coordinate search converged within improvement tolerance |
| reverse (selected) | 0.000000 | 0.063566 | 1 | 2.50001E-10 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **2.5000091E-10**, D **0** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 39.241000 | 0.000000 | 35.138531 | 25.620469 | 0.000000 |
| forward | 39.241000 | 0.000000 | 35.138531 | 25.620469 | 0.000000 |
| reverse | 39.241000 | 0.000000 | 35.138531 | 25.620469 | 0.000000 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| D | D Offer | 0.05 | continue | 0.05: 100% | 0.05: 56.633%; 0.15: 33.333%; 0.25: 10.033% | 1.000 -> 2.507 |
| D | D Offer | 0.15 | continue | 0.05: 100% | 0.05: 63.248%; 0.15: 33.333%; 0.25: 3.419% | 1.000 -> 2.163 |
| D | D Offer | 0.25 | continue | 0.05: 100% | 0.05: 66.77%; 0.15: 33.23% | 1.000 -> 1.889 |
| D | D Offer | 0.35 | continue | 0.05: 100% | 0.05: 66.681%; 0.15: 33.319% | 1.000 -> 1.890 |
| D | D Offer | 0.45 | continue | 0.05: 100% | 0.05: 63.109%; 0.15: 33.333%; 0.25: 3.558% | 1.000 -> 2.171 |
| D | D Offer | 0.55 | continue | 0.15: 100% | 0.05: 57.314%; 0.15: 33.333%; 0.25: 9.353% | 1.000 -> 2.476 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
