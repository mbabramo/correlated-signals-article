# Strategy changes after equilibrium-preserving mixing

Experimental comparison only. Original equilibria, solution-path animations and existing paper tables are unchanged. The mixing search chooses local diagnostic representatives, not globally or uniquely maximally mixed equilibria.

**Focus rule:** retain a changed, commonly reached information set if more than 0.0001% of the original policy uses actions worse than the best local action by more than 1E-06 target-utility units, against the target opponent and with the player's subsequent decisions reoptimized. This allows overlapping supports. A change between tied actions is shown separately, not declared irrelevant: it may be needed to sustain the opponent's incentives.

One row per information set. The decomposed quantity is probability assigned to the set of actions that gain probability (percentage points), not the mean offer. Thus mixed distributions do not explode into one row per action. Full action-level decompositions remain in the calculation JSON.

| Intervention (ordinary costs) | Original changed sets | Original focus | After mixing | Focus retained | Disjoint supports after mixing | Focus with Remaining |
|---|---:|---:|---:|---:|---:|---:|
| American → British; risk neutral | 4 | 3 | 9 | 2 | 1 | 0 |
| American → British; moderate risk aversion | 22 | 11 | 22 | 12 | 15 | 0 |
| Risk neutral → moderate risk aversion; American rule | 20 | 20 | 22 | 22 | 15 | 0 |
| Risk neutral → moderate risk aversion; British rule | 13 | 6 | 14 | 8 | 7 | 1 |

The same focus rule can be applied without mixing (Original focus column). Greater mixing does not necessarily reduce the number of differences or resolve selection dependence.


**Reading the allocation:** Direct changes the rule/preferences first. Entry, offers and exit average the incremental opponent-policy replacements over all six orders. Remaining is the target share minus the selected best-response share with all opponent policies replaced; it is not assigned to a mechanism. This is diagnostic accounting, not an identified causal explanation.

Flags: `*` nonzero Remaining; `T` tie-selection sensitivity; `C` donor-off-path completion sensitivity; `H` some hybrid response does not reach this information set (conditional values remain defined); `U` zero counterfactual reach prevents allocation. Rounding can make tiny effects display as zero.

## American → British; risk neutral

### Focused changes

| Decision | Signal | Actions gaining probability | Shift (pp) | Direct | Opp. entry | Opp. offers | Opp. exit | Remaining | Flags |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| P Files | 0.25 | Yes | 12.17 | 12.17 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| P Offer / continue | 0.35 | 0.05 | 100.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |

### Endpoint strategies for focused changes

| Decision | Signal | Original diagnostic distribution | Target diagnostic distribution | Old-policy local loss at target |
|---|---:|---|---|---:|
| P Files | 0.25 | Yes: 87.83%; No: 12.17% | Yes: 100% | 0.000526451 |
| P Offer / continue | 0.35 | 0.45: 5.91%; 0.55: 12.74%; 0.65: 19.57%; 0.75: 26.4%; 0.85: 27.59%; 0.95: 7.79% | 0.05: 100% | 0.126508 |

Local loss uses the target utility scale and optimized own continuation against the target opponent. It does not compare welfare across risk regimes or measure the loss of reverting the entire strategy. Fixed-target-continuation losses are also retained in the JSON.

### Other changed sets (retained for audit)

| Decision | Signal | Actions gaining probability | Shift (pp) | Direct | Opp. entry | Opp. offers | Opp. exit | Remaining | Flags |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| P Offer / continue | 0.45 | 0.95 | 30.74 | 0.00 | -5.10 | -22.45 | 27.55 | 30.74 | *TC |
| P Offer / continue | 0.55 | 0.95 | 22.83 | 0.00 | -29.18 | -10.41 | 39.59 | 22.83 | *TC |
| P Offer / continue | 0.65 | 0.65, 0.95 | 12.66 | 0.00 | -17.87 | -16.07 | 33.93 | 12.66 | *TC |
| P Offer / continue | 0.75 | 0.65, 0.75, 0.95 | 9.44 | 0.00 | -22.96 | 11.48 | 11.48 | 9.44 | *TC |
| P Offer / continue | 0.85 | 0.65, 0.75 | 13.63 | 0.00 | 4.78 | -2.39 | -2.39 | 13.63 | *TC |
| P Offer / continue | 0.95 | 0.55, 0.65, 0.75 | 17.53 | 0.00 | 7.10 | -3.55 | -3.55 | 17.53 | *TC |
| D Answers | 0.65 | No | 8.29 | 8.29 | -50.00 | -50.00 | 0.00 | 100.00 | * |

2 histories change reach and are excluded from the two-endpoint strategy comparison. They remain listed in the JSON.

