# Revised article and exhibit plan: preserve the existing organization

September 25, 2026

## Governing approach

Revise the existing article in place conceptually: retain its section order, division between risk neutrality and risk aversion, numbered exhibit roles, and folder organization. Change content only where the revised model, new results or accurate interpretation requires it. A more compact exhibit scheme is not, by itself, a reason to restructure the article.

This plan supersedes the earlier proposal for five main figures, three main tables and ten separately numbered supplemental groups. Those working labels were a proposed redesign, not the article's established numbering. They should no longer guide placement. Previously generated figures and tables remain useful source/review artifacts; their existence does not require putting all of them in the manuscript or changing its order.

## Responses to the four concerns

1. **No separate computational methods and validation section or exhibit group.** Remove the proposed standalone S8. Implementation and validation belong primarily with the relevant code, tests and reproducible commands. Put necessary short explanatory notes in the existing analysis folder or its Sources/README; keep manifests, execution logs and audit records in the existing Results/Run records location and the isolated provenance archive. The exact-arithmetic verification evidence remains preserved. None of this creates a new reader-facing article section or folder.
2. **Keep Figures 1 and 2 separate.** The former F1 suggestion would have consolidated information structure and timing into a new summary. The current Figure 2 is specifically a worked equilibrium path, so that proposal also changed its purpose. There is no established reason to make either change.
3. **Keep Figures 3 and 4 separate, and likewise Figures 5 and 6.** The former F3 grouped participation, dispositions and agreement across risk settings. It overlapped with parts of four existing figures and did not provide the full signal-dependent offer content of Figures 4 and 6. It is a useful working overview, not a replacement for those distinct figures.
4. **Keep welfare and robustness in their current positions.** The former F2 placement suggested leading the results with the all-cost monetary overview. There is no demonstrated reason to move that material ahead of the existing behavioral explanation. Risk-neutral dispositions/strategies come first, then their risk-averse counterparts, then Welfare Analysis, followed by Robustness. The introduction can still summarize findings as it ordinarily does.

## Preserve the manuscript sequence

The current TeX source, not an assumed new outline, supplies this sequence:

- Introduction.
- The Model: Information structure; Litigation sequence and updating; Costs, preferences, and fee shifting rules; Parameter Values and Example Path; Outcome measures.
- Results: Risk Neutrality; Risk Aversion; Welfare Analysis.
- Robustness: Parameter Changes; Multiple Equilibria.
- Conclusion.

Keep existing labels, cross-references and placement anchors where possible. Preserve useful prose and explanations when they remain correct. Update numerical claims, model descriptions and conclusions that no longer match the new evidence; preserving structure does not mean retaining outdated scientific claims. No new top-level section is proposed.

## Agreed presentation corrections, September 25

- Preserve the original Latin Modern typography and restrained booktabs/TikZ style. Table names and explanatory captions remain outside the table files.
- Figure 2 follows a real American equilibrium history through entry, exit commitments, agreement, offers and trial, with a neighboring settlement history and zero-probability deviations. Preserve chance/player nodes and valid information-set links; do not imply observation of simultaneous actions.
- Figures 3 and 5 restore the original directional convention: white backgrounds for pro-defendant outcomes, black backgrounds for pro-plaintiff outcomes, gray for settlement, with the prior dot/line patterns distinguishing dispositions.
- Figures 4 and 6 superimpose American circles and British open diamonds on shared signal axes. Omit exactly unreached histories from the display; keep their full policies in Sources. RN reached commitments always continue, so omit redundant commitment panels. Preserve meaningful RA commitments. Show every positive-probability reached offer with a support marker, with marker area proportional to probability. No heatmaps or long bottom notes.
- Tables 2 and 3 omit flags and remainder columns; full reconciliation remains preserved in the detailed records. Figure 7 and the Table 5 row changes are as specified in the exhibit map below.
- Keep the supplemental folder structure. Avoid duplicating the old all-cost plot now that its revised form is Figure 7; keep its full-precision numerical records. Preserve utility curves, the manuscript, unrelated repository changes, and all underlying research artifacts.

## Existing numbered exhibits and necessary updates

The user approved one change of exhibit type: Figure 7 replaces Table 4 within Welfare Analysis. The set is now seven figures and five tables. Figures 1-6 and Tables 1-3, 5-6 retain their existing file identifiers and roles; no unrelated renumbering or article reorganization is introduced. The prepared collection is an isolated overlay, subject to the existing final release gates.

