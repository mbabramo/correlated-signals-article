# Numbered main tables

PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text.

| Exhibit | Canonical source |
|---|---|
| [Table 1 - Model primitives](<Table 1 - Model primitives.pdf>) | [model-primitives](<../Supplemental materials/Game tree diagrams/model-primitives.pdf>) |
| [Table 2 - Strategy mechanisms](<Table 2 - Strategy mechanisms.pdf>) | [selected-strategy-mechanisms](<../Supplemental materials/Equilibrium strategy changes/Tables/selected-strategy-mechanisms.pdf>) |
| [Table 3 - Risk-averse strategy changes](<Table 3 - Risk-averse strategy changes.pdf>) | [Risk-averse selection](<../Supplemental materials/Equilibrium strategy changes/Tables/selected-risk-averse-strategy-mechanisms.pdf>) |
| [Table 4 - Welfare outcomes](<Table 4 - Welfare outcomes.pdf>) | [Combined welfare comparison](<../Results/Aggregated Data/Baseline/Risk Comparison/cost-1-welfare-outcomes.pdf>) |

Regenerate Tables 2 and 3 from ACESim4 with `LitigCharts equilibrium-manuscript --input <strategy-change directory> --article <article repository>`. The article uses three risk-neutral and nine risk-averse illustrative rows, without sensitivity markers. Both selections omit zero remaining contributions; Table 3 retains opponent-exit contributions. The complete seven-panel analysis and diagnostic checks remain in `Supplemental materials/Equilibrium strategy changes/Tables/manuscript-strategy-mechanisms.pdf` and its sources.

The routine main-exhibit publisher refreshes Table 4, which presents the five welfare measures for both risk preferences, rounded to three decimals. All welfare results appear in the manuscript's Welfare Analysis section. Table 1 comes from the separate game-tree workflow. `manuscript-exhibits.json` records source/output hashes. The main selection contains six figures and four tables.