## American → British; moderate risk aversion

### Focused changes

| Decision | Signal | Actions gaining probability | Shift (pp) | Direct | Opp. entry | Opp. offers | Opp. exit | Remaining | Flags |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| P Files | 0.05 | No | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| P Files | 0.15 | No | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| P Files | 0.25 | No | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | C |
| P Abandons | 0.35 | Yes | 100.00 | 0.00 | 0.00 | 50.00 | 50.00 | 0.00 | TCH |
| P Abandons | 0.45 | Yes | 100.00 | 0.00 | 0.00 | 50.00 | 50.00 | 0.00 | TC |
| P Abandons | 0.55 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | TC |
| D Answers | 0.85 | No | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | C |
| D Answers | 0.95 | No | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| D Defaults | 0.45 | Yes | 100.00 | 0.00 | 33.33 | 83.33 | -16.67 | 0.00 | TC |
| D Defaults | 0.55 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | TC |
| D Defaults | 0.65 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | TCH |
| D Defaults | 0.75 | Yes | 100.00 | 0.00 | 0.00 | 50.00 | 50.00 | 0.00 | TH |

### Endpoint strategies for focused changes

| Decision | Signal | Original diagnostic distribution | Target diagnostic distribution | Old-policy local loss at target |
|---|---:|---|---|---:|
| P Files | 0.05 | Yes: 100% | No: 100% | 0.020959 |
| P Files | 0.15 | Yes: 100% | No: 100% | 0.0143025 |
| P Files | 0.25 | Yes: 100% | No: 100% | 0.00402183 |
| P Abandons | 0.35 | No: 100% | Yes: 100% | 0.00213593 |
| P Abandons | 0.45 | No: 100% | Yes: 100% | 0.0107562 |
| P Abandons | 0.55 | No: 100% | Yes: 100% | 0.0198596 |
| D Answers | 0.85 | Yes: 100% | No: 100% | 0.0492877 |
| D Answers | 0.95 | Yes: 100% | No: 100% | 0.0783073 |
| D Defaults | 0.45 | No: 100% | Yes: 100% | 0.0285228 |
| D Defaults | 0.55 | No: 100% | Yes: 100% | 0.139747 |
| D Defaults | 0.65 | No: 100% | Yes: 100% | 0.0745816 |
| D Defaults | 0.75 | No: 100% | Yes: 100% | 0.0144805 |

Local loss uses the target utility scale and optimized own continuation against the target opponent. It does not compare welfare across risk regimes or measure the loss of reverting the entire strategy. Fixed-target-continuation losses are also retained in the JSON.

### Other changed sets (retained for audit)

| Decision | Signal | Actions gaining probability | Shift (pp) | Direct | Opp. entry | Opp. offers | Opp. exit | Remaining | Flags |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| P Abandons | 0.65 | Yes | 91.35 | 100.00 | 0.00 | 50.00 | -50.00 | -8.65 | *TC |
| P Offer / continue | 0.65 | 0.65, 0.75, 0.95 | 75.17 | 0.00 | 16.67 | 16.67 | 66.67 | -24.83 | *CH |
| P Offer / continue | 0.75 | 0.65, 0.75, 0.95 | 77.21 | 0.00 | 50.00 | 0.00 | 50.00 | -22.79 | *CH |
| P Offer / continue | 0.85 | 0.65, 0.75, 0.95 | 77.20 | 0.00 | 0.00 | 50.00 | 50.00 | -22.80 | *C |
| P Offer / continue | 0.95 | 0.65, 0.75, 0.95 | 76.88 | 0.00 | 16.67 | 66.67 | 16.67 | -23.12 | *C |
| D Answers | 0.75 | No | 80.99 | 0.00 | 0.00 | 50.00 | -50.00 | 80.99 | *C |
| D Offer / continue | 0.05 | 0.05 | 100.00 | 0.00 | 16.67 | 16.67 | 66.67 | 0.00 | C |
| D Offer / continue | 0.15 | 0.05 | 100.00 | 0.00 | 50.00 | 0.00 | 50.00 | 0.00 | C |
| D Offer / continue | 0.25 | 0.05 | 100.00 | 0.00 | 50.00 | 0.00 | 50.00 | 0.00 | CH |
| D Offer / continue | 0.35 | 0.05, 0.25 | 66.67 | 0.00 | -16.67 | -16.67 | 33.33 | 66.67 | *TCH |

25 histories change reach and are excluded from the two-endpoint strategy comparison. They remain listed in the JSON.

## Risk neutral → moderate risk aversion; American rule

### Focused changes

