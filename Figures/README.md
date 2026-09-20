# Numbered main figures

PDF and PNG files are ready for manuscript insertion. Sources contains standalone TeX, exact-data JSON and separate caption text. Captions and costs are not added inside the research artwork.

| Exhibit | Canonical source |
|---|---|
| [Figure 1 - Information structure](<Figure 1 - Information structure.pdf>) | [Continuous merits - party - bw](<../Supplemental materials/Liability signals diagrams/Continuous merits - party - bw.pdf>) |
| [Figure 2 - Worked equilibrium path](<Figure 2 - Worked equilibrium path.pdf>) | [worked equilibrium path](<../Supplemental materials/Game tree diagrams/worked equilibrium path.pdf>) |
| [Figure 3 - Dispositions](<Figure 3 - Dispositions.pdf>) | [Risk-neutral dispositions](<../Supplemental materials/Outcome summaries/risk-neutral-dispositions.pdf>) |
| [Figure 4 - Participation and offers](<Figure 4 - Participation and offers.pdf>) | [cost-1-participation-and-offers](<../Results/Aggregated Data/Baseline/Risk Neutral/cost-1-participation-and-offers.pdf>) |
| [Figure 5 - Risk-averse dispositions](<Figure 5 - Risk-averse dispositions.pdf>) | [Risk-averse dispositions](<../Supplemental materials/Outcome summaries/risk-averse-dispositions.pdf>) |
| [Figure 6 - Risk-averse participation and offers](<Figure 6 - Risk-averse participation and offers.pdf>) | [cost-1-participation-and-offers](<../Results/Aggregated Data/Baseline/Risk Averse/cost-1-participation-and-offers.pdf>) |

Run ACESim4's `scripts/publish_article_results.py refresh-main --article <article repository>` after generating the routine collection to refresh Figures 3-6 and the combined welfare Table 4. The two disposition figures omit redundant risk headings inside the artwork; the manuscript captions identify the risk preference. Scientific data and original routine charts remain unchanged. Figures 4 and 6 show participation and offers under risk neutrality and risk aversion, respectively. The main selection contains six figures and four tables. `manuscript-exhibits.json` records source/output hashes and caption companions.
