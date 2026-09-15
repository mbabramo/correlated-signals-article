# risk-neutral-complete-cost-2: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-2__Fee-British__ExitFees-AllUnilateralExits`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward | 0.024921 | 0.096519 | 1 | 2.50004E-10 | Coordinate search converged within improvement tolerance |
| reverse (selected) | 0.024921 | 0.096519 | 1 | 2.50004E-10 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **2.5000446E-10**, D **0** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 47.116274 | 0.000000 | 41.161672 | 10.221985 | 1.500069 |
| forward | 47.116274 | 0.000000 | 41.161672 | 10.221985 | 1.500069 |
| reverse | 47.116274 | 0.000000 | 41.161672 | 10.221985 | 1.500069 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| D | D Offer | 0.05 | continue | 0.05: 100% | 0.05: 26.001%; 0.15: 22.097%; 0.25: 18.191%; 0.35: 14.286%; 0.45: 10.38%; 0.55: 6.476%; 0.65: 2.569% | 1.000 -> 5.920 |
| D | D Offer | 0.15 | continue | 0.05: 100% | 0.05: 30.649%; 0.15: 25.057%; 0.25: 19.463%; 0.35: 13.871%; 0.45: 8.276%; 0.55: 2.684% | 1.000 -> 4.978 |
| D | D Offer | 0.25 | continue | 0.05: 100% | 0.05: 34.215%; 0.15: 27.109%; 0.25: 19.999%; 0.35: 12.893%; 0.45: 5.784% | 1.000 -> 4.356 |
| D | D Offer | 0.35 | continue | 0.05: 100% | 0.05: 36.207%; 0.15: 28.105%; 0.25: 19.999%; 0.35: 11.897%; 0.45: 3.792% | 1.000 -> 4.153 |
| D | D Offer | 0.45 | continue | 0.05: 64.157%; 0.95: 35.843% | 0.05: 28.544%; 0.15: 20.209%; 0.25: 11.87%; 0.35: 3.534%; 0.95: 35.843% | 1.920 -> 4.137 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
