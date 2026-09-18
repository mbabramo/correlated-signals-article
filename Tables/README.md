# Numbered main tables

PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text. Captions and costs are not added inside the research artwork.

| Exhibit | Canonical source |
|---|---|
| [Table 1 - Model primitives](<Table 1 - Model primitives.pdf>) | [model-primitives](<../Supplemental materials/Game tree diagrams/model-primitives.pdf>) |
| [Table 2 - Strategy mechanisms](<Table 2 - Strategy mechanisms.pdf>) | [selected-strategy-mechanisms](<../Supplemental materials/Equilibrium strategy changes/Tables/selected-strategy-mechanisms.pdf>) |
| [Table 3 - Risk-averse outcomes](<Table 3 - Risk-averse outcomes.pdf>) | [risk-averse-outcomes](<../Supplemental materials/Outcome summaries/risk-averse-outcomes.pdf>) |
| [Table 4 - Welfare outcomes](<Table 4 - Welfare outcomes.pdf>) | [cost-1-welfare-outcomes](<../Results/Aggregated Data/Baseline/Risk Neutral/cost-1-welfare-outcomes.pdf>) |

Publish the completed routine collection with ACESim4's `scripts/Publish-ArticleResults.ps1` to refresh Table 4 and its source records. Its five outcome columns use three decimal places. Table 1 comes from the separate game-tree workflow.

Regenerate Table 2 from ACESim4 with `LitigCharts equilibrium-manuscript --input <strategy-change directory> --article <article repository>`. The article uses three risk-neutral illustrative rows, without sensitivity markers. The full seven-panel analysis and diagnostic checks remain in `Supplemental materials/Equilibrium strategy changes/Tables/manuscript-strategy-mechanisms.pdf` and its sources. Opponent-exit and remaining contributions are zero in the selected rows and omitted from the display. `manuscript-exhibits.json` records the numbered files and their source/output hashes.

The main selection contains four figures and four tables. Table 4 contains risk-neutral welfare outcomes; Table 3 combines risk-averse dispositions and welfare measures. Table 3 is regenerated from saved outcome data by ACESim4 scripts/build_risk_averse_summary.py and refreshed with the routine main-exhibit publication command. Numbered online appendices, manuscript insertion and submission-proof review remain separate writing and packaging work.
