# Original ECTA equilibrium derivations

These are independent replays of the original ordinary-cost American/British
equilibria under risk neutrality/moderate risk aversion. Each starts from the
original exact seed-zero uniform prior, under fixed rules throughout. They are
not transitions between equilibria or behavioral learning paths.

Generate from ACESim4 with:

    dotnet run --project LitigCharts -c Release -- equilibrium-paths --request "C:/Users/Admin/source/repos/correlated-signals-article/equilibrium-paths.request.json"

Every pivot is recorded in a JSONL file; JSON metadata identifies the information
sets and actions and records validation and input hashes. Successful metadata
requires both the original log's pivot count and the original saved equilibrium
probabilities to match. A complete four-run batch also has a manifest. A JSONL
without matching successful metadata is incomplete and must not be animated.

The original pivot counts are 209 (risk-neutral American), 235 (risk-neutral
British), 403 (risk-averse American), and 975 (risk-averse British).

Probabilities include every action at all 80 information sets, including both
private exit-commitment histories for offers. Undefined local incentives are
null. Uniform fallback at a zero-realization history is flagged; it is not
evidence of equilibrium mixing.

Epsilon is the largest unrestricted unilateral best-response gain. Local action
advantage is the conditional utility of that action minus the utility of the
current mix, holding continuation strategies fixed. Positive off-path local
advantages can remain at a Nash equilibrium; the full-game epsilon is a separate
measure. Neither epsilon nor strategy movement must be monotone along the path.

For the mathematical construction of intermediate behavioral profiles and the
native LCP residuals, see ACESim4's `scripts/Equilibrium-paths.md` and each result's
Interpretation field. Existing production equilibria are never overwritten.
