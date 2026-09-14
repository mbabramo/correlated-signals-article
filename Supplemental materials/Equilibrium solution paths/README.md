# Equilibrium solution paths

This separate workflow contains the interactive HTML paths and JSON/JSONL records for the four ordinary-cost American/Trial Fee-Shifting RN/RA reference cases. `all-equilibrium-solution-paths.html` is the combined viewer. These paths describe computation, not an observed adjustment process in litigation.

`equilibrium-paths.request.json` is the live regeneration request; `equilibrium-paths.recorded-request.json` preserves the original request. The manifest identifies the calculation sources and outputs. Original solve logs are retained under `Sources/Original solve logs`, and the live request references the preserved strategy-calculation inputs. These analyses were retained and rebased during the results cleanup; they were not recalculated in the 124-case report rebuild.

This workflow is separate from the game-tree worked path and the routine parameter comparisons. Consult ACESim4's equilibrium-path command and the live request before launching an intentional recalculation.
