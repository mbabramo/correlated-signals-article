# Equilibrium-preserving mixing exploration

This explores local equilibrium-preserving mixing around the original equilibrium. It does not find or certify a globally maximally mixed equilibrium, enumerate all equilibria, or impose quantal response.

A player's same-decision information sets change jointly across signals and reached exit branches. They are mutually exclusive on any path in the supported one-round game, making their joint deviation comparisons affine. Candidate actions include current support and actions tied in conditional utility under current continuation play. A quadratic program spreads probability subject to full-strategy deviation constraints, added by the unrestricted best-response oracle for BOTH players.

Each accepted complete profile passes the stated root-payoff deviation limit. A local utility tie alone is never treated as permission to change the equilibrium. Numerical tolerances are absolute reported utility units, not percentages of damages or a 2% equilibrium tolerance.

Only information sets reached in the original equilibrium enter the objective or can change. Source-unvisited policies stay fixed. Sets becoming unvisited are also skipped; this prevents meaningless off-path mixing from inflating the score.

Forward and reverse decision-block orders restart independently from the saved original. Their difference measures search-order sensitivity, not exhaustive bounds. Blocks can be constrained optima while the joint search remains order-dependent and only locally converged. Multiple changes in an accepted block must be applied together; intermediate partial application is not verified.

Adding or mixing actions can change opponent incentives, beliefs and outcomes. Every accepted full profile is rechecked, and final action values/reaches are retained. An evenly spread representative is a diagnostic convention, not an additional behavioral prediction.

- [risk-neutral-trial-cost-1](risk-neutral-trial-cost-1.md): mixing score 0.000000 -> 0.086896; selected forward; maximum unilateral gain 2.49951E-11.
