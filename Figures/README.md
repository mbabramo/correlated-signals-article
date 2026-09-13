# Revised publication figures

This is the sole directory for the revised manuscript's publication figures. The old PDFs and duplicate PNGs were removed after checkpoint commit `7e92fc01e1d7ff92bf0b07dbe80ac9ff021ce7b3`. The empty `Updated figures` folder is retired.

All four selected main-article figures are assembled in this directory. Filenames describe their content; manuscript numbering belongs in the manuscript, not the filenames. Each PDF has matching PNG, TeX, TXT, and JSON companions. Appendix-only figures and alternative renderings remain in their descriptive supplemental folders. Current generated research diagrams and their TeX sources are available in [Results](../Results/) and [Supplemental materials/Multiple equilibria](../Supplemental%20materials/Multiple%20equilibria/). Do not treat the old manuscript's now-missing figure references as current illustrations.

## Selected main-article figures and their sources

| Publication file | Content | Source and remaining work |
|---|---|---|
| [continuous-merits-and-party-signals.pdf](continuous-merits-and-party-signals.pdf) | Standalone continuous Q-to-party-signal diagram, black and white | Publication copy of the [generated source](<../Supplemental materials/Liability signals diagrams/Continuous merits - party - bw.pdf>). Truth/court counterparts are proposed Figures A1-A2; opponent-signal comparisons are Figures B1-B3. No combined signal figure is planned. |
| [worked-equilibrium-path.pdf](worked-equilibrium-path.pdf) | Approved full-game worked equilibrium path and selected adjacent histories | Publication copy of the [generated source](<../Supplemental materials/Game tree diagrams/worked equilibrium path.pdf>); numerical extraction and C# layout exist. Final manuscript-size review remains. Table A3 will supply additional action-value comparisons. |
| [participation-and-offers.pdf](participation-and-offers.pdf) | Four compact panels: filing, answering, P offers, D offers; both fee regimes | Assembled from baseline cost-1 action CSVs. Actual mixed filing/answering probabilities and pure on-path offers; off-path offer regions are left blank, without labels or markers. |
| [disposition.pdf](disposition.pdf) | Baseline, higher costs (2x), moderate risk aversion, lower noise, and lower noise plus moderate risk aversion | Assembled from ten CS004 All/Only Eq rows, ten offers; cost 1 except the higher-cost pair at cost 2. Compares proposed explanations for higher settlement with the actual routes away from trial. Seven mutually exclusive categories, all potential disputes denominator; saved abandonment/default already include mutual-give-up allocation. |

The main selection remains **four figures and four tables**. The new party-to-party
diagrams belong in Appendix B, with a main-text pointer explaining the role of shared
merits; they do not replace Figure 1 or add a fifth main figure.

The shared disposition palette uses black for plaintiff trial wins, white for defendant
trial wins, and middle gray for settlement. Defendant default is black with white diagonal
lines; plaintiff abandonment is white with black diagonal lines. Nonfiling uses small black
dots on white; nonanswering uses small white dots on black. Bars and legend share the
same styles, which should also be used for proposed Figure C1. These patterns classify
procedural outcomes, not true liability or outcome fidelity.

Lower costs are omitted from the main disposition figure; the full cost sweep remains
planned as Figure C1. Participation restrictions are separate extension files, not main
Figure 4 scenarios: [mandatory entry](<../Supplemental materials/Participation restrictions/mandatory-entry-dispositions.pdf>)
and [mandatory entry without later exit](<../Supplemental materials/Participation restrictions/mandatory-entry-no-exit-dispositions.pdf>).
Each file compares its restriction with baseline under both fee regimes at cost 1.

## Main tables

The four main tables are now assembled in [Tables](../Tables/), with descriptive PDF filenames, editable TeX fragments, previews, captions and source-data JSON. The numbers below remain proposed manuscript order, not filename prefixes. See [Tables/README.md](../Tables/README.md) for links, regeneration, and denominator checks.

| Table | Scope | Detailed online support |
|---|---|---|
| 1 | Essential primitives, legal interpretation, and numerical values | A1 full parameters; A2 information, timing, and accounting |
| 2 | Cost-1 American/British baseline: participation/selection, bargaining, dispositions, and net outcomes | A3 action values; C1 full cost results; E1 denominator/units dictionary |
| 3 | Higher costs, moderate risk aversion, lower noise, and lower noise plus moderate risk aversion relative to the appropriate cost-1 baseline: three monetary perspectives, fidelity loss, expenditures | Matches main Figure 4's contrasts; B3 and C1-C2 give broader levels/comparative results |
| 4 | Compact model-form, 10/15-offer, and multiple-start sensitivity panels | B3 model-form outcomes; D1-D3 recovery, dispersion, and grid comparisons |

Keep raw means and conditional quantities distinct. The three conditional monetary
perspectives must accompany Net Outcome Fidelity Loss; do not substitute the old
two-component accuracy/expenditure charts for the new table.

## Proposed online appendix exhibits

