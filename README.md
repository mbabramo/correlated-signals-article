# Correlated signals in litigation

[Author-maintained article](https://github.com/mbabramo/correlated-signals-article/tree/main/Article%20and%20bibliography) · [Figures](Figures/README.md) · [Tables](Tables/README.md)

This collection contains 74 validated primary profiles from the 74-case resolved article plan. The grid comparisons are 8 signals / 12 offers (both risk preferences); 12 signals / 8 offers (both risk preferences); 8 signals / 8 offers (both risk preferences). American and British denote the principal rules; trial-only fee shifting is a separate extension.

- **Figures** and **Tables**: exhibits included in the article, with editable sources and previews.
- **Results/Individual simulations**: complete strategies, audits, numerical reports and standard diagrams for every reported game.
- **Results/Aggregated Data**: matched comparisons, welfare measures, truth-formula sensitivity and tremble responses.
- **Supplemental materials**: multiple-equilibrium results, decompositions, solution-path viewers, signal and game-tree diagrams, and utility curves.

The **Article and bibliography** folder is author-maintained and separate from default replication. The journal command generates the four research-output folders above. An optional `--manuscript true` author build also compiles the embedded manuscript snapshot with generated numerical bindings; it never overwrites the author's checkout.

## Replication

Use the `ArticleReplication` C# project in the [ACESim4 correlated-signals branch](https://github.com/mbabramo/ACESim4/tree/correlated-signals). Follow its [installation instructions](https://github.com/mbabramo/ACESim4/blob/correlated-signals/ArticleReplication/INSTALL.md) for .NET, TeX, fonts and PDF tools, or use its container build target. Tools are installed separately.

Download and extract the optional saved-solutions archive from the [article repository releases](https://github.com/mbabramo/correlated-signals-article/releases). From the code checkout, run:

```sh
dotnet run --project ArticleReplication -c Release -- rebuild --source . --output /path/new-rebuild --input /path/saved-solutions --missing wait --workers 4
```

Read the collection in `new-rebuild/run/article`. Remove `--input` and use `--missing compute` for a complete fresh calculation, which can take substantially longer. Settings and stage switches are documented in the [coordinator README](https://github.com/mbabramo/ACESim4/blob/correlated-signals/ArticleReplication/README.md). Worker counts must account for other active computations.

Shortcuts contain only complete primary equilibria, the 200 multiple-start outcomes (including explicit failed attempts), and optional solver histories. Every accepted profile is revalidated; histories are replay-checked. Decompositions, tremble experiments, reports and exhibits are freshly generated. The manuscript PDF is compiled only when explicitly requested. Failed searches are not proofs of nonexistence. Exact-primary, approximate-search and trajectory-replay criteria remain distinct.

The case inventory is [selected-primary-catalog.json](Results/Aggregated%20Data/selected-primary-catalog.json). Temporary build, execution and release-review records belong outside this published collection.
