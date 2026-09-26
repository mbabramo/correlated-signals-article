# Rebuild the Results collection

From the article repository root, run:

```powershell
python .\generate_results.py
```

This one command restores the pinned dependencies, compiles the complete numerical engine, LitigCharts and the diagnostic host in Release, and regenerates the available Results collection. It does not rely on previously compiled application DLLs or on the original Codex workspace paths. The source snapshot and all complete saved profiles are bundled.

It revalidates 72 primary profiles, rebuilds their strategy PDFs and aggregate outcomes, recalculates the available American/British four-corner welfare decompositions, and reruns the 203-profile tremble study. The automated sensitivity report includes all 6,496 checks, per-profile results, group ranges, the definition of welfare reversals, and the comparisons after one player responds. Thirty-two independent full-tree best-response comparisons and 16 independent outcome checks run automatically. Complete off-path strategies are retained.

The pipeline checks every primary scientific profile and welfare value against the frozen audited results. Every field of the tremble test table must reproduce the frozen result. Existing primary best-response, normalization, accounting, saved-action and numeric-replay checks remain in place. A failed step prevents publication of the new collection and leaves its logs intact.

The Results folder keeps its existing Individual simulations, Aggregated Data and Run records structure. Tremble reports are under Aggregated Data/Equilibrium sensitivity. Replaced files are first copied and hash-checked into the build's archive. Unrelated files, the manuscript, Figures, Tables and supplemental folders are not overwritten by this results-only command. A run record identifies the generated files and fresh build. Existing visual-review records apply only to the artifact hashes they identify; recompilation does not create a new human visual approval.

## Requirements

- Windows; tested with Python 3.12.
- .NET SDK 10.0.401 and the .NET 9 runtime, on PATH. The supplied global.json fixes the SDK; NuGet lock files fix the dependency graph and content hashes.
- LuaLaTeX with the packages required by the existing strategy exhibits (tested with MiKTeX).
- The Python packages pinned in requirements.txt. Install with `python -m pip install -r "Results/Run records/Reproduction/requirements.txt"` if needed.
- Network access for the first NuGet restore, or a populated NuGet cache.

## Options

```powershell
python .\generate_results.py --workers 29
python .\generate_results.py --workers 4 --output C:\Reports\Results --work C:\Reports\reproduction-run-1
```

The default is one worker. Each computation is single-threaded. Set workers to the number available within the shared 32-computation ceiling, including other active work. Workers are hidden. Builds use one MSBuild worker. An operating-system lock rejects overlapping invocations for this repository. Each invocation creates a fresh isolated build directory; it refuses to overwrite an existing work directory. Completed runs and failed attempts are preserved under .reproduction unless an explicit work location is supplied. LaTeX intermediate files stay in the isolated build rather than entering the reader-facing Results folders.

This regenerates results from saved equilibria; it does not rerun equilibrium searches. The frozen input set contains 72 of the 74 selected primary profiles and marks the two missing British risk-averse grid cases explicitly. It also preserves the distinction between 199 accepted approximate profiles and four exact primary profiles. Missing profiles are never silently simulated, approximated or treated as zero. Update the frozen input package after those profiles have completed and passed the established import/audit procedure.

The source snapshot is commit 204536f57afe5415e641870129d555c962fd8f68. The original exact ECTA certificate and frozen production builds are unaffected. These report rebuilds do not substitute for that certificate, and a completed report rebuild does not mean that all article publication gates have been completed.
