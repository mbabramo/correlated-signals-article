# Equilibrium solution paths

The completed collection reproduces 6 ordinary-cost original exact solves: every core fee rule crossed with every available risk level. These are numerical solver paths from the uniform prior, not transitions between fee regimes or models of how litigants learn an equilibrium.

Each replay must match its original log's pivot count and every saved final action probability (tolerance 1e-10), with final exploitability at most 1e-7. Sources/Original solve logs preserves original single-prior logs; cached-equilibrium validation logs cannot substitute for them. Sources/Requests and Sources/Traces contain reproducible requests, frame streams and fingerprinted verification metadata. Sources/Run records holds replay process logs.

All six replays have verified. all-equilibrium-solution-paths.html combines them, and each scenario also has an individual HTML viewer. equilibrium-paths-collection-manifest.json records completed collection inputs. The shared supplemental-plan.json lists requested jobs; it does not assert that pending traces have completed.

The generalized supplemental rebuild performs these replays and builds the collection automatically. Its path cache reuses completed traces only after checking their request, input, frame and assembly hashes. A separate multiple-start study is in Multiple equilibria.

All original pivot counts and saved action probabilities matched. The combined viewer uses distinct American, Trial Fee-Shifting and Complete Fee-Shifting labels within each risk preference; playback, stepping and equilibrium endpoints were checked in a browser. Sources/path-verification.json records numerical verification and visual review.

| Risk | American pivots | Trial Fee-Shifting pivots | Complete Fee-Shifting pivots |
|---|---:|---:|---:|
| Risk Neutral | 209 | 235 | 211 |
| Risk Averse | 403 | 975 | 1871 |
