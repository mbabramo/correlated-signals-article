# risk-averse-american-cost-2: equilibrium-preserving mixing

Source specification: `Specification-ModerateRiskAversion__Cost-2__Fee-American`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.064194 | 0.175077 | 1 | 2.52385E-11 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **0**, D **2.5238478E-11** (reported utility units). Acceptance limit: 1E-10. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 39.241000 | 45.321279 | 8.953021 | 2.848478 | 3.636222 |
| forward | 39.241000 | 45.321279 | 8.953021 | 2.848478 | 3.636222 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.55 | exit | 0.85: 100% | 0.15: 8.412%; 0.25: 9.033%; 0.35: 9.72%; 0.45: 10.48%; 0.55: 11.319%; 0.65: 12.246%; 0.75: 13.292%; 0.85: 13.097%; 0.95: 12.4% | 1.000 -> 8.895 |
| P | P Offer | 0.65 | exit | 0.75: 81.005%; 0.85: 18.995% | 0.15: 1.181%; 0.25: 3.468%; 0.35: 5.995%; 0.45: 8.788%; 0.55: 11.876%; 0.65: 15.287%; 0.75: 19.134%; 0.85: 18.417%; 0.95: 15.854% | 1.626 -> 7.475 |
| P | P Offer | 0.65 | continue | 0.85: 100% | 0.15: 0.694%; 0.25: 2.224%; 0.35: 3.914%; 0.45: 5.782%; 0.55: 7.846%; 0.65: 10.128%; 0.75: 13.868%; 0.85: 26.489%; 0.95: 29.055% | 1.000 -> 6.218 |
| P | P Offer | 0.75 | continue | 0.85: 100% | 0.55: 1.715%; 0.65: 6.047%; 0.75: 13.147%; 0.85: 37.109%; 0.95: 41.982% | 1.000 -> 3.450 |
| P | P Offer | 0.85 | continue | 0.85: 100% | 0.35: 1.308%; 0.45: 3.743%; 0.55: 6.435%; 0.65: 9.409%; 0.75: 14.284%; 0.85: 30.738%; 0.95: 34.084% | 1.000 -> 4.884 |
| P | P Offer | 0.95 | continue | 0.85: 100% | 0.15: 2.75%; 0.25: 3.977%; 0.35: 5.334%; 0.45: 6.833%; 0.55: 8.491%; 0.65: 10.322%; 0.75: 13.324%; 0.85: 23.454%; 0.95: 25.515% | 1.000 -> 7.155 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
