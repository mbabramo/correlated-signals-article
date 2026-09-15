# risk-averse-trial-cost-1: equilibrium-preserving mixing

Source specification: `Specification-ModerateRiskAversion__Cost-1__Fee-British`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.039877 | 0.084163 | 2 | 2.48974E-11 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **2.4897417E-11**, D **2.1600499E-11** (reported utility units). Acceptance limit: 1E-10. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 28.431000 | 25.539189 | 17.187622 | 2.272451 | 26.569738 |
| forward | 28.431000 | 25.539189 | 17.187623 | 2.272451 | 26.569738 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| P | P Offer | 0.65 | continue | 0.65: 100% | 0.65: 23.175%; 0.75: 23.962%; 0.85: 24.832%; 0.95: 28.031% | 1.000 -> 3.989 |
| P | P Offer | 0.75 | continue | 0.75: 43.081%; 0.85: 56.919% | 0.65: 0.953%; 0.75: 11.326%; 0.85: 22.79%; 0.95: 64.932% | 1.981 -> 2.480 |
| P | P Offer | 0.85 | continue | 0.85: 1.004%; 0.95: 98.996% | 0.65: 1.073%; 0.75: 11.394%; 0.85: 22.801%; 0.95: 64.733% | 1.058 -> 2.496 |
| P | P Offer | 0.95 | continue | 0.95: 100% | 0.65: 4.596%; 0.75: 13.397%; 0.85: 23.124%; 0.95: 58.883% | 1.000 -> 2.890 |
| D | D Offer | 0.35 | continue | 0.15: 40.367%; 0.25: 59.633% | 0.05: 33.333%; 0.15: 33.333%; 0.25: 33.333% | 1.963 -> 3.000 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
