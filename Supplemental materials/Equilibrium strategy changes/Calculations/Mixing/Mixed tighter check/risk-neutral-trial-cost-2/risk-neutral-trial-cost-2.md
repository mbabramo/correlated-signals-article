# risk-neutral-trial-cost-2: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-2__Fee-British`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.058027 | 0.190994 | 1 | 2.50022E-11 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **0**, D **2.5002223E-11** (reported utility units). Acceptance limit: 1E-10. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 28.431000 | 43.435453 | 13.212325 | 9.763754 | 5.157468 |
| forward | 28.431000 | 43.435453 | 13.212325 | 9.763754 | 5.157468 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.45 | exit | 0.55: 100% | 0.15: 9.741%; 0.25: 10.295%; 0.35: 10.849%; 0.45: 11.403%; 0.55: 11.957%; 0.65: 12.504%; 0.75: 12.24%; 0.85: 10.506%; 0.95: 10.506% | 1.000 -> 8.970 |
| P | P Offer | 0.55 | exit | 0.55: 100% | 0.15: 8.747%; 0.25: 9.703%; 0.35: 10.659%; 0.45: 11.615%; 0.55: 12.57%; 0.65: 13.514%; 0.75: 13.06%; 0.85: 10.066%; 0.95: 10.066% | 1.000 -> 8.912 |
| P | P Offer | 0.55 | continue | 0.85: 100% | 0.15: 0.525%; 0.25: 2.594%; 0.35: 4.662%; 0.45: 6.731%; 0.55: 8.8%; 0.65: 10.971%; 0.75: 17.585%; 0.85: 24.066%; 0.95: 24.066% | 1.000 -> 6.648 |
| P | P Offer | 0.65 | continue | 0.95: 100% | 0.35: 1.243%; 0.45: 4.183%; 0.55: 7.123%; 0.65: 10.208%; 0.75: 19.607%; 0.85: 28.818%; 0.95: 28.818% | 1.000 -> 5.181 |
| P | P Offer | 0.75 | continue | 0.95: 100% | 0.25: 0.234%; 0.35: 2.813%; 0.45: 5.391%; 0.55: 7.97%; 0.65: 10.676%; 0.75: 18.919%; 0.85: 26.998%; 0.95: 26.998% | 1.000 -> 5.666 |
| P | P Offer | 0.85 | continue | 0.95: 100% | 0.15: 0.727%; 0.25: 2.757%; 0.35: 4.786%; 0.45: 6.815%; 0.55: 8.844%; 0.65: 10.974%; 0.75: 17.461%; 0.85: 23.818%; 0.95: 23.818% | 1.000 -> 6.743 |
| P | P Offer | 0.95 | continue | 0.95: 100% | 0.15: 3.863%; 0.25: 5.28%; 0.35: 6.696%; 0.45: 8.112%; 0.55: 9.529%; 0.65: 11.015%; 0.75: 15.543%; 0.85: 19.981%; 0.95: 19.981% | 1.000 -> 7.891 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
