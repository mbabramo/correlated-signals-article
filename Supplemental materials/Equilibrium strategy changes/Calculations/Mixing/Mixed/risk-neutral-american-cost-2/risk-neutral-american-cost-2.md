# risk-neutral-american-cost-2: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-2__Fee-American`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.000000 | 0.104794 | 1 | 2.50001E-10 | Coordinate search converged within improvement tolerance |
| reverse | 0.000000 | 0.104794 | 1 | 2.50001E-10 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **0**, D **2.5000091E-10** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 28.431000 | 45.949671 | 13.745517 | 11.873812 | 0.000000 |
| forward | 28.431000 | 45.949671 | 13.745517 | 11.873812 | 0.000000 |
| reverse | 28.431000 | 45.949671 | 13.745517 | 11.873812 | 0.000000 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.55 | continue | 0.75: 100% | 0.25: 0.736%; 0.35: 3.319%; 0.45: 5.903%; 0.55: 8.487%; 0.65: 11.071%; 0.75: 16.417%; 0.85: 27.034%; 0.95: 27.034% | 1.000 -> 5.889 |
| P | P Offer | 0.65 | continue | 0.85: 100% | 0.25: 1.064%; 0.35: 3.576%; 0.45: 6.087%; 0.55: 8.599%; 0.65: 11.111%; 0.75: 16.308%; 0.85: 26.627%; 0.95: 26.627% | 1.000 -> 6.010 |
| P | P Offer | 0.75 | continue | 0.85: 100% | 0.15: 0.238%; 0.25: 2.44%; 0.35: 4.643%; 0.45: 6.846%; 0.55: 9.049%; 0.65: 11.252%; 0.75: 15.81%; 0.85: 24.861%; 0.95: 24.861% | 1.000 -> 6.540 |
| P | P Offer | 0.85 | continue | 0.85: 100% | 0.15: 2.555%; 0.25: 4.288%; 0.35: 6.021%; 0.45: 7.755%; 0.55: 9.488%; 0.65: 11.222%; 0.75: 14.809%; 0.85: 21.931%; 0.95: 21.931% | 1.000 -> 7.489 |
| P | P Offer | 0.95 | continue | 0.95: 100% | 0.15: 5.138%; 0.25: 6.348%; 0.35: 7.558%; 0.45: 8.768%; 0.55: 9.978%; 0.65: 11.188%; 0.75: 13.692%; 0.85: 18.664%; 0.95: 18.664% | 1.000 -> 8.248 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
