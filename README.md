# Correlated-signals litigation article

The September 14 rebuild contains 124 retained cases. Baseline crosses **American, Trial Fee-Shifting, Complete Fee-Shifting** with **risk neutrality and symmetric CARA alpha 2** at costs **0.25, 0.5, 1, 2, 4**. The other 94 cases cover the retained information, cost-timing and offer-grid comparisons. All 124 saved equilibria were revalidated and reports regenerated; substantive results match their prior reports. No fresh equilibrium solve was needed.

## Reading the collection

- [Figures](Figures/README.md): four numbered main figures, including the three-rule strategy figure and six-case dispositions.
- [Tables](Tables/README.md): three numbered main tables: model primitives, welfare outcomes and selected strategy mechanisms.
- [Results](Results/README.md): the full routine study. Figures and tables share `Aggregated Data/<Specification>/<Risk Neutral|Risk Averse|Risk Comparison>`. Each cost has separate welfare and disposition files. PDF/PNG sit in the display folder; TeX/CSV/JSON sit in its `Sources` folder.
- [Supplemental materials](<Supplemental materials/README.md>): separate solution-path, game-tree, signal, multiple-equilibrium and strategy-change workflows. Ordinary parameter variations remain in Results.
- [Main exhibit manifest](manuscript-exhibits.json): exact canonical-source and numbered-output hashes, including caption companions.
- [Verification record](<Results/Run records/final-verification.json>): coverage, source/output hashes and validation of the relocated collection.

There are 937 routine exhibits: 744 individual diagrams, 57 strategy figures, 68 welfare tables and 68 disposition charts. The 68 table/chart pairs include separate RN and RA views plus combined views where both are available. All headline welfare and disposition values use the population of potential disputes, including nonfiling. The five welfare measures are distinct, not an additive index.

## Regeneration

Run `scripts/Rebuild-ArticleResults.ps1` **from the ACESim4 repository**. It produces the retained suite and diagrams, using all available processors by default. `-DiagramsOnly` uses completed reports. A clean rebuild begins with the code repository's `scripts/Prepare-ArticleRebuild.ps1`, which preserves the 124 required profiles before clearing ReportResults. See [the workflow](Results/README.md) for exact behavior and validation.

After production and diagram verification, run this repository's `scripts/Import-ArticleResults.ps1`, followed by `python scripts/assemble_manuscript_exhibits.py`. Import replaces Results and clears Figures/Tables; assembly repopulates the numbered main exhibits and their source/caption companions. `python scripts/verify_article_results.py` checks the imported collection. Existing separate supplemental calculations are retained, with exact original inputs and live requests that use the new paths.

The original labels in option-set names are unchanged: CS004 `Fee-British` means Trial Fee-Shifting; CS006EF `ExitFees-AllUnilateralExits` means Complete Fee-Shifting. Initial nonanswer and later unilateral exit both trigger the latter rule. There is no separate exit-extension results folder. Mandatory participation/no-exit cases are removed from the routine study and active article outputs.

The authoritative revision plan is `G:/My Drive/Articles, books in progress/Machine learning model of litigation/Correlated signals revision/ALER_revision_outline_final.md`. The numbered standalone main exhibits are ready for insertion; the article manuscript, numbered online appendix and journal submission proof still require revision. The existing manuscript is the earlier draft and has not been rewritten by this results task.

Checkpoint commits preserve superseded files; no archive directory is used. Numerical production ran from clean source `ca50fe16c1ca683209db14bdcd3a177ad2c84c4f`. Source/build manifests, reused-profile hashes and verification records are in Results/Run records. No push is included in this workflow.
