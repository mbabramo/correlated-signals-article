"""Apply the user's agreed local exhibit corrections to the preserved plan."""
import pathlib, shutil
from article_release import ROOT, read, identity, save_new, utc

TASK=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to')
old=TASK/'outputs/Article-preservation-plan-20260925/Revised article and exhibit plan.md'
out=TASK/'outputs/Article-preservation-plan-20260925-v2';out.mkdir(exist_ok=False)
text=old.read_text(encoding='utf-8')
replacements={
'Retain the current six figures and six tables as the default manuscript set. The table below is a content-update map, not authorization to overwrite existing files.':
'The user approved one change of exhibit type: Figure 7 replaces Table 4 within Welfare Analysis. The set is now seven figures and five tables. Figures 1-6 and Tables 1-3, 5-6 retain their existing file identifiers and roles; no unrelated renumbering or article reorganization is introduced. The prepared collection is an isolated overlay, subject to the existing final release gates.',
'| **Table 4 - Welfare outcomes** | Results / Welfare Analysis | Update the existing five-measure welfare table in place from the four core profiles. Explain the mechanical/behavioral decomposition here, using the new welfare material where needed. |':
'| **Figure 7 - Welfare outcomes (replaces Table 4)** | Results / Welfare Analysis | Use the full 20-case American/British monetary-outcomes figure: risk-neutral and risk-averse panels, five cost multipliers as rows, five separate outcome measures as columns. Keep common scales within each column. This is the levels comparison, not the mechanical/behavioral decomposition. |',
'| **Table 5 - Overall results summary** | Robustness / Parameter Changes | Retain the comparative-summary role and location. Update to the revised case matrix. Report signed differences for the selected extensions, with full detail in Results; obsolete counts over the old 276-case design cannot be reused. |':
'| **Table 5 - Overall results summary** | Robustness / Parameter Changes | Keep the RN and symmetric-RA panels. Immediately after earlier-costs and later-costs rows, put the corresponding cost-1 trial-only-versus-American row. Group calibrated direct binary with center-weighted and polarized merits near the end. Other rows compare British minus American. Asymmetric risk cases remain separate. Two grid rows remain Pending until validated imports arrive. |',
'The separate Table 2/Table 3 publication layouts still need to be prepared from these reviewed inputs. Their existing scientific roles and positions are retained.':
'Tables 2 and 3 retain their separate scientific roles and positions and use the reviewed inputs. Remove the flags and selection-remainder columns from these main-table displays; retain complete reconciliation, unrounded values and sensitivity diagnostics in Sources and the full supplemental records. Do not claim the displayed components alone sum to the change when the omitted reconciliation is nonzero.',
'The old captions\' assertions that remaining contributions are zero must be updated wherever the new rows have a selection remainder. Necessary tie/off-path qualifications can be concise table notes linked to the full diagnostics.':
'Do not describe omitted reconciliation terms as zero. Keep necessary qualifications in the separate captions and underlying diagnostics, without a flags column or a column labelled "Remain".',
'Preserve Table 4\'s monetary-outcome role; use an adjacent compact illustration only if needed to explain a result, and keep the full decomposition in its relevant reporting folder.':
'The all-cost Figure 7 now fills Table 4\'s monetary-outcome role. Keep the full mechanical/behavioral decomposition in its relevant reporting folder.',
'Evidence for Welfare Analysis and the cost discussion in Parameter Changes; retain the full plot with the welfare/Results material. It does not move to the beginning or automatically replace a numbered figure.':
'Approved as Figure 7 replacing Table 4 in Welfare Analysis, using all 20 latest main profiles. It does not move to the beginning.',
'1. Prepare separate agreement-enabled updates for Figures 1-6, retaining their roles and the existing order. The combined working overviews are not yet those final numbered artifacts.':
'1. Prepare and visually inspect the restored presentation for Figures 1-6 and the new Figure 7, retaining the article order.',
'2. Prepare separate layouts for Tables 2 and 3 from the already reviewed excerpts; update their captions and local explanatory prose. Update Table 1\'s primitives, Table 4\'s welfare values, Table 5\'s revised comparisons and Table 6\'s new ranges in their existing roles.':
'2. Prepare Tables 1-3, 5-6 without titles embedded in the files. Retain separate captions. Apply the agreed Table 5 row order and trial-only placement. Figure 7 replaces Table 4.',
}
for before,after in replacements.items():
    assert before in text,before
    text=text.replace(before,after)
