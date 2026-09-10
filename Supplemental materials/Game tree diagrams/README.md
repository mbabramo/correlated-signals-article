# Game-tree illustrations

These six diagrams are generated from the revised continuous-merits baseline in
ACESim4, using two signal bins per party, two court outcomes, and two offer values.
They illustrate the extensive form; they are not solved equilibria or the
ten-signal, ten-/fifteen-offer production results.

## Model and interpretation

- Q is uniform on [0, 1], and true liability conditional on Q is Bernoulli(Q).
  Q is integrated with the baseline's 64-point Gauss-Legendre quadrature.
  The quadrature points are not game-tree states.
- Both party signal standard deviations and the court standard deviation are 0.2.
  Party signal bins and offers are represented by 0.25 and 0.75; the court has
  two findings (not liable / liable). A court finding is not true liability.
- Both initial wealth levels are 10. Damages are 1. Each party's total
  litigation cost is 0.30: 0.15 before bargaining and 0.15 at trial.
  There is no fee shifting and both parties are risk neutral.
- Filing and answering remain endogenous. Exit commitments are simultaneous,
  as are offers: the drawn order does not imply observation. Repeated P/D
  node numbers identify the same information set, including across signal branches.
  A Yes exit commitment operates only if the offers do not settle.
- Chance probabilities are rounded to three decimal places, payoffs to four.
  No behavioral probabilities are displayed: the initializer's arbitrary
  strategy is not presented as an equilibrium.
- Payoff pairs are (plaintiff final wealth, defendant final wealth).
  Simplified leaves give expected wealth, not a realized monetary allocation.
  These pairs are not the article's net-outcome-fidelity measure.

## The six views

- game tree 2x2x2.pdf: all actions, with court and mutual-exit lotteries explicit.
- game tree 2x2x2 simplified.pdf: the same game with terminal lotteries integrated out.
- The two beginning PDFs stop after private signals, at the filing information sets.
  They are deliberately identical: continuous merits are integrated out in both
  versions, so the obsolete finite case-strength layer is not reinstated.
- The two end PDFs show the first bargaining subtree: both signals are 0.25,
  and the plaintiff has filed and the defendant has answered.
- The legacy 2x2x2 filenames are retained to avoid unnecessary link changes.
  They do not mean that continuous merits now has two discrete states.

## Regeneration

In ACESim4, run scripts/Generate-ArticleGameTrees.ps1 -OutputDirectory <this folder>.
This invokes the existing C# tree walker and TikZ generator, compiles all six
LaTeX sources with LuaLaTeX, and refreshes the two existing PNG previews.
Explanatory prose is in a matching .txt file for each diagram, not inside the PDF.
Only node/branch labels, probabilities, and payoff pairs appear in the diagrams.
No production settings, equilibrium files, or production results are modified.
The .tex sources are retained here so the figures can also be compiled directly.

Generated from ACESim4 commit 2fa3798809ee5c152e66b4f69b1eee190c88ada0 (clean source).
