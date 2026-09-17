# Findings from the six-case search

The ordinary-cost study completed fifty requested initializations for each fee/risk case. The table distinguishes successful recoveries from distinct strategy profiles. The 32 unsuccessful final exact attempts reached the configured pivot cutoff: 17 in risk-averse American and 15 in risk-averse Complete Fee-Shifting. These were completed searches with unsuccessful attempts, not cases still running.

| Risk | Fee rule | Verified recoveries | Distinct profiles |
|---|---|---:|---:|
| Neutral | American | 50 | 21 |
| Neutral | Trial Fee-Shifting | 50 | 11 |
| Neutral | Complete Fee-Shifting | 50 | 15 |
| Averse | American | 33 | 12 |
| Averse | Trial Fee-Shifting | 50 | 19 |
| Averse | Complete Fee-Shifting | 35 | 7 |

All 85 saved profiles passed a fresh best-response check, with a maximum computed gain of 3.41 × 10⁻¹³. This floating-point audit is separate from the solver's original numerical method. It also reproduced 40,800 saved action-report rows. The seven tables and 510 individual figures are indexed in multiple-equilibria-exhibits.json. Recovery frequencies are numerical search diagnostics, not estimates of equilibrium-selection probabilities, and the search does not enumerate all equilibria.

Across the recovered risk-neutral profiles, all five headline welfare measures and all seven disposition shares are invariant at source-report precision within each fee rule. Strategies nevertheless differ, including conditional offer means. Thus the risk-neutral comparison of welfare and dispositions survives this check; it does not establish that every strategic mechanism is identical across profiles.

Risk-averse profiles have substantial outcome variation. Unconditional settlement ranges from 0.138330 to 0.927347 under American, 0.141728 to 0.485777 under Trial Fee-Shifting, and 0.638363 to 0.958995 under Complete Fee-Shifting. Every recovered risk-averse Complete Fee-Shifting profile therefore has more settlement than every recovered risk-averse Trial Fee-Shifting profile. Other welfare rankings overlap and should not be generalized from the selected main-text equilibria.

The main text should describe the American-rule result that risk aversion can raise settlement, expenditures and gross outcome error as a result for the selected equilibria. American settlement is higher than the risk-neutral baseline in every recovered risk-averse profile, but the expenditure and error increases are not invariant across this set. Trial Fee-Shifting does not have an invariant increase in settlement when moving to risk aversion. Qualify these claims where they first appear, as well as in the sensitivity section.

Use Risk Comparison/cost-1-equilibrium-recoveries for Appendix D1. Use the welfare-outcome-ranges and disposition-ranges tables in that folder as separate panels or parts of Appendix D2. Their editable layouts, captions and data are under Sources. Retain the original profile identities when illustrating a particular equilibrium. All headline outcomes are population averages; conditional offer statistics are labeled diagnostics.

Sources/reporting-repair.json explains why the original wrapper's preserved run record says Failed even though the numerical searches completed and the repaired reports passed verification. Sources/final-verification.json records numerical and artifact checks, and Sources/visual-verification.json identifies the tables and sample figures visually reviewed.

## Diversity under risk aversion

All figures below use cost multiplier 1 and symmetric CARA alpha 2. Filing and disposition percentages refer to all potential disputes. Withdrawal combines plaintiff abandonment and defendant default after answering, allocating mutual give-up once. It excludes nonfiling and nonanswer.

| Measure | American | Trial Fee-Shifting | Complete Fee-Shifting |
|---|---:|---:|---:|
| Distinct recovered profiles | 12 | 19 | 7 |
| Filing | 60.8–100% | 71.6–100% | 71.6–100% |
| Settlement | 13.8–92.7% | 14.2–48.6% | 63.8–95.9% |
| Withdrawal | 0–12.3% | 20.9–26.6% | 2.0–5.2% |
| Trial | 7.3–11.9% | 2.1–3.2% | 2.1–3.5% |
| Plaintiff shortfall contribution | 0.198–0.283 | 0.197–0.267 | 0.210–0.298 |
| Nonliable defendant contribution | 0.154–0.283 | 0.161–0.257 | 0.148–0.295 |
| Liable defendant contribution | 0.005–0.023 | 0.010–0.021 | 0.005–0.039 |
| Gross outcome error | 0.276–0.373 | 0.282–0.318 | 0.298–0.380 |
| Real litigation costs | 0.181–0.336 | 0.182–0.265 | 0.221–0.309 |

American profiles 1–3 have universal filing and answering, no withdrawal, and 88.1–92.7% settlement. Other profiles have substantial nonfiling or nonanswer and, in some cases, withdrawal. Profile 12 combines 28.4% nonfiling and 45.9% nonanswer with only 13.8% settlement. Its costs are 0.181, compared with 0.336 in profile 1.

American profiles 4 and 5 illustrate different incidence despite almost identical settlement and trial shares (42.7% and 11.9%). Profile 4 has 39.2% nonfiling and 6.2% plaintiff abandonment; profile 5 has universal filing, 39.2% nonanswer, and 6.2% defendant default after answering. Plaintiff shortfall contributions are 0.261 and 0.198, nonliable-defendant contributions 0.154 and 0.261, and costs 0.218 and 0.277, respectively. Observing the settlement share alone would conceal these differences.

Trial Fee-Shifting's 19 strategy profiles reduce to four distinct bundles of filing, disposition and headline welfare outcomes at six decimals. Seventeen profiles share the two bundles with 14.2% or 17.2% settlement; the remaining two have 45.1% or 48.6% settlement. Every recovered profile has substantial withdrawal (20.9–26.6%) and very little trial.

Complete Fee-Shifting has two broad groups: four profiles with 71.6% filing and approximately 64% settlement, and three with universal filing and 93.1–95.9% settlement. Defendants answer in every recovered profile. The latter group's expenditure range is 0.306–0.309, compared with 0.221–0.225 in the former. More settlement across all potential disputes can therefore coexist with higher expenditure because more disputes enter litigation.

Across all recovered profiles, risk aversion reduces trial relative to the risk-neutral outcome under each fee rule. Complete Fee-Shifting always has more settlement and less withdrawal than Trial Fee-Shifting under risk aversion. Risk aversion's effect on meritorious-plaintiff and nonliable-defendant contributions can go in either direction under each rule; the liable-defendant contribution falls throughout the recovered samples. Gross outcome error rises in every recovered risk-averse Trial and Complete profile and in 11 of 12 American profiles. Trial Fee-Shifting's costs fall throughout its recovered risk-averse sample, whereas the cost changes under American and Complete depend on the selected profile.

The individual diagrams were corrected after a subsequent comparison with the action records exposed pooled paths in the original manual reports. All 85 profiles were replayed separately, reproducing 486,233 numeric outcome cells; the outcome and range files are unchanged. The corrected code passed six regression/report tests, and 1,700 displayed filing percentages were checked against the action records. The earlier visual review checked rendering and missed this semantic error. Use the finished individual diagrams, not the preserved original production TeX.
