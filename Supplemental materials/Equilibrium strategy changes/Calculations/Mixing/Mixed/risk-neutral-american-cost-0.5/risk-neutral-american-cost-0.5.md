# risk-neutral-american-cost-0.5: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-0.5__Fee-American`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.000000 | 0.156412 | 2 | 3.66947E-10 | Coordinate search converged within improvement tolerance |
| reverse | 0.000000 | 0.156335 | 2 | 3.66951E-10 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **3.6694736E-10**, D **2.5000446E-10** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 17.813000 | 17.663189 | 0.000000 | 64.523811 | 0.000000 |
| forward | 17.813000 | 17.663189 | 0.000000 | 64.523811 | 0.000000 |
| reverse | 17.813000 | 17.663189 | 0.000000 | 64.523811 | 0.000000 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.25 | continue | 0.75: 100% | 0.55: 0%; 0.65: 28.053%; 0.75: 26.302%; 0.85: 25.961%; 0.95: 19.683% | 1.000 -> 3.967 |
| P | P Offer | 0.35 | continue | 0.75: 100% | 0.65: 21.539%; 0.75: 27.337%; 0.85: 29.02%; 0.95: 22.104% | 1.000 -> 3.967 |
| P | P Offer | 0.45 | continue | 0.85: 100% | 0.65: 5.66%; 0.75: 28.337%; 0.85: 34.575%; 0.95: 31.428% | 1.000 -> 3.493 |
| P | P Offer | 0.55 | continue | 0.85: 100% | 0.75: 21.541%; 0.85: 35.284%; 0.95: 43.175% | 1.000 -> 2.889 |
| P | P Offer | 0.65 | continue | 0.95: 100% | 0.75: 9.09%; 0.85: 32.273%; 0.95: 58.637% | 1.000 -> 2.450 |
| P | P Offer | 0.75 | continue | 0.95: 100% | 0.85: 26.286%; 0.95: 73.714% | 1.000 -> 1.779 |
| P | P Offer | 0.85 | continue | 0.95: 100% | 0.85: 18.836%; 0.95: 81.164% | 1.000 -> 1.622 |
| P | P Offer | 0.95 | continue | 0.95: 100% | 0.85: 18.088%; 0.95: 81.912% | 1.000 -> 1.604 |
| D | D Offer | 0.05 | continue | 0.05: 100% | 0.05: 84.8%; 0.15: 15.2% | 1.000 -> 1.531 |
| D | D Offer | 0.15 | continue | 0.05: 100% | 0.05: 86.63%; 0.15: 13.37% | 1.000 -> 1.482 |
| D | D Offer | 0.25 | continue | 0.05: 100% | 0.05: 81.86%; 0.15: 18.14% | 1.000 -> 1.606 |
| D | D Offer | 0.35 | continue | 0.05: 100% | 0.05: 73.098%; 0.15: 26.902% | 1.000 -> 1.790 |
| D | D Offer | 0.45 | continue | 0.15: 100% | 0.05: 61.681%; 0.15: 33.62%; 0.25: 4.699% | 1.000 -> 2.244 |
| D | D Offer | 0.55 | continue | 0.15: 100% | 0.05: 48.708%; 0.15: 34.461%; 0.25: 16.831% | 1.000 -> 2.766 |
| D | D Offer | 0.65 | continue | 0.25: 100% | 0.05: 40.495%; 0.15: 34.572%; 0.25: 24.932%; 0.35: 0% | 1.000 -> 2.944 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
