# Supplemental materials: revision status

## Current numerical robustness output

[Multiple equilibria](Multiple%20equilibria/) replaces the old `Robustness checks` folder. Its README describes the current multiple-start design, recovery catalogs, outcome/range tables, and diagnostic figures. The fixed-signal ten-versus-fifteen comparisons are integrated into [Results](../Results/).

## Explanatory assets

The following folders contain explanatory assets for the appendix revision. Their intended roles are:

- `Game tree diagrams`: five current reduced-grid structural views, plus the separate worked path from a saved full-sized equilibrium. Each has TeX, PDF, PNG, and explanatory text; the worked path also has its request and extracted numerical JSON. The duplicate simplified beginning is no longer generated. Structural views show chance probabilities, not equilibrium behavior; the worked path does show information-set-specific equilibrium action probabilities and utilities.
- `Liability signals diagrams`: 28 current standalone PDFs with matching color/B&W versions, PNG/TeX/TXT/JSON companions: eight forward relationships, three inverse relationships, and three party-to-party relationships. Both palettes highlight a reference fan by fill alone; no ribbon borders are used. The older `Truth-conditioned merits - party signals.pdf` is a historical packaging reference, not a current publication candidate.
- `Risk aversion`: `risk aversion v2.tex` contains a reusable CARA plotting source. Its moderate curve uses alpha 2, matching the current moderate-risk-aversion cases. A revised appendix may show only risk neutrality and that curve.
- `Information set pressure analysis`: the historical log from the older model, retained for methodological reference; do not confuse it with the new calculation below.
- [Information-set pressure](<Information-set pressure/README.md>): the current production-model analysis, with eight intervention PDFs, action utilities, reach/posterior data, tie/completion sensitivity, and validation records. This replaces the historical analysis for the revision.

## Planned appendix exhibits

The main article retains four figures and four tables. The recommended online core
is **six figures and fifteen tables**, listed below. These are proposed exhibit
numbers, not existing appendix manuscripts. Color and B&W are versions of the same
exhibit. Core means recommended for submission; optional means include only for a
specific explanatory need; archive-only means retain as a linked download without
inserting it as a numbered figure. No deletion or reorganization is implied.

### A. Model details and computation

| Exhibit | Proposed content | Status/source |
|---|---|---|
| Figure A1 | Continuous merits to true liability | [Existing PDF](<Liability signals diagrams/Continuous merits - truth - bw.pdf>) |
| Figure A2 | Continuous merits to court finding | [Existing PDF](<Liability signals diagrams/Continuous merits - court - bw.pdf>) |
| Table A1 | Complete primitives and parameter grid | Assemble from production options/manifests; distinguish signal/offer actions from Q display bins and quadrature nodes |
| Table A2 | Observed information, simultaneous decisions, cost/fee timing, accounting conventions and outcome denominators | Assemble from current model/report definitions; optionally add a numerical post-filing/answering belief example |
| Table A3 | Selected filing, answering and P/D offer action values at relevant and adjacent information sets | Select existing action reports and worked-path data; show reach, action probability, conditional utility, and action loss |
| Table A4 | Finite representation, quadrature/rounding, verification tolerances/residuals and accounting checks | Summarize actual tests/run records; distinguish configured tolerances from measured checks |

An optional Figure A3 may use the [small bargaining/exit subtree](<Game tree diagrams/game tree 2x2x2 end.pdf>)
if it clarifies the protocol beyond main Figure 2. Keep all five structural views
downloadable through Appendix E; do not require five numbered tree figures.

### B. Alternative information and quality specifications

| Exhibit | Proposed content | Status/source |
|---|---|---|
| Figure B1 | Party-to-party prediction: continuous merits | [Existing PDF](<Liability signals diagrams/Continuous merits - party to party - bw.pdf>) |
| Figure B2 | Party-to-party prediction: truth -> discrete merits -> signals | [Existing PDF](<Liability signals diagrams/Truth-conditioned merits - party to party - bw.pdf>) |
| Figure B3 | Party-to-party prediction: direct truth -> signals | [Existing PDF](<Liability signals diagrams/Direct binary signals - party to party - bw.pdf>) |
| Table B1 | Architecture/calibration: baseline, direct binary, truth-conditioned merits, center-weighted Q, polarized Q | Assemble from production settings and signal companions; party noise is not identical across all models |
| Table B2 | Ten conditional opponent-bin probabilities given own bin 0.45, plus unconditional/conditional middle-range mass | Assemble from the matching party-to-party TXT/JSON files |
| Table B3 | Full model-form outcomes at all five costs and both fees | 40 alternative-information/Q ten-offer cases, plus clearly labeled baseline reference rows; split lifecycle/bargaining and monetary/expenditure panels |

Keep B1-B3 as three separate figures with the same reference signal and sizing.
They show pre-selection predictions, not beliefs after filing or answering. The
middle-range probability rises from 21.5% to 27.8% in the baseline and from 20.1%
to 26.7% in the truth-conditioned model, but remains 16.7% in direct binary. Explain
the symmetric conditional-independence restriction without claiming that binary
truth itself rules out close beliefs or correlated evidence.

Optional: the truth-to-discrete-merits and direct-truth-to-party forward diagrams,
if the architecture table is insufficient. The inverse diagrams, extra court
diagrams, and unused density/noise illustrations are archive-only by default.

