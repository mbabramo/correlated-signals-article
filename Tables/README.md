# Numbered main tables

PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text.

| Exhibit | Canonical source |
|---|---|
| [Table 1 - Model primitives](<Table 1 - Model primitives.pdf>) | [model-primitives](<../Supplemental materials/Game tree diagrams/model-primitives.pdf>) |
| [Table 2 - Strategy mechanisms](<Table 2 - Strategy mechanisms.pdf>) | [selected-strategy-mechanisms](<../Supplemental materials/Equilibrium strategy changes/Tables/selected-strategy-mechanisms.pdf>) |
| [Table 3 - Risk-averse strategy changes](<Table 3 - Risk-averse strategy changes.pdf>) | [Risk-averse selection](<../Supplemental materials/Equilibrium strategy changes/Tables/selected-risk-averse-strategy-mechanisms.pdf>) |
| [Table 4 - Welfare outcomes](<Table 4 - Welfare outcomes.pdf>) | [Combined welfare comparison](<../Results/Aggregated Data/Baseline/Risk Comparison/cost-1-welfare-outcomes.pdf>) |
| [Table 5 - Overall results summary](<Table 5 - Overall results summary.pdf>) | [All-cost comparisons](<../Supplemental materials/Generated pairwise comparisons/all-costs.md>) |
| [Table 6 - Disposition ranges](<Table 6 - Disposition ranges.pdf>) | [Multiple-equilibria risk comparison](<../Supplemental materials/Multiple equilibria/Risk Comparison/cost-1-disposition-ranges.pdf>) |

Regenerate Tables 2 and 3 from ACESim4 with `LitigCharts equilibrium-manuscript --input <strategy-change directory> --article <article repository>`. The article uses three risk-neutral and eleven risk-averse illustrative rows, without sensitivity markers. Both selections omit zero remaining contributions; Table 3 retains opponent-exit contributions. The complete seven-panel analysis and diagnostic checks remain in `Supplemental materials/Equilibrium strategy changes/Tables/manuscript-strategy-mechanisms.pdf` and its sources.

The routine main-exhibit publisher refreshes Table 4, which presents the five welfare measures for both risk preferences, rounded to three decimals. All welfare results appear in the manuscript's Welfare Analysis section. Table 1 comes from the separate game-tree workflow. `manuscript-exhibits.json` records source/output hashes. The main selection contains six figures and six tables.

## Reproduction

The [generated pairwise comparisons](<../Supplemental materials/Generated pairwise comparisons/README.md>) contain full-grid and selected-cost counts with case-level details. Regenerate Table 5 directly here with ACESim4's `python -B scripts/publish_fee_rule_summary.py --article-directory <article repository>`. It uses all five cost multipliers, reads the saved aggregate data and places editable TeX, CSV and JSON in Sources.

Regenerate Table 6 with `python -B scripts/publish_disposition_ranges.py --article-directory <article repository>`. It uses the Risk Comparison disposition ranges from the separate multiple-equilibria study at cost 1. Endpoints are rounded directly from the full-precision data to three decimal places. Sources contains editable TeX, exact-data JSON and a caption companion.
