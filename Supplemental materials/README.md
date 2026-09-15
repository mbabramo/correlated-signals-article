# Separate supplemental workflows

This folder is reserved for analyses or illustrations generated separately from the routine parameter study. Placement here does not determine whether a particular exhibit appears in the main text or an online appendix. Standard parameter variation belongs in Results.

The directed-comparison expansion is complete: 90 original/mixed/tighter-checked tables cover all six fee transitions within each risk preference and both risk directions within every fee rule, across five costs. The comparison audit verifies 6,520 printed numeric entries and 2,760 fingerprints; all 90 tables and revised main Table 3 were visually reviewed. All six exact path replays are verified, including both Complete Fee-Shifting cases; the combined viewer and six individual viewers are complete. The six-case fifty-start search was interrupted by a computer restart and restarted at 06:54 Eastern on September 15; its old reference outputs will be replaced only after the new records verify. See expansion-status.json and each workflow's completion manifests.

| Folder | Contents and role |
|---|---|
| [Equilibrium solution paths](<Equilibrium solution paths/README.md>) | Separate trajectory/replay calculations, original solve logs, and interactive path diagrams |
| [Game tree diagrams](<Game tree diagrams/README.md>) | Reduced structural trees, worked saved-equilibrium path, and the primitives/fee-trigger table |
| [Liability signals diagrams](<Liability signals diagrams/README.md>) | Separate signal-architecture probability illustrations and their data |
| [Multiple equilibria](<Multiple equilibria/README.md>) | Six-case multiple-start study, recovery/dispersion records and associated diagrams; expansion running |
| [Equilibrium strategy changes](<Equilibrium strategy changes/README.md>) | All 90 directed fee/risk comparisons, mixing checks and the selected main strategy table |

Participation restrictions, Cost comparisons, Risk aversion and Fee shifting on exit are no longer separate folders. Complete Fee-Shifting is in Results/Aggregated Data/Baseline. Cost, noise, preference and grid comparisons share the ordinary Results structure and exhibit formats. Multiple equilibria remains a separate production plan rather than part of the default retained-study run.

Original inputs for separate calculations are preserved exactly, since a report rebuild can reserialize an equilibrium or action report without changing its outcomes. Live requests now point to those preserved local inputs. Recorded requests and calculation JSON retain their historical provenance; they are not the requests to use for a new run.

The revision plan proposes nine numbered online figures and sixteen tables. That appendix manuscript is still to be assembled. Current main outputs are the four numbered Figures and three numbered Tables at the repository root. Use their Sources caption companions and manuscript-exhibits.json for insertion and attribution. Git history retains superseded material; there is no archive directory.
