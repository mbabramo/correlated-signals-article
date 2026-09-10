# Liability-signal illustrations

## Retained: truth-conditioned merits robustness model

`Truth-conditioned merits - party signals.pdf` is the earlier `liability signals default.pdf`, renamed without changing its contents. It remains useful for the **truth-conditioned latent merits** robustness specification, not for the principal continuous-merits model.

The old default diagram's construction and settings match that robustness specification:

| Feature | Setting |
|---|---|
| True liability | Binary, with probability 0.5 |
| Merits given truth | Ten discrete midpoint levels, 0.05 through 0.95 |
| Noise from truth to merits | Normal standard deviation 0.35, with the signal-construction boundary treatment |
| Party signals given merits | Ten midpoint signal bins; normal standard deviation 0.2 |
| Figure's rightmost column | One party's signal; the same kernel applies to either party |

The retained PDF is the earlier rendering. This review checked its depicted structure, the original manuscript's stated parameters, and the current model specification; it did not re-estimate every flow width from the PDF. Refresh its caption and publication styling when preparing the appendix. The current court signal has two bins and is not depicted by the figure's ten-bin party-signal column.

Evidence for the match is in ACESim4's `LitigGameCorrelatedSignalsArticleLauncher.ConfigureFocusedSpecification` (`TruthConditionedLatentMerits`), `LitigGameExogenousDisputeGenerator.Setup`, and the truth-conditioned specification metadata in `Results/CS004 numerical results.csv`.

Suggested caption: *Truth-conditioned discrete merits robustness specification. True liability determines a distribution over ten merits levels, and each party receives a noisy signal conditional on merits. This diagram depicts a party's signal, not the court's signal or the principal continuous-merits model.*

## Removed variants

The nine other diagrams varied party noise, truth-to-merits noise, the true-liability prior, or the size of the discrete game. Those full combinations are not in the current truth-conditioned robustness matrix. The current low/high-noise checks use the continuous-merits model, so their diagrams cannot simply be borrowed from this older family.

The removed variants remain recoverable from article commit `af9a3a1ba6562b9c487f9f0bc670be0df93731eb` and earlier history.

## Different illustrations still needed

- Principal model: continuous merits Q, the truth relationship `T | Q ~ Bernoulli(Q)`, and party/court signals conditional on Q.
- Direct-binary robustness: signals generated directly from true liability, without the intermediate merits column and with that specification's calibrated signal noise.

Neither is represented by the retained three-column diagram. These can be drawn from the existing model definitions without solving the equilibria again.
