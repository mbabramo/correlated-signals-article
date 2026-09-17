# Multiple equilibria

Six ordinary-cost scenarios cross three fee rules with risk neutrality and symmetric CARA alpha 2. 85 distinct profiles were recovered from 50 initializations per case.

See [Findings.md](Findings.md) for the substantive conclusions, including universal answering in all 22 recovered Complete Fee-Shifting profiles and the variation in risk-averse outcomes. [Sources/answering-verification.json](Sources/answering-verification.json) records the direct checks at all defendant signals; [Sources/verify_answering.py](Sources/verify_answering.py) reproduces them from the saved action reports.

Risk Comparison and each risk folder contain separate welfare-range and disposition-range tables; recovery diagnostics are in Risk Comparison. Individual simulations contains each equilibrium's generated figures, grouped by risk and fee rule. Sources contains exact data, editable TeX and captions. The production manifest identifies the solving build; the exhibit inventory separately records reporting inputs and output hashes.

Individual diagrams are regenerated from each saved profile separately, and each replay is checked against the original numeric outcome report. Sources/Replayed reports contains these checks' report inputs. Original production TeX is preserved as historical source material; older builds pooled preceding profiles' paths in individual diagrams, so those raw TeX files must not be used as individual-equilibrium exhibits.

Ranges across distinct recovered equilibrium strategy profiles; each profile receives equal weight. Recovery frequencies describe numerical searches, not behavioral equilibrium selection. Each scenario requests fifty starts; failed attempts can leave fewer verified recoveries. These ranges are not confidence intervals or guarantees that every equilibrium has been found. Cost multiplier is 1. Gross outcome error is E[|R-T|], averaged over all potential disputes. R is the base payment before legal costs and separately awarded fee transfers; T is true liability and damages equal one. Since payments lie in [0,1], error equals pi(1-E[R|T=1])+(1-pi)E[R|T=0]. Conditional means are intermediate calculations, not conditional headline outcomes. The configured truth prior is also used for the three net-burden contributions. Source reports are rounded. Fee rules still affect error through equilibrium behavior. The five measures are distinct, not additive welfare components.

Additional approximate attempts are capped at 500 pivots and additional exact attempts at 1,000; the initial exact solve is uncapped. A cutoff ends that attempt; failed exact attempts are not replaced with additional starts. Read the actual recovery totals and the saved solve logs together.

Sources/strategy-verification.json records a fresh best-response check for every saved profile and reproduction of its action report. The recovery table uses these current-profile gains. The original report statistic is retained separately because older reporting builds measured the running average of profiles instead.

The legacy truth-specific burden columns in the full CSV remain conditional diagnostics. The five headline columns and all displayed disposition shares are population averages. Conditional offer means describe reached bargaining decisions. Distinctness follows the production recovery catalog; behavioral/outcome differences must be assessed separately.

Regenerate with `LitigCharts multiple-equilibria-report --input <completed production directory> --output <this folder> --jobs 32`. The supplemental rebuild script runs this automatically after multiple-start aggregation.
