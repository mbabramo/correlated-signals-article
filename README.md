# Correlated-signals litigation article

The September 16 rebuild contains **276 verified cases**. Every retained ten-offer specification crosses **American, Trial Fee-Shifting, Complete Fee-Shifting** with **risk neutrality and symmetric CARA alpha 2** at costs **0.25, 0.5, 1, 2, 4**. Nine such families supply 270 cases; six fifteen-offer cases at cost 1 complete the collection. The run revalidated 124 saved equilibria and solved 152 additional cases. Scientific report values for the reused cases are unchanged.

## Reading the collection

- [Figures](Figures/README.md): six numbered main figures, including separate disposition and four-panel strategy figures for risk neutrality and risk aversion.
- [Tables](Tables/README.md): four numbered main tables: model primitives, selected risk-neutral strategy changes, selected risk-averse strategy changes and combined welfare outcomes.
- [Results](Results/README.md): the full routine study. Figures and tables share `Aggregated Data/<Specification>/<Risk Neutral|Risk Averse|Risk Comparison>`. Each cost has separate welfare and disposition files. PDF/PNG sit in the display folder; TeX/CSV/JSON sit in its `Sources` folder.
- [Supplemental materials](<Supplemental materials/README.md>): separate solution-path, game-tree, signal, multiple-equilibrium and strategy-change workflows. Ordinary parameter variations remain in Results.
- [Main exhibit manifest](manuscript-exhibits.json): exact canonical-source and numbered-output hashes, including caption companions.
- [Verification record](<Results/Run records/final-verification.json>): coverage, source/output hashes and validation of the relocated collection.

There are **2,024 routine exhibits**: 1,656 individual diagrams, 92 strategy figures, 138 welfare tables and 138 disposition charts. Every family has separate RN and RA views plus combined welfare/disposition views. All headline welfare and disposition values use the population of potential disputes, including nonfiling. The five welfare measures are distinct, not an additive index. All 2,760 printed welfare values passed source and rounding checks; representative visual checks cover every family and the main routine exhibits.

## Regeneration

Run `scripts/Rebuild-ArticleResults.ps1` **from the ACESim4 repository**. It produces the retained suite and diagrams, using all available processors by default. `-DiagramsOnly` uses completed reports. A clean rebuild begins with `scripts/Prepare-ArticleRebuild.ps1`, which derives the case matrix from C#, preserves available matching profiles and lists missing cases. See [the workflow](Results/README.md) for exact behavior and validation.

After production and diagram verification, run ACESim4's `scripts/Publish-ArticleResults.ps1 -ResultsSource <completed Results> -ArticleDirectory <this repository> -Python <python with pypdf>`. It verifies and imports the collection, refreshes Figures 3-6 and Table 4, and preserves the other main exhibits and separate supplemental calculations. `LitigCharts equilibrium-manuscript` refreshes Tables 2 and 3 from the saved comparisons.

The original labels in option-set names are unchanged: CS004 `Fee-British` means Trial Fee-Shifting; CS006EF `ExitFees-AllUnilateralExits` means Complete Fee-Shifting. Initial nonanswer and later unilateral exit both trigger the latter rule. There is no separate exit-extension results folder. Mandatory participation/no-exit cases are removed from the routine study and active article outputs.

The authoritative revision plan is `G:/My Drive/Articles, books in progress/Machine learning model of litigation/Correlated signals revision/ALER_revision_outline.md`. The numbered standalone main exhibits are ready for insertion; the article manuscript, numbered online appendix and journal submission proof still require revision. The manuscript introduction is being revised; exhibit insertion and the remaining text are still in progress.

Checkpoint commits preserve superseded files; no archive directory is used. Numerical production ran from clean source `68a37629ca0b5091dfc7707b6fcb7cfa68698f4d`. A subsequent rendering-only pass used the compiler timeout-retry repair. Source/build manifests, reused-profile comparisons, artifact hashes and verification records are in Results/Run records. The separate 90 strategy comparisons and six exact paths remain complete; the repaired six-case multiple-equilibrium search follows the routine-results commit. No push is included in this workflow.
