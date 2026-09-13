# Decomposition after equilibrium-preserving mixing

The four ordinary-cost equilibria were explored separately, then the four
fee-rule/preference interventions were recalculated using the selected mixed
profiles. These are research diagnostics. The saved production equilibria,
original solution-path animations, and existing paper tables are unchanged.

## What the exercise establishes

Mixing alone does **not** simplify the comparison. It broadens some offers but
adds differences in their probability distributions: the number of changed,
commonly reached information sets rises from 59 to 70. These are information
sets across four contrasts, not unique sets across the whole game.

A more useful restriction is to focus on previously used actions that cease to
be optimal against the target opponent, even after reoptimizing the player's
subsequent decisions. This is stronger than asking whether the two supports
overlap: disjoint supports can still consist of tied actions, while overlapping
supports can contain important losses of optimality. The rule is explicit and
can also be applied to the original profiles without any mixing.

| Intervention | Original changed sets | Mixed changed sets | Focused mixed sets | Focused in original and both mixed variants |
|---|---:|---:|---:|---:|
| American to British; risk neutral | 4 | 9 | 2 | 2 |
| American to British; moderate risk aversion | 22 | 22 | 11 | 11 |
| Risk neutral to moderately risk averse; American | 20 | 22 | 22 | 20 |
| Risk neutral to moderately risk averse; British | 13 | 17 | 7 | 6 |
| Total | 59 | 70 | 42 | 39 |

The selected-profile focus has no Remaining greater than 0.0001 percentage
points. That is not evidence that the full equilibrium change has been explained:
28 other changed sets remain in the audit, and 54 histories across the contrasts
change reach and cannot be compared as two reached endpoint decisions. Tie and
off-path-completion sensitivities also remain in some focused allocations.

The 39-set intersection is stable only across the tested representations. It is
not a characterization of all equilibria or all possible equilibrium-preserving
mixtures, and its component allocations need not be stable.

## Substantive examples

- Under risk neutrality, the focused fee-rule comparison retains increased
  filing at P signal 0.25 (87.83% to 100%) and the move to a 0.05 demand at
  P signal 0.35. Both are direct effects in this diagnostic accounting. Differences
  among high-signal aggressive demands remain outside the focus because the
  actions stay tied against the target opponent.
- With moderate risk aversion, moving American to British still attributes the
  disappearance of filing at P signals 0.05, 0.15 and 0.25, and answering at
  D signals 0.85 and 0.95, to replacement of opponent offers under the direct-first
  accounting convention. This pattern appears in both tested mixed variants.
  Some of these allocations retain off-path-completion sensitivity flags.
- More detailed exit attributions are less secure. For P abandonment at signal
  0.45 in the risk-averse fee-rule comparison, the selected-profile accounting is
  100 percentage points from opponent offers; the forward/tighter variant splits
  that as 50 from offers and 50 from exit. The underlying abandonment change is
  unchanged. Equilibrium-preserving mixing therefore does not identify one
  unique explanation for every strategy change.

Recommended paper use: a compact table of clearly stated strategy changes,
preferably emphasizing the 39-set intersection, with sensitivity flags and the
other changes retained online. Do not describe excluded tied-action changes as
unimportant; their probabilities can discipline the opponent and sustain the
equilibrium. The current publication tables have not been replaced.

## Reports

- [Selected-profile focused comparison](Focused%20strategy%20changes.md): one row
  per information set, full focused endpoint distributions, and an audit of the
  other changed sets. The decomposed quantity is probability assigned to the
  actions gaining probability, not a mean offer.
- [Forward-order, tighter-tolerance comparison](Forward-order%20tighter%20check/Focused%20strategy%20changes.md):
  the same four contrasts, using the forward search at the tighter tolerance.
- [Mixing reports](../Equilibrium%20mixing%20exploration/README.md): both orders,
  full strategies, equilibrium checks, and outcome comparisons for all four cases.
- Each directory retains the complete eight-coalition calculations, semantic
  profiles, action utilities, source/override fingerprints, and calculation
  manifest. The compact JSON also retains fixed-target-continuation losses,
  optimized-continuation losses, support comparisons and all omitted histories.

## Numerical and search limitations

The main search permits maximum unrestricted unilateral root gain of 1e-9
reported utility units; all selected profiles achieve less than 2.6e-10. The
tenfold tighter rerun permits 1e-10 and achieves less than 2.6e-11 in both orders.
These are absolute utility units, not percentages of damages.

The mixing objective changes from 0.014632 to 0.115654 for risk-neutral American,
0 to 0.086896 for risk-neutral British, and remains 0 for risk-averse American.
Risk-averse British rises from 0.039877 to 0.084163 in forward order and 0.106854
in the selected reverse order. The reverse run reaches its six-sweep cap with
small continuing improvements; it has NOT certified a local optimum. Both
orders pass equilibrium checks, but their strategies differ materially.

Tightening numerical tolerances changes same-order action probabilities by at
most 1.90e-8 (risk-neutral American), 1.12e-8 (risk-neutral British), zero
(risk-averse American), and 3.20e-6 forward / 2.46e-4 reverse (risk-averse British).
The reverse British search remains sweep-limited at the tighter tolerance.
The forward/tighter decomposition retains 44 focused sets rather than 42,
adding P abandonment at signal 0.35 in both comparisons involving risk-averse
British. One of its focused rows still has Remaining: the focus criterion is not
designed to force residuals to zero.

Aggregate dispositions are unchanged up to floating-point noise in the first
three cases. For risk-averse British the largest difference across either main
search order is 2.13e-8 in unconditional probability (0.00000213 percentage
points). No source-unvisited policy changed. These outcome checks do not assert
that every distribution of settlement transfers is identical.

## Reproduction and preservation

From the ACESim4 repository, use the existing `equilibrium-mixing`,
`equilibrium-changes --calculate-only`, and `equilibrium-change-focus` C# commands.
The article request files are `equilibrium-mixing.request.json`,
`equilibrium-mixing-tight.request.json`, `equilibrium-changes-mixed.request.json`
and `equilibrium-changes-mixed-forward.request.json`. The latter is a combined
forward-order/tighter-tolerance sensitivity check, not an independent new solve.

The focused report uses a conditional utility threshold of 1e-6 and probability
threshold of 1e-6. Complete deviation tests, semantic-profile validation and
focus/accounting regression tests pass (39 tests). SHA-256 checks confirm all
99 pre-existing files in Equilibrium derivations, Equilibrium changes and Tables
remain byte-for-byte unchanged.
