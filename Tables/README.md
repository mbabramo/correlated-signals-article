# Main-article tables

## Change-only mechanism comparison

[Equilibrium strategy changes](Equilibrium%20strategy%20changes.pdf) is the new
paper-facing candidate for the four ordinary-cost interventions. It shows only
changed decisions reached in both equilibria, with direct-first additive
contributions where the target policy can be reconciled. Selection-dependent
rows are explicitly labeled. It has its own regeneration command:

    dotnet run --project LitigCharts -c Release -- equilibrium-changes --request "C:/Users/Admin/source/repos/correlated-signals-article/equilibrium-changes.request.json"

The high-cost version and all exact diagnostics are in Supplemental materials/
Equilibrium changes. The pre-existing four numbered-in-the-manuscript tables
below are unchanged; final manuscript placement of the new comparison remains
an editorial choice.

## Existing four-table selection

The four selected main tables are assembled here under descriptive, unnumbered names. Numbering and final captions belong in the manuscript. These are editable publication assets, not a replacement for the underlying research reports.

| PDF | Content |
|---|---|
| [model-primitives.pdf](model-primitives.pdf) | Essential primitives, interpretations, and baseline settings. |
| [baseline-outcomes.pdf](baseline-outcomes.pdf) | Baseline American/British participation, dispositions, truth-conditioned participation, and the three monetary perspectives. |
| [comparative-outcomes.pdf](comparative-outcomes.pdf) | Changes from each fee regime's own baseline for the four contrasts in the disposition figure. |
| [robustness-and-sensitivity.pdf](robustness-and-sensitivity.pdf) | Separately labeled direct-binary model form, 10/15-offer grid, and original multiple-start checks. |

Each has a matching `.tex` manuscript fragment, `.png` preview, `.txt` caption/interpretation, and `.json` containing exact reported values, source CSV records, cell-level inputs and formulas, and SHA-256 source hashes. CSV record numbers include the header as record 1; they are not necessarily physical line numbers. Model-primitives also records reconstructed option settings and fingerprints the defining C# files. These four model-definition files were unchanged from production commit `31d0f17836435a2b1a7cc3fc52a6dfcec0db3565` when assembled.

## Regeneration

From the ACESim4 repository:

```powershell
dotnet run --project LitigCharts -c Release -- tables --request "C:/Users/Admin/source/repos/correlated-signals-article/publication-tables.json"
```

The C# command reads saved CSVs and constructs options only; it neither loads nor solves equilibria. The request lists exact cases and paths, resolved relative to the request file. `--sources-only` regenerates TeX/JSON/TXT without running PDF tools. Normal generation compiles with LuaLaTeX and creates PNG previews with `pdftoppm`; existing generated companions are replaced. Close these PDFs in Acrobat before regenerating. The original CSVs and manuscript files are not changed. This separate `tables` command is not implicitly included in `diagrams all`.

For editable manuscript inclusion, load `booktabs`, `tabularx`, and `array` and use a normal table float:

```latex
\begin{table}
\caption{Baseline outcomes}
\label{tab:baseline-outcomes}
\input{../Tables/baseline-outcomes.tex}
\end{table}
```

Alternatively include the PDF inside a table float using `\includegraphics[width=\linewidth]{../Tables/baseline-outcomes.pdf}`. The PDF contains a short title; the TeX fragment omits it so the manuscript controls the caption. Fragments preserve editable type and adapt to the available width. Recheck layout at the final manuscript width; the standalone PDFs use 17 cm.

## Denominators and limits

- Overall filing, reaching bargaining, settlement and trial rates use all potential disputes. Conditional answering uses the joint filing-and-answering rate divided by filing, within the stated truth group where applicable. Truth is not the court's finding.
- The baseline table's intermediate events and trial subtotal must not be added to the seven mutually exclusive dispositions. Saved abandonment/default values already include the mutual-give-up allocation.
- Monetary values are in damages units. The first three monetary measures condition on true liability/nonliability. Net Outcome Fidelity Loss is ex ante, uses the saved population components, and is not the unweighted sum of the three conditional columns. It is a one-sided, entitlement-dependent proxy, not social welfare or a judicial-error probability. Full formulas and limitations are in comparative-outcomes.txt.
- Differences are computed before display rounding. Source-data JSON retains the exact reported values; source reports themselves have finite precision. Undefined conditional rates display as a dash, never zero.
- The model-form panel changes information structure and calibrated noise parameters. The offer-grid panel keeps ten party-signal bins. The multiple-start panel describes 50 verified recoveries per fee rule and 21/11 distinct retained profiles; recovery frequency is not an equilibrium-selection probability. Repeated range endpoints do not prove uniqueness.
- The 5x5 pure-strategy enumeration and QRE project are excluded. Appendix-only model forms, cost sweeps, risk-averse fifteen-offer comparisons, and full recovery accounting remain in their source folders for later appendix assembly.

The four standalone PDFs have been rendered and checked, with numerical cells independently audited against their source records. Manuscript integration and the final submission-system PDF check remain to be done.