| Decision | Signal | Actions gaining probability | Shift (pp) | Direct | Opp. entry | Opp. offers | Opp. exit | Remaining | Flags |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| P Files | 0.05 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| P Files | 0.15 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| P Files | 0.25 | Yes | 12.17 | -87.83 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| P Offer / continue | 0.25 | 0.15 | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | H |
| P Offer / continue | 0.35 | 0.15 | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | H |
| P Offer / continue | 0.45 | 0.15 | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | H |
| P Offer / continue | 0.55 | 0.85 | 64.40 | 0.00 | 32.20 | 32.20 | 0.00 | 0.00 | TC |
| P Offer / continue | 0.65 | 0.85 | 63.99 | 0.00 | 15.33 | 65.33 | -16.67 | 0.00 | TC |
| P Offer / continue | 0.75 | 0.85 | 65.55 | 0.00 | 16.11 | 66.11 | -16.67 | 0.00 | TC |
| P Offer / continue | 0.85 | 0.85 | 67.42 | 0.00 | 17.04 | 67.04 | -16.67 | 0.00 | TC |
| P Offer / continue | 0.95 | 0.85 | 68.51 | 0.00 | 0.92 | 50.92 | 16.67 | 0.00 | TC |
| D Answers | 0.65 | Yes | 91.71 | -8.29 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| D Answers | 0.75 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| D Answers | 0.85 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| D Answers | 0.95 | Yes | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| D Offer / continue | 0.05 | 0.15 | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| D Offer / continue | 0.15 | 0.15 | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 |  |
| D Offer / continue | 0.25 | 0.15 | 100.00 | 0.00 | 16.67 | 66.67 | 16.67 | 0.00 | C |
| D Offer / continue | 0.35 | 0.15 | 100.00 | 0.00 | 16.67 | 66.67 | 16.67 | 0.00 | C |
| D Offer / continue | 0.45 | 0.15 | 100.00 | 0.00 | 16.67 | 66.67 | 16.67 | 0.00 | C |
| D Offer / continue | 0.55 | 0.85 | 100.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | H |
| D Offer / continue | 0.65 | 0.85 | 100.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | H |

### Endpoint strategies for focused changes

| Decision | Signal | Original diagnostic distribution | Target diagnostic distribution | Old-policy local loss at target |
|---|---:|---|---|---:|
| P Files | 0.05 | No: 100% | Yes: 100% | 0.00816007 |
| P Files | 0.15 | No: 100% | Yes: 100% | 0.012118 |
| P Files | 0.25 | Yes: 87.83%; No: 12.17% | Yes: 100% | 0.00225043 |
| P Offer / continue | 0.25 | 0.05: 100% | 0.15: 100% | 0.0176775 |
| P Offer / continue | 0.35 | 0.45: 5.91%; 0.55: 12.74%; 0.65: 19.57%; 0.75: 26.4%; 0.85: 27.59%; 0.95: 7.79% | 0.15: 100% | 0.0568077 |
| P Offer / continue | 0.45 | 0.55: 7.38%; 0.65: 16.76%; 0.75: 26.13%; 0.85: 32.38%; 0.95: 17.34% | 0.15: 100% | 0.0298977 |
| P Offer / continue | 0.55 | 0.65: 10.77%; 0.75: 22.41%; 0.85: 35.6%; 0.95: 31.22% | 0.85: 100% | 0.0162056 |
| P Offer / continue | 0.65 | 0.65: 2.75%; 0.75: 15.8%; 0.85: 36.01%; 0.95: 45.44% | 0.85: 100% | 0.019979 |
| P Offer / continue | 0.75 | 0.75: 9.55%; 0.85: 34.45%; 0.95: 56.01% | 0.85: 100% | 0.0194258 |
| P Offer / continue | 0.85 | 0.75: 7.18%; 0.85: 32.58%; 0.95: 60.24% | 0.85: 100% | 0.0159236 |
| P Offer / continue | 0.95 | 0.65: 0.77%; 0.75: 9.88%; 0.85: 31.49%; 0.95: 57.86% | 0.85: 100% | 0.011824 |
| D Answers | 0.65 | Yes: 8.29%; No: 91.71% | Yes: 100% | 0.189361 |
| D Answers | 0.75 | No: 100% | Yes: 100% | 0.136633 |
| D Answers | 0.85 | No: 100% | Yes: 100% | 0.0895426 |
| D Answers | 0.95 | No: 100% | Yes: 100% | 0.0603076 |
| D Offer / continue | 0.05 | 0.05: 100% | 0.15: 100% | 0.144519 |
| D Offer / continue | 0.15 | 0.05: 100% | 0.15: 100% | 0.191623 |
| D Offer / continue | 0.25 | 0.05: 100% | 0.15: 100% | 0.251413 |
| D Offer / continue | 0.35 | 0.05: 100% | 0.15: 100% | 0.31294 |
| D Offer / continue | 0.45 | 0.05: 100% | 0.15: 100% | 0.353993 |
| D Offer / continue | 0.55 | 0.05: 100% | 0.85: 100% | 0.500349 |
| D Offer / continue | 0.65 | 0.05: 100% | 0.85: 100% | 0.693665 |