### C. Additional parameter and participation checks

The two [participation-restriction comparisons](<Participation restrictions/README.md>)
are assembled as separate standalone files: mandatory entry and mandatory entry
without later exit. Each includes baseline at cost 1 under both fee regimes. They
are supplementary illustration candidates alongside Table C2, not main Figure 4
scenarios or additions to the six-figure online core count.

| Exhibit | Proposed content | Status/source |
|---|---|---|
| Figure C1 | Baseline dispositions over costs 0.25, 0.5, 1, 2, 4 under both fees | Needs publication assembly: ten bars using main Figure 4's seven categories and all-potential-disputes denominator; saved numerical inputs exist |
| Table C1 | Baseline, low/high noise, moderate risk aversion, low noise plus moderate risk aversion across costs/fees | Assemble 50 ten-offer cases from saved reports; include conditional settlement, the three monetary perspectives, fidelity loss and expenditures in readable panels |
| Table C2 | All costs avoidable/sunk, mandatory entry, and mandatory entry with no later exit | Assemble 40 ten-offer cases across all costs/fees, with labeled baseline comparisons |
| Table C3 | Information-set pressure: direct full best responses, two-step dynamics, and actual-equilibrium opponent-component substitutions | [Completed tables and data](<Information-set pressure/README.md>); eight matched fee/risk contrasts at costs 1 and 4. Select compact manuscript panels from the complete four-page-per-contrast tables |

Together B3, C1, and C2 cover the 130 distinct ten-offer cases; D3 adds the four
fifteen-offer cases. Baseline comparison rows may repeat without representing new
simulations. Optional: a reviewed risk-neutral/CARA-alpha-2 curve or one mechanism
plot; neither the legacy utility source nor all cost-breakdown charts are required.
Table C3 is now a core mechanism exhibit; its calculation and standalone tables are
complete. Appendix integration and selection of the most informative rows remain.

### D. Equilibrium and discretization robustness

No core figure is necessary.

| Exhibit | Proposed content | Status/source |
|---|---|---|
| Table D1 | Starts/priors, inexact/exact solve attempts, verified recoveries, duplicates, distinct profiles | Assemble from [Multiple equilibria](<Multiple equilibria/README.md>) recovery catalogs and manifest |
| Table D2 | Ranges, SD/CV where defined, strategy dispersion and verification residuals across distinct profiles | Assemble existing equilibrium ranges/outcomes files; displayed invariance is not a uniqueness proof |
| Table D3 | Matched 10/15-offer comparisons and within-grid British-minus-American contrasts, with baseline and risk-aversion panels | Assemble saved Results rows; keep signals fixed and explain the non-nested grids |

A plaintiff-demand-by-equilibrium dot plot is optional if it adds to D2. Recovery
frequency is not a behavioral selection probability. Keep the 216 existing ME
research PDFs as indexed downloads, not 216 numbered appendix figures.

### E. Complete results and reproducibility

No core figure is necessary.

| Exhibit | Proposed content | Status/source |
|---|---|---|
| Table E1 | Complete column/units/denominator dictionary, including truth filters, missing/off-path values and utility versus monetary measures | Assemble from report definitions; distinguish action mixing, probability-flow mass and recovery shares |
| Table E2 | Exhibit-to-source/regeneration index | Exact filenames, specification/fee/cost/grid, equilibrium/info set or filter, selected rows, request/generator, source states and hashes; link detailed mappings |

Link all research diagrams, raw equilibria/action reports and the [run documentation](<../Results/Run documentation/README.md>).
Do not rewrite historical manifests to describe newly regenerated files. Current
illustrations must record their actual newer generator source state, including
uncommitted work until committed. Damages/endogenous-disputes illustrations remain
outside this article's submitted set. Publication table formatting, Appendix C's
cost figure, full appendix manuscripts, and actual-size/submission-proof review
remain to be done; the existence of source files is not completed assembly.

## Current mechanism analysis

Use a few current information-set/action reports to explain final-equilibrium filing, answering, and offer choices. Report reach, the selected and alternative actions, conditional utility differences, and any mixing. Do not interpret conditional utilities at off-path information sets.

The [new pressure analysis](<Information-set pressure/README.md>) computes full best responses after a fee or symmetric-risk-aversion intervention, first holding the opponent's original strategy fixed. It then substitutes the opponent's participation, offers, exit, or all three, separately using first-round best responses and actual target-equilibrium strategies. The same four contrasts run at ordinary and fourfold costs. All focal continuation decisions are optimized; this is not subtraction of final-equilibrium CSV values.

The completed run contains 340 response/sensitivity calculations plus 16 original-equilibrium controls. All 3,840 source action rows were validated; the 33 targeted tests passed. No saved equilibrium or historical production manifest was changed. Counterfactual action values and beliefs are distinguished from undefined actual conditional utilities at unreached histories. Stars mark exposure to donor-unvisited opponent policies; daggers mark near-tied action values. Consult the sensitivity reports before assigning a mechanism to a component.

Choose one or two participation thresholds and one offer threshold if they explain the findings clearly. These strategy adjustments are diagnostic constructions, not evidence of actual learning, unique equilibrium selection, or additive causal shares. Most detail belongs in the supplement; a compact worked example can appear in the article. See [initial interpretation notes](<Information-set pressure/interpretation-notes.md>).