section='''## Agreed presentation corrections, September 25

- Preserve the original Latin Modern typography and restrained booktabs/TikZ style. Table names and explanatory captions remain outside the table files.
- Figure 2 follows a real American equilibrium history through entry, exit commitments, agreement, offers and trial, with a neighboring settlement history and zero-probability deviations. Preserve chance/player nodes and valid information-set links; do not imply observation of simultaneous actions.
- Figures 3 and 5 restore the original directional convention: white backgrounds for pro-defendant outcomes, black backgrounds for pro-plaintiff outcomes, gray for settlement, with the prior dot/line patterns distinguishing dispositions.
- Figures 4 and 6 superimpose American circles and British open diamonds on shared signal axes. Omit exactly unreached histories from the display; keep their full policies in Sources. RN reached commitments always continue, so omit redundant commitment panels. Preserve meaningful RA commitments. Show every positive-probability reached offer with a support marker, with marker area proportional to probability. No heatmaps or long bottom notes.
- Tables 2 and 3 omit flags and remainder columns; full reconciliation remains preserved in the detailed records. Figure 7 and the Table 5 row changes are as specified in the exhibit map below.
- Keep the supplemental folder structure. Avoid duplicating the old all-cost plot now that its revised form is Figure 7; keep its full-precision numerical records. Preserve utility curves, the manuscript, unrelated repository changes, and all underlying research artifacts.

'''
text=text.replace('## Existing numbered exhibits and necessary updates',section+'## Existing numbered exhibits and necessary updates')
(out/old.name).write_text(text,encoding='utf-8')
frozen=ROOT/'planning/updates/article-preservation-plan-20260925-v2';frozen.mkdir(exist_ok=False)
shutil.copy2(out/old.name,frozen/old.name)
snapshot=read(ROOT/'imports/remaining-primary-completion-v29/snapshot.json')
prior=read(ROOT/'imports/remaining-primary-completion-v28/snapshot.json')
before={t['PlanLabel']:t for t in prior['Tasks']};after={t['PlanLabel']:t for t in snapshot['Tasks']}
assert before.keys()==after.keys()
assert all(not t['Complete'] or after[k]['Complete'] for k,t in before.items())
pending=[t['PlanLabel'] for t in snapshot['Tasks'] if not t['Complete'] and not t['Failed']]
assert len(pending)==2 and not any(t['Failed'] for t in snapshot['Tasks'])
save_new(ROOT/'validation/remaining-profile-check-v29.json',dict(Passed=True,CheckedUtc=snapshot['CheckedUtc'],
    Snapshot=identity(ROOT/'imports/remaining-primary-completion-v29/snapshot.json'),Completed=34,Pending=pending,Failed=0,
    PriorCompletedTasksPreserved=True,SolvesStarted=0,UserRequested=True,MonitoringRemainsPaused=True))
save_new(ROOT/'provenance/current-editorial-plan-20260925-presentation.json',dict(CreatedUtc=utc(),
    Plan=identity(frozen/old.name),Delivered=identity(out/old.name),Previous=identity(old),
    Figure7ReplacesTable4=True,ManuscriptAndUserRepositoriesModified=False))
save_new(out/'manifest.json',dict(CreatedUtc=utc(),Plan=identity(out/old.name),FrozenPlan=identity(frozen/old.name),
    Snapshot=identity(ROOT/'validation/remaining-profile-check-v29.json')))
print('Plan updated; current snapshot confirms 34 complete, 2 pending, 0 failed.')
