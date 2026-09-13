# Original ECTA equilibrium derivations

[Open the four-case solution-path viewer](all-equilibrium-derivations.html)

- [American rule, risk-neutral](risk-neutral-american-cost-1.html)
- [British rule, risk-neutral](risk-neutral-british-cost-1.html)
- [American rule, moderate risk aversion](risk-averse-american-cost-1.html)
- [British rule, moderate risk aversion](risk-averse-british-cost-1.html)

All four original pivot counts and all 480 saved action probabilities per case
match exactly. The batch contains 1,826 frames, including four initial priors.
Tracing code was checkpointed in ACESim4 commit 30554e89 before animation work.

Open the self-contained HTML files in a current browser (tested in the Codex
in-app Chromium browser). Play runs only the selected case and stops at its
equilibrium. Pressing Play there restarts the same case. Use the Case menu to
choose another solve, starting at its own uniform prior. The slider and Step
buttons retain every pivot within the selected case. Playback can skip unchanged
probabilities. Data compression is
lossless; no precision or steps are discarded.

Low signals are at the bottom of each panel, high signals at the top; P is above
D. Blue encodes probability, orange corners positive action advantage. Hatched rows
are actually unreached, and dots mark uniform completions. Off-path advantages
are optional. Hover or tap for precise values; Save frame as PNG exports the grid.

Optional smooth color transitions fade the blue cells between recorded pivots;
these are visual transitions, not additional solver states. Numerical values,
orange advantages and reach markings refer to the destination pivot throughout.
Pause, scrubbing and PNG export show the exact recorded frame. Reduced-motion
preferences disable smoothing.

These are independent replays of the original ordinary-cost American/British
equilibria under risk neutrality/moderate risk aversion. Each starts from the
original exact seed-zero uniform prior, under fixed rules throughout. They are
not transitions between equilibria or behavioral learning paths.

Generate from ACESim4 with:

    dotnet run --project LitigCharts -c Release -- equilibrium-paths --request "C:/Users/Admin/source/repos/correlated-signals-article/equilibrium-paths.request.json"

To rebuild animations from these completed traces without solving again:

    dotnet run --project LitigCharts -c Release -- equilibrium-paths --request "C:/Users/Admin/source/repos/correlated-signals-article/equilibrium-paths.request.json" --render-only

The default command calculates and renders; --calculate-only exports just data.
Choose a new output directory to repeat an already completed calculation batch.

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