| Existing exhibit | Existing location | Treatment |
| --- | --- | --- |
| **Figure 1 - Information structure** | The Model / Information structure | Keep separate, in its existing position. Preserve the current design where accurate; update only information/prior/signal details affected by the revised specification. |
| **Figure 2 - Worked equilibrium path** | The Model / Parameter Values and Example Path | Keep separate from Figure 1. Refresh the worked example against a validated agreement-enabled profile; show commitment, agreement and conditional offers correctly. It remains an example path, not a generic timing panel. |
| **Figure 3 - Dispositions** | Results / Risk Neutrality | Keep a separate RN disposition figure. Use the new American/British cost-1 profiles, preserve population denominators, and do not count agreement refusal as an additional terminal disposition. |
| **Figure 4 - Participation and offers** | Results / Risk Neutrality | Keep the separate RN strategy figure. Preserve filing, answering and offer content; add the necessary agreement/commitment information and complete mixed-offer representation. Do not replace it with aggregate participation bars alone. |
| **Figure 5 - Risk-averse dispositions** | Results / Risk Aversion | Keep the separate RA disposition figure with the same role and ordering as now, using the new profiles. |
| **Figure 6 - Risk-averse participation and offers** | Results / Risk Aversion | Keep the separate RA strategy figure. Agreement and mixed strategies must be represented faithfully; do not combine it with Figure 5 or with the RN figures. |
| **Table 1 - Model primitives** | The Model / Parameter Values and Example Path | Retain the primitives table and its place. Update changed model values/fee triggers. Do not expand it into a computational validation catalog. |
| **Table 2 - Strategy mechanisms** | Results / Risk Neutrality | Retain a separate risk-neutral mechanism table. Use the reviewed American-to-British RN excerpt panel as its source; preserve contributions and necessary caveats. |
| **Table 3 - Risk-averse strategy changes** | Results / Risk Aversion | Retain a separate table for changes involving risk aversion. Use the reviewed American-to-British RA and RN-to-RA under each rule panels. Do not merge this into Table 2. |
| **Figure 7 - Welfare outcomes (replaces Table 4)** | Results / Welfare Analysis | Use the full 20-case American/British monetary-outcomes figure: risk-neutral and risk-averse panels, five cost multipliers as rows, five separate outcome measures as columns. Keep common scales within each column. This is the levels comparison, not the mechanical/behavioral decomposition. |
| **Table 5 - Overall results summary** | Robustness / Parameter Changes | Keep the RN and symmetric-RA panels. Immediately after earlier-costs and later-costs rows, put the corresponding cost-1 trial-only-versus-American row. Group calibrated direct binary with center-weighted and polarized merits near the end. Other rows compare British minus American. Asymmetric risk cases remain separate. Two grid rows remain Pending until validated imports arrive. |
| **Table 6 - Disposition ranges** | Robustness / Multiple Equilibria | Retain the range table and location, updated from the 200-start/199-accepted-profile study. Discuss monetary ranges here too, with the requested full outcome plot available in the existing multiple-equilibria materials. |

Adding agreement information may require extra panels within a strategy figure or an adjacent supplemental reference. Keep the disposition/strategy and RN/RA distinctions. Any change to numbering, merging or moving exhibits needs a specific scientific or space constraint; do not make it just to match the earlier working-artifact list.

## Decomposition excerpts: selected, but keep Tables 2 and 3 distinct

The 32-row, four-panel strategic packet has already passed numerical checks and visual review. It is a review/source packet, not one combined numbered Table 2. Its placement is:

| Existing table | Reviewed source panels | Selected rows |
| --- | --- | ---: |
| Table 2 - Strategy mechanisms | American to British, risk neutral | 8 |
| Table 3 - Risk-averse strategy changes | American to British, risk averse; risk neutral to risk averse under American; risk neutral to risk averse under British | 24 |

These rows follow the rule fixed before drafting claims: largest absolute coordinate change within each decision family among information sets with positive reach at both endpoints; exact ties retain existing information-set/action order. Zero-change winners remain eligible. Complete offer supports and full history identities remain in the source data. The detailed decomposition, reverse comparisons and diagnostic records remain in the existing Equilibrium strategy changes folder.

Tables 2 and 3 retain their separate scientific roles and positions and use the reviewed inputs. Remove the flags and selection-remainder columns from these main-table displays; retain complete reconciliation, unrounded values and sensitivity diagnostics in Sources and the full supplemental records. Do not claim the displayed components alone sum to the change when the omitted reconciliation is nonzero. The current 32 rows are the reproducible selection pool; fitting final manuscript tables should preserve the selected evidence and clearly reference any rows continued in the existing supplement, rather than silently choosing a new set that supports a preferred story. Do not describe omitted reconciliation terms as zero. Keep necessary qualifications in the separate captions and underlying diagnostics, without a flags column or a column labelled "Remain".

The monetary welfare decomposition is different from this strategic-response decomposition. Introduce its accounting and interpretation within the existing Welfare Analysis discussion. The all-cost Figure 7 now fills Table 4's monetary-outcome role. Keep the full mechanical/behavioral decomposition in its relevant reporting folder. Do not rename Table 3 as a robustness table, as the previous proposal implied.

