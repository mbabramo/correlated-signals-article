# Numbered main tables

PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text. Captions and costs are not added inside the research artwork.

| Exhibit | Canonical source |
|---|---|
| [Table 1 - Model primitives](<Table 1 - Model primitives.pdf>) | [model-primitives](<../Supplemental materials/Game tree diagrams/model-primitives.pdf>) |
| [Table 2 - Welfare outcomes](<Table 2 - Welfare outcomes.pdf>) | [cost-1-welfare-outcomes](<../Results/Aggregated Data/Baseline/Risk Comparison/cost-1-welfare-outcomes.pdf>) |
| [Table 3 - Strategy mechanisms](<Table 3 - Strategy mechanisms.pdf>) | [manuscript-strategy-mechanisms](<../Supplemental materials/Equilibrium strategy changes/Tables/manuscript-strategy-mechanisms.pdf>) |

Publish the completed routine collection with ACESim4's `scripts/Publish-ArticleResults.ps1` to refresh Table 2 and its source records. Its five outcome columns use three decimal places. Table 1 comes from the separate game-tree workflow.

Regenerate Table 3 from ACESim4 with `LitigCharts equilibrium-manuscript --input <strategy-change directory> --article <article repository>`. The supplemental rebuild generates its canonical source automatically. All qualifying rows in the seven specified comparisons are retained. The PDF contains every page; the ordinary PNG is page one and additional PNGs have numbered page suffixes. `manuscript-exhibits.json` records the numbered files and their source/output hashes.

The revision plan retains four main figures and three main tables. Numbered online appendices, manuscript insertion and submission-proof review remain separate writing and packaging work.
