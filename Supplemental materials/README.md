# Supplemental materials: revision status

## Current numerical robustness output

[Multiple equilibria](Multiple%20equilibria/) replaces the old `Robustness checks` folder. Its README describes the current multiple-start design, recovery catalogs, outcome/range tables, and diagnostic figures. The fixed-signal ten-versus-fifteen comparisons are integrated into [Results](../Results/).

## Explanatory assets

The following folders contain explanatory assets for the appendix revision. Their intended roles are:

- `Game tree diagrams`: regenerated from the current continuous-merits baseline on an illustrative two-signal, two-offer grid. Six PDFs, their LaTeX sources, matching `.txt` explanations, two previews, and a parameter/regeneration README are included. Explanatory prose is outside the diagrams. Full views expand terminal lotteries; simplified views use expected payoffs. The beginning views are identical because continuous merits are integrated out in both. These are structural illustrations with chance probabilities, not solved equilibria or the production-grid results.
- `Liability signals diagrams`: contains the one retained default diagram, renamed `Truth-conditioned merits - party signals.pdf`. Its construction and parameter settings match the truth-conditioned ten-point merits robustness specification; it shows party signals, not the court's two-bin signal. The nine unused prior/noise/small-game variants were removed. The main continuous-merits and direct-binary models require different illustrations.
- `Risk aversion`: `risk aversion v2.tex` contains a reusable CARA plotting source. Its moderate curve uses alpha 2, matching the current moderate-risk-aversion cases. A revised appendix may show only risk neutrality and that curve.
- `Information set pressure analysis`: a historical log from the older model, retained for methodological reference. It has not yet been redone for the current production model.

## Planned appendix structure

1. **A: Model and computation.** Primitives, chronology, truth and continuous merits, signals and quadrature, payoff/cost timing, equilibrium computation and verification, outcome definitions, and accounting identities.
2. **B: Alternative information specifications.** Direct-binary signals, truth-conditioned discrete merits, and alternative continuous merits distributions.
3. **C: Parameter and participation checks.** Noise, risk aversion, cost levels/timing, mandatory entry, and restrictions on later exit.
4. **D: Equilibrium and offer-grid robustness.** Current CS004ME recoveries and outcome ranges; CS004 ten-versus-fifteen comparisons with fixed signals and non-nested grids.
5. **E: Reproducibility.** Data dictionary, exhibit-to-source mapping, code/manifests, full strategy/action reports, and an index of research diagrams.

## Recommended mechanism analysis, not yet performed

Use a few current information-set/action reports to explain final-equilibrium filing, answering, and offer choices. Report reach, the selected and alternative actions, conditional utility differences, and any mixing. Do not interpret conditional utilities at off-path information sets.

A focused successor to the old pressure analysis would add a separate counterfactual calculation: hold the American equilibrium strategies fixed, change the fee rule, recompute action utilities, and identify the resulting profitable deviations. Compare those incentives with the final British equilibrium. Recompute under the current payoff and signal implementation; differences between the two final-equilibrium CSVs alone do not isolate the direct fee-rule effect.

Choose one or two participation thresholds and one offer threshold if they explain the findings clearly. Any subsequent sequence of strategy adjustments is a diagnostic construction, not evidence that real litigants follow that adjustment path or that it selects the British equilibrium uniquely. Most detail belongs in the supplement; a compact worked example can appear in the article. This reporting exercise should use the stored equilibria and ordinarily does not require solving the production suite again.