Local loss uses the target utility scale and optimized own continuation against the target opponent. It does not compare welfare across risk regimes or measure the loss of reverting the entire strategy. Fixed-target-continuation losses are also retained in the JSON.

### Other changed sets (retained for audit)

None.


10 histories change reach and are excluded from the two-endpoint strategy comparison. They remain listed in the JSON.

## Risk neutral → moderate risk aversion; British rule

### Focused changes

| Decision | Signal | Actions gaining probability | Shift (pp) | Direct | Opp. entry | Opp. offers | Opp. exit | Remaining | Flags |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| P Files | 0.25 | No | 100.00 | 100.00 | 33.33 | -16.67 | -16.67 | 0.00 | C |
| P Abandons | 0.35 | Yes | 100.00 | 0.00 | 50.00 | 0.00 | 50.00 | 0.00 | TCH |
| P Abandons | 0.45 | Yes | 100.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | TC |
| P Abandons | 0.55 | Yes | 100.00 | 0.00 | 16.67 | 16.67 | 66.67 | 0.00 | TC |
| P Offer / continue | 0.95 | 0.95 | 11.60 | 0.00 | 1.52 | -24.40 | 75.60 | -41.12 | *TC |
| D Answers | 0.65 | Yes | 100.00 | 0.00 | -16.67 | 33.33 | 83.33 | 0.00 | C |
| D Defaults | 0.45 | Yes | 100.00 | 0.00 | 50.00 | 50.00 | 0.00 | 0.00 | TCH |
| D Defaults | 0.55 | Yes | 100.00 | 0.00 | 0.00 | 50.00 | 50.00 | 0.00 | TCH |

### Endpoint strategies for focused changes

| Decision | Signal | Original diagnostic distribution | Target diagnostic distribution | Old-policy local loss at target |
|---|---:|---|---|---:|
| P Files | 0.25 | Yes: 100% | No: 100% | 0.00402183 |
| P Abandons | 0.35 | No: 100% | Yes: 100% | 0.00213593 |
| P Abandons | 0.45 | No: 100% | Yes: 100% | 0.0107562 |
| P Abandons | 0.55 | No: 100% | Yes: 100% | 0.0198596 |
| P Offer / continue | 0.95 | 0.55: 1.81%; 0.65: 9.39%; 0.75: 16.97%; 0.85: 24.55%; 0.95: 47.28% | 0.65: 4.6%; 0.75: 13.4%; 0.85: 23.12%; 0.95: 58.88% | 0.000807536 |
| D Answers | 0.65 | No: 100% | Yes: 100% | 0.10466 |
| D Defaults | 0.45 | No: 100% | Yes: 100% | 0.0285228 |
| D Defaults | 0.55 | No: 100% | Yes: 100% | 0.139747 |

Local loss uses the target utility scale and optimized own continuation against the target opponent. It does not compare welfare across risk regimes or measure the loss of reverting the entire strategy. Fixed-target-continuation losses are also retained in the JSON.

### Other changed sets (retained for audit)

| Decision | Signal | Actions gaining probability | Shift (pp) | Direct | Opp. entry | Opp. offers | Opp. exit | Remaining | Flags |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| P Abandons | 0.65 | Yes | 91.35 | 0.00 | -16.67 | 83.33 | 33.33 | -8.65 | *TC |
| P Offer / continue | 0.65 | 0.65, 0.75 | 29.70 | -17.44 | 0.00 | 0.00 | 0.00 | 47.14 | *CH |
| P Offer / continue | 0.75 | 0.95 | 7.20 | -57.73 | 14.09 | -7.05 | 92.95 | -35.07 | *TCH |
| P Offer / continue | 0.85 | 0.95 | 10.54 | 0.00 | -2.80 | -25.70 | 74.30 | -35.27 | *TC |
| D Answers | 0.75 | Yes | 19.01 | 0.00 | 0.00 | 0.00 | 100.00 | -80.99 | *C |
| D Offer / continue | 0.35 | 0.15, 0.25 | 66.67 | 0.00 | 0.00 | 0.00 | 0.00 | 66.67 | *TH |

17 histories change reach and are excluded from the two-endpoint strategy comparison. They remain listed in the JSON.