## Where the new working artifacts belong

| Working artifact from the prior proposal | Role under the preserved organization |
| --- | --- |
| Combined model/timing proposal, former F1 | Withdraw as a consolidation. Refresh existing Figures 1 and 2 separately. |
| All-cost monetary overview, former F2 | Approved as Figure 7 replacing Table 4 in Welfare Analysis, using all 20 latest main profiles. It does not move to the beginning. |
| Combined participation/disposition overview, former F3 | Cross-check/source material for existing Figures 3-6. Prepare the separate final figures and restore full signal-dependent strategy/offer content where the overview lacks it. |
| Mechanical/behavioral welfare plot, former F4 | Welfare Analysis and the corresponding welfare decomposition materials. Main-text placement, if needed, is local to that existing discussion. |
| Multiple-start outcome plot, former F5 | Existing Multiple Equilibria subsection and folder, alongside the updated Table 6. No separate early-results section. |
| Combined strategic packet, former T2 | Reviewed source panels for separate existing Tables 2 and 3, as mapped above. |
| Proposed robustness table, former T3 | Input for updating existing Table 5 within Parameter Changes; not a renumbering of the strategy table. |

## Changes that do have a strong substantive reason

- Describe the agreement-enabled game accurately: commitments, simultaneous agreement, offers only following mutual agreement, and the existing outcomes after refusal. Update Figure 2, strategy figures and relevant model prose accordingly.
- Use American and British as the main comparison. Move trial-only fee shifting to its cost-1 extension discussion within Parameter Changes; preserve its other calculated profiles in the comprehensive record. Do not build a new top-level section for it.
- Replace old model results with the validated agreement-enabled profiles. All 20 main profiles are available; the two outstanding grids are extension cases. Preserve correct arguments but revise any numerical or qualitative claims contradicted by the new results.
- Preserve the five distinct monetary measures and population/conditional denominators. Reflect mixed policies and agreement behavior accurately; a mean offer cannot stand in for a complete mixed strategy.
- Update the existing Multiple Equilibria subsection to the actual 200 attempts and 199 accepted approximate profiles, including failures, ranges and grouping limitations. Recovery frequencies are not probabilities of real-world equilibrium selection.
- Update the extension matrix and comparison tables to the authorized narrower design. Keep the truth-map interpretation with the relevant welfare/decomposition analysis; alternative strengths remain unresolved, and this editorial correction does not authorize those jobs.

## Folder and documentation policy

Retain the existing article roots: Article and bibliography, Figures, Tables, Results and Supplemental materials. Use existing subject folders such as Equilibrium strategy changes, Multiple equilibria, Game tree diagrams, Liability signals diagrams and Equilibrium solution paths. Keep the previously required welfare outputs with their relevant welfare reporting material, rather than using them to justify another article section.

Reproducibility material stays with the code/tests, each subject's Sources or README, and Results/Run records as appropriate. Include only the definitions, units, selection criteria and limitations the reader needs in the manuscript or exhibit notes. No standalone Computational methods and validation section, numbered supplemental group, or new folder of that name is planned. The utility-curve materials remain unchanged.

## Remaining work under this corrected plan

1. Prepare and visually inspect the restored presentation for Figures 1-6 and the new Figure 7, retaining the article order.
2. Prepare Tables 1-3, 5-6 without titles embedded in the files. Retain separate captions. Apply the agreed Table 5 row order and trial-only placement. Figure 7 replaces Table 4.
3. Write and verify replacements only for affected paragraphs and claims. Keep the existing article sequence and retain unaffected content. Put necessary methodological explanation next to the relevant result/code.
4. Finish the outstanding scientific/reporting work: the two existing grid cases and dependent comparisons; the existing fourth trajectory and viewer QA; unresolved truth-map choices before dependent replays; remaining supplemental visual review, terminology consistency and complete inventory.
5. Stage the validated collection and proposed file-level changes before the established archive/replacement procedure. Preserve the current manuscript, numbered artifacts, unrelated repository edits and protected materials until that procedure applies.

Hourly checks remain disabled. This plan neither starts simulations nor changes their code/builds. It does not authorize an article reorganization, fresh searches, renumbering or a duplicate process.

## Status and provenance

The computation/reporting status remains the latest recorded status; no run was polled for this planning correction. Main profiles: 20/20; full primary catalog: 80/82; welfare pairs: 34/36; strategic directions: 182/190; multiple-start search: 200 completed attempts/199 accepted approximate profiles. The existing 32 strategic excerpts remain selected and reviewed. Final numbered layouts and article insertion are separate outstanding work.

The adjacent manifest binds the current manuscript outline, actual numbered exhibit registry/READMEs, prior plan and reviewed excerpt inputs. The article and code repositories were read only. Prior plans remain as provenance, but their F1-F5/T1-T3/S1-S10 restructuring proposal is superseded by this document.
