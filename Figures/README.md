# Numbered main figures

PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text. Captions and costs are not added inside the research artwork.

| Exhibit | Canonical source |
|---|---|
| [Figure 1 - Information structure](<Figure 1 - Information structure.pdf>) | [Continuous merits - party - bw](<../Supplemental materials/Liability signals diagrams/Continuous merits - party - bw.pdf>) |
| [Figure 2 - Worked equilibrium path](<Figure 2 - Worked equilibrium path.pdf>) | [worked equilibrium path](<../Supplemental materials/Game tree diagrams/worked equilibrium path.pdf>) |
| [Figure 3 - Participation and offers](<Figure 3 - Participation and offers.pdf>) | [cost-1-participation-and-offers](<../Results/Aggregated Data/Baseline/Risk Neutral/cost-1-participation-and-offers.pdf>) |
| [Figure 4 - Dispositions](<Figure 4 - Dispositions.pdf>) | [cost-1-dispositions](<../Results/Aggregated Data/Baseline/Risk Comparison/cost-1-dispositions.pdf>) |

After generating the routine collection, run `scripts/Publish-ArticleResults.ps1` from ACESim4 with the completed Results source and this article directory. It verifies and imports the collection, refreshes Figures 3 and 4, and preserves Figures 1 and 2 from their separate supplemental workflows. `manuscript-exhibits.json` records source/output hashes and caption companions. Publishing saved results does not determine equilibria.

The revision plan retains four main figures and three main tables. Numbered online appendices, manuscript insertion and submission-proof review remain separate writing and packaging work.
