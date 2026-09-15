# Numbered main tables

PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text. Captions and costs are not added inside the research artwork.

| Exhibit | Canonical source |
|---|---|
| [Table 1 - Model primitives](<Table 1 - Model primitives.pdf>) | [model-primitives](<../Supplemental materials/Game tree diagrams/model-primitives.pdf>) |
| [Table 2 - Welfare outcomes](<Table 2 - Welfare outcomes.pdf>) | [cost-1-welfare-outcomes](<../Results/Aggregated Data/Baseline/Risk Comparison/cost-1-welfare-outcomes.pdf>) |
| [Table 3 - Strategy mechanisms](<Table 3 - Strategy mechanisms.pdf>) | [selected-strategy-mechanisms](<../Supplemental materials/Equilibrium strategy changes/Tables/selected-strategy-mechanisms.pdf>) |

Regenerate with `python scripts/assemble_manuscript_exhibits.py` from the article repository. The script uses saved results and separate diagnostic calculations; it does not determine equilibria. `manuscript-exhibits.json` records the source/output hashes. After importing a new Results collection, rerun assembly to refresh these copies.

The revision plan retains four main figures and three main tables. Numbered online appendices, manuscript insertion and submission-proof review remain separate writing and packaging work.
