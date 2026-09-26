# Equilibrium tremble sensitivity

All 199 accepted approximate profiles and four exact primary profiles passed baseline reproduction and the completed sensitivity checks. No equilibrium solve was run.

At each opponent information set, the saved behavior was mixed with a uniform distribution or one of four frozen nonuniform full-support distributions. Tremble probabilities were 0.1%, 0.5% and 1%; each player was optimized separately. Chance probabilities and the full game were unchanged.

The main statistic below is the largest *additional* best-response gain at 1% trembles across both players and five directions, relative to that profile's no-tremble gap. Gains are expressed as a percentage of the responding player's full terminal utility range. Repeated discoveries count as separate profiles; these counts do not measure equilibrium likelihood.

| Risk | Rule / profile group | Profiles | Median additional gain (%) | Range (%) | Median largest behavior change (%) |
|---|---|---:|---:|---:|---:|
| Risk neutral | American | 50 | 0.0448 | 0.0011–0.0903 | 15.83 |
| Risk neutral | British / no reversal | 50 | 0.0148 | -0.0030–0.0555 | 20.06 |
| Risk averse | American | 50 | 0.0125 | 0.0054–0.0396 | 4.45 |
| Risk averse | British / no reversal | 34 | 0.0089 | 0.0049–0.0788 | 14.68 |
| Risk averse | British / plaintiff reversal | 11 | 0.0480 | 0.0408–0.0864 | 18.67 |
| Risk averse | British / defendant reversal | 4 | 0.0539 | 0.0425–0.0593 | 19.68 |

Behavior change is total-variation distance from the zero-tremble selected response, averaged over information sets using original reach weights. All off-path policies remain included in the complete records and are summarized separately.

Response selection preserves original probabilities among actions within 1e-10 of the full terminal utility range of optimal continuation value. Every selected complete policy was independently checked against the untouched best-response value; its residual must be at most 1e-8. The precise gain uses the engine's unchanged strict best-response value.

The CSV includes each welfare and disposition change relative to the no-tremble response. These are unilateral response experiments, not new equilibria, not a proof of trembling-hand perfection, and not predictions of selection frequency.

[Per-profile results](profiles.csv) · [All tests](all-tremble-tests.csv) · [Protocol, hashes and validation](validation-and-summary.json)

Here, a reversal means that British has greater meritorious-plaintiff shortfall or greater nonliable-defendant burden than the exact primary American profile. The median additional gain for other British risk-averse profiles is 0.0089% of the full terminal utility range.

For the 11 plaintiff reversal profiles, the median additional incentive to change at 1% trembles is 0.0480% (5.37 times the other British profiles). The unfavorable comparison remains in 110/110 matched unilateral-response experiments.

For the 4 defendant reversal profiles, the median additional incentive to change at 1% trembles is 0.0539% (6.04 times the other British profiles). The unfavorable comparison remains in 40/40 matched unilateral-response experiments.

Sensitivity here means additional incentive to respond to an opponent's mistakes. It does not mean an equilibrium collapses or becomes unlikely. One player responds to a perturbed opponent; both players are not re-equilibrated. The absolute incentives remain small.

All report fields reproduce the frozen diagnostic results exactly. The 32 independent best-response comparisons and 16 outcome checks passed. [Reproduction validation](reproduction-validation.json) · [Independent checks](independent-br-validation.json).
