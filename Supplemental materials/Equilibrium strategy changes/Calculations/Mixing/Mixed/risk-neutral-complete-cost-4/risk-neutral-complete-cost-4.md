# risk-neutral-complete-cost-4: equilibrium-preserving mixing

Source specification: `Specification-Baseline__Cost-4__Fee-British__ExitFees-AllUnilateralExits`. Original saved equilibrium retained unchanged.

Mixing score is the equally weighted mean of (1 - sum of squared probabilities)/(1 - 1/action count) over source-reached information sets. Zero means pure; one means uniform over every action. This is a quadratic/Gini mixing measure, not Shannon entropy or a predicted randomization rule.

| Search order | Initial score | Final score | Accepted changes | Maximum gain | Status |
|---|---:|---:|---:|---:|---|
| forward (selected) | 0.030394 | 0.092735 | 1 | 2.50001E-10 | Coordinate search converged within improvement tolerance |
| reverse | 0.030394 | 0.092735 | 1 | 2.50001E-10 | Coordinate search converged within improvement tolerance |

Selected profile's unrestricted best-response gains: P **2.5000091E-10**, D **1.7763568E-15** (reported utility units). Acceptance limit: 1E-09. This checks Nash deviations at the root, not an equilibrium refinement.

## Aggregate outcomes

Unconditional percentages, partitioning all potential disputes.

| Profile | Not filed | Not answered | Settled | Trial | Exit after failed bargaining |
|---|---:|---:|---:|---:|---:|
| original | 55.954592 | 0.000000 | 40.070062 | 2.889977 | 1.085370 |
| forward | 55.954592 | 0.000000 | 40.070062 | 2.889977 | 1.085370 |
| reverse | 55.954592 | 0.000000 | 40.070062 | 2.889977 | 1.085370 |
## Strategy changes

Only changed, source-reached information sets are listed. Unvisited source policies remain frozen, including uniform loader fallbacks. Offer branches retain the player's private exit commitment.

| Player | Decision | Signal | Branch | Original distribution | Selected distribution | Effective actions, original -> selected |
|---|---|---:|---|---|---|---:|
| D | D Offer | 0.05 | continue | 0.05: 100% | 0.05: 11.111%; 0.15: 11.111%; 0.25: 11.111%; 0.35: 11.111%; 0.45: 11.111%; 0.55: 11.111%; 0.65: 11.111%; 0.75: 11.111%; 0.85: 11.111% | 1.000 -> 9.000 |
| D | D Offer | 0.15 | continue | 0.05: 100% | 0.05: 11.111%; 0.15: 11.111%; 0.25: 11.111%; 0.35: 11.111%; 0.45: 11.111%; 0.55: 11.111%; 0.65: 11.111%; 0.75: 11.111%; 0.85: 11.111% | 1.000 -> 9.000 |
| D | D Offer | 0.25 | continue | 0.05: 100% | 0.05: 11.111%; 0.15: 11.111%; 0.25: 11.111%; 0.35: 11.111%; 0.45: 11.111%; 0.55: 11.111%; 0.65: 11.111%; 0.75: 11.111%; 0.85: 11.111% | 1.000 -> 9.000 |
| D | D Offer | 0.35 | continue | 0.05: 39.502%; 0.95: 60.498% | 0.05: 4.389%; 0.15: 4.389%; 0.25: 4.389%; 0.35: 4.389%; 0.45: 4.389%; 0.55: 4.389%; 0.65: 4.389%; 0.75: 4.389%; 0.85: 4.389%; 0.95: 60.498% | 1.956 -> 4.659 |

Effective actions = exp(Shannon entropy), a supplementary measure. Displayed shares omit probabilities below the support threshold; the JSON retains all probabilities.

## Interpretation

- This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.
- A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.
- Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.
- Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.
- Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.
- Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

Full profiles, action utilities and reaches, best-response gains, every accepted block, solver statuses and input fingerprints are in the JSON files. No existing decomposition or publication figure has been replaced.
