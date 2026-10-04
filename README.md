# Correlated signals in litigation

[Article](https://github.com/mbabramo/correlated-signals-article/tree/main/Article%20and%20bibliography) · [Figures](Figures/README.md) · [Tables](Tables/README.md)

- **Figures** and **Tables**: exhibits included in the article, with editable sources and previews.
- **Results/Individual simulations**: complete strategies, audits, numerical reports and standard diagrams for every reported game.
- **Results/Aggregated Data**: matched comparisons, welfare measures, truth-formula sensitivity and tremble responses.
- **Supplemental materials**: multiple-equilibrium results, decompositions, solution-path viewers, signal and game-tree diagrams, and utility curves.

Replication regenerates the results, tables, figures and supplemental materials. The article and bibliography are maintained separately.

## Replication

No programming experience is required. Docker runs the replication software with its required tools already installed.

1. **Install and start Docker.** Use [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) or [Docker Engine for Linux](https://docs.docker.com/engine/install/). On Windows, use Linux containers (the default).
2. **Download the saved solutions.** Create a new folder called `replication`. Download [this ZIP file](https://github.com/mbabramo/correlated-signals-article/releases/download/replication-20261004/correlated-signals-saved-solutions.zip), extract it, and put its contents in a folder named `solutions` inside `replication`. The `solutions` folder should contain `Equilibria`, `Search` and `Histories` directly.
3. **Open a terminal in the `replication` folder.** On Windows, right-click inside that folder and choose **Open in Terminal**, using a PowerShell tab. On Linux, open a terminal in that folder.
4. **Copy and paste this entire command**, then press Enter. You do not need to change any paths:

```sh
docker run --rm --network none --cpus 4 -v "${PWD}/solutions:/inputs:ro" -v "${PWD}/output:/output" ghcr.io/mbabramo/acesim-correlated-signals:2026-10-04.1 run --input /inputs --output /output/run --missing wait --workers 4
```

The first run downloads the software automatically; you do not need a GitHub account or a copy of the code. Leave the terminal open until it finishes. The completed results will be in **`replication/output/run/article`**. The program creates the output folders for you and refuses to overwrite an existing run. Use a new `replication` folder if you want to repeat the exercise.

The supplied solutions avoid repeating the slow equilibrium searches. The program checks those solutions and recalculates the analyses, tables and figures. This command is for Windows or Linux on an Intel/AMD computer; the tested machine has four available processors and 16 GB of memory.

[Detailed instructions and other options](https://github.com/mbabramo/ACESim4/blob/correlated-signals/ArticleReplication/INSTALL.md) · [C# source code](https://github.com/mbabramo/ACESim4/tree/correlated-signals) · [Simulation inventory](Results/Aggregated%20Data/selected-primary-catalog.json)
