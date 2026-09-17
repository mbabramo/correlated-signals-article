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