The recommended core set is **six figures and fourteen tables**; optional assets
and color/B&W alternatives do not add to those counts. Most numerical source data
exist, but these publication tables and appendix manuscripts still need assembly.
See the [supplemental exhibit map](<../Supplemental materials/README.md>) for named
exhibits, sources, optional additions, and the distinction between appendices and downloads.

| Appendix | Core figures | Core tables |
|---|---|---|
| A. Model and computation | A1 Q-to-truth; A2 Q-to-court | A1 parameters; A2 information/timing/accounting; A3 selected action values; A4 numerical verification |
| B. Information structures | B1-B3 party-to-party predictions under continuous merits, truth-conditioned merits, and direct binary signals, as separate PDFs | B1 architecture/calibration; B2 conditional opponent probabilities; B3 model-form results |
| C. Parameters and participation | C1 baseline dispositions across five costs and both fee rules; needs new assembly from saved data | C1 cost/noise/risk results; C2 cost timing and participation restrictions |
| D. Equilibria and discretization | None required | D1 recovery accounting; D2 dispersion; D3 baseline and risk-aversion 10/15-offer comparisons |
| E. Reproducibility | None required | E1 data dictionary; E2 exhibit-to-source/regeneration index |

Figures A1-A2 and B1-B3 already have source PDFs. Optional extra trees, forward/inverse
signal illustrations, a CARA plot, or an equilibrium-demand plot should be included
only if they add an explanation. Keep the full automatic chart collection as indexed
downloads, not hundreds of numbered appendix figures. Main-article copies use descriptive
filenames; the original supplemental source assets are preserved.

Baseline source stems, relative to `Results/Individual simulations`:

- `CS004 Specification-Baseline__Cost-1__Fee-American`
- `CS004 Specification-Baseline__Cost-1__Fee-British`

Append ` -fileans.pdf`, ` -offers.pdf`, or ` -InformationSetActions.csv`. Matching diagram sources end in `.tex`. Preserve exact CSV probabilities when preparing new plots; the PDF labels are rounded.

Current aggregate disposition comparisons are under `Results/Aggregated Data/<specification>/Risk Neutral/Single Row`. This grouping directory name does not override each panel's risk-aversion specification.

The three-perspective monetary-outcome presentation belongs in the planned main table and, if useful, a supplemental plot. The existing aggregate `Accuracy and Expenditures` charts show only two ex ante monetary measures plus expenditures; the additional required columns are already in `CS004 numerical results.csv`.

Keep each final figure's source script/TeX and source-row mapping alongside the PDF. Replacing manuscript figure references remains part of the article revision.

The September 11 collection contains the four selected main figures, not an
unfiltered copy of generated diagrams. Information and worked-path publication
copies are now included alongside the participation/offer and disposition figures.
The manuscript references and submission proof have not yet been updated.

Every signal relationship is generated independently in color and grayscale.
Combining signal diagrams later would be a separate layout decision. Damages
are not part of the article's figure selection. Use tables for the three
truth-conditioned monetary perspectives, Net Outcome Fidelity Loss and real
expenditures; do not add a fifth dense chart simply because it is available.

## Regeneration and verification

The command below regenerates `participation-and-offers` and `disposition`
directly under their descriptive names (and the separately configured participation
extensions). For the information figure, regenerate the `signals` target and copy the
five `Continuous merits - party - bw` companions to `continuous-merits-and-party-signals`
here. For the path figure, regenerate `worked-path` and copy its PDF/PNG/TeX/TXT here
as `worked-equilibrium-path`; copy the extraction `worked equilibrium paths.json` as
`worked-equilibrium-path.json`. The editable request remains at
`../Supplemental materials/Game tree diagrams/worked equilibrium paths.request.json`.
When refreshing the path TXT copy, update its extraction/request references to these
publication locations. The copied diagrams and numerical JSON are otherwise unchanged.

From ACESim4, run:

```text
dotnet run --project LitigCharts -c Release -- diagrams publication --config "C:/Users/Admin/source/repos/correlated-signals-article/article-diagrams.json"
```

The request is `../publication-figures.json`. The reusable renderer and validation
are in `LitigCharts/PublicationFigures.cs`, within the existing C# project. The configuration's
`AdditionalDispositionFigures` also regenerates both separate participation-restriction
files from their own requests. No
settings edits or equilibrium reruns are required. Each figure has matching
TeX, PNG, caption `.txt`, and source-data `.json`; explanations stay outside the
figure. Request/source hashes and exact row identifiers are retained in JSON.

The two PDFs were visually checked as standalone files and included at 16 cm
width in a local manuscript-size test. Fonts are embedded, both PDFs are single
page with no raster images, and PNGs are strictly grayscale. The updated workflow
passes 44 targeted regression tests, including eight publication-figure tests.
Inspect the actual journal submission proof after packaging.

The subsequent five-scenario disposition update and its two separate participation
files were checked as single-page, strictly grayscale vector PDFs with embedded
fonts. All 18 displayed bars reconcile, exact request/source hashes match, and
53 targeted tests pass. This standalone check does not replace manuscript-size
and submission-proof review of the newly selected figure.
