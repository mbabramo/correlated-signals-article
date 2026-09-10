# Correlated Signals Article

Manuscript and research materials for *A Correlated Signals Computational Game Theory Model of Litigation Bargaining*.

## Current repository layout

| Directory | Contents |
|---|---|
| [Article and bibliography](Article%20and%20bibliography/) | Existing manuscript, bibliography, and saved draft. The manuscript is being revised incrementally. |
| [Figures](Figures/) | Reserved for revised publication figures. Its README maps the planned figures to current results. |
| [Results/CS004](Results/CS004/) | Main clean production output: 130 ten-offer cases and four fifteen-offer cases, including numerical and action reports, equilibria, diagrams, and solver logs. |
| [Supplemental materials/CS004ME](Supplemental%20materials/CS004ME/) | Current multiple-equilibrium exercise: 50 verified recoveries per fee rule and 21 American/11 British distinct retained profiles. |
| [Results/Provenance](Results/Provenance/) | Original suite manifest, original diagram inventory, and an import manifest mapping every imported file to its original path and SHA-256 hash. |
| [Supplemental materials](Supplemental%20materials/) | Current CS004ME output plus older explanatory assets awaiting the substantive appendix revision. See its README for status. |

The old `smalltree`, `bigtree`, `Supplemental materials/Robustness checks`, and old figure assets were replaced after checkpoint commit `7e92fc01e1d7ff92bf0b07dbe80ac9ff021ce7b3`. Their committed contents remain in Git history. The empty `Updated figures` directory is retired; revised figures will use `Figures`.

The current manuscript still refers to removed figures. Its source and saved PDF were preserved, but rebuilding the source requires replacing those references as the revised figures and sections are prepared.

## Production source

- Model and solver repository: `ACESim4`.
- Numerical production commit: `31d0f17836435a2b1a7cc3fc52a6dfcec0db3565`.
- Diagram-generator commit: `a991f31fa355d788981bf399251123c17f8ebc89`.
- Original run directory: `ReportResults/Production Runs/ALER Production 31d0f1783643` in the model repository.
- Both plans completed aggregation and required artifact/accounting validation.
- The article import verified 3,983 files byte-for-byte, including 1,358 applicable PDFs and 166 information-set/action reports.

The imported files preserve their original names and bytes. The article repository separates CS004 and CS004ME, so original manifest paths describe the source run; use `Results/Provenance/article import manifest.json` to resolve their new locations.

Full solver reproduction commands, runtime information, plan fingerprints, executable hashes, and reused-equilibrium hashes are retained in the production manifests. The coordinated run used 16 workers. The suite's stored command uses `--processors all`; substitute `--processors 16` to reproduce the resource limit used for this run.

## Reading the results

Start with `Results/CS004/CS004 numerical results.csv`, `Supplemental materials/CS004ME/CS004ME equilibrium outcomes.csv`, and `Supplemental materials/CS004ME/CS004ME equilibrium ranges.csv`.

The generated diagrams are research outputs, not finished publication exhibits. Generic legacy signal illustrations were excluded from this import. Some retained plots still require revised terminology and layout; the planned manuscript figures and the three-perspective net-outcome presentation have yet to be prepared.

## Windows paths

The preserved source filenames are long. Enable Windows long-path support if needed and configure Git in this checkout:

```powershell
git config core.longpaths true
```
