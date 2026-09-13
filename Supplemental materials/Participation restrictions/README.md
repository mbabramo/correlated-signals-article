# Participation restrictions

These are separate extension comparisons, not scenarios in main Figure 4.

- [Mandatory entry](mandatory-entry-dispositions.pdf): mandatory filing and answering, with later exit available.
- [Mandatory entry without later exit](mandatory-entry-no-exit-dispositions.pdf): mandatory filing and answering, with abandonment/default unavailable.

Each PDF includes baseline and its restriction under American and British fee rules,
at cost multiplier 1 with ten offers. Comparing the second restriction with baseline
changes both entry and later exit; it does not isolate the effect of later exit alone.
The same baseline is repeated only as a comparison, not as additional simulations.

All bars use all potential disputes as the denominator and the same seven-category
palette as main Figure 4. Captions, exact source-row data and hashes are in matching
TXT/JSON files. PNG previews and standalone TeX are also retained.

The two request files select saved numerical rows. The article's `article-diagrams.json`
lists their outputs under `AdditionalDispositionFigures`. From ACESim4, run:

```text
dotnet run --project LitigCharts -c Release -- diagrams dispositions --config "C:/Users/Admin/source/repos/correlated-signals-article/article-diagrams.json"
```

This regenerates main Figure 4 and both files here. `publication` and `all` include
them too; `--list`, `--sources-only`, `--compile-only`, and `--output-root` are supported.
No equilibrium solving or manual production-setting change is required.

These are available supplementary illustrations alongside planned Table C2, not
additional required numbered appendix figures. Assign numbers only if selected
for an appendix manuscript.
