# Correlated signals in litigation

[Article](https://github.com/mbabramo/correlated-signals-article/tree/main/Article%20and%20bibliography) · [Figures](Figures/README.md) · [Tables](Tables/README.md)

- **Figures** and **Tables**: exhibits included in the article, with editable sources and previews.
- **Results/Individual simulations**: complete strategies, audits, numerical reports and standard diagrams for every reported game.
- **Results/Aggregated Data**: matched comparisons, welfare measures, truth-formula sensitivity and tremble responses.
- **Supplemental materials**: multiple-equilibrium results, decompositions, solution-path viewers, signal and game-tree diagrams, and utility curves.

Replication regenerates the results, tables, figures and supplemental materials. The article and bibliography are maintained separately.

## Replication

Choose **Docker**, which includes the required software, or **without Docker**, which builds the C# source using tools installed on your computer. Either option can use saved solutions or compute from scratch:

- **Use saved solutions:** verify the saved equilibria, search records and solver histories, then recalculate the analyses, tables and figures. This avoids the slow searches.
- **Compute from scratch:** run the equilibrium searches and recreate solver histories as well. No saved files are needed; this can take days or longer.

Create a new folder called `replication`. If using saved solutions, download [the saved-solutions ZIP](https://github.com/mbabramo/correlated-signals-article/releases/download/replication-20261004/correlated-signals-saved-solutions.zip) and extract its contents into `replication/solutions`. That folder should directly contain `Equilibria`, `Search` and `Histories`. Skip this download when computing from scratch.

### Using Docker

Install and start [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) or [Docker Engine for Linux](https://docs.docker.com/engine/install/). On Windows, use Linux containers (the default).

Open PowerShell on Windows, or a terminal on Linux, **inside the `replication` folder**. On Windows, right-click inside the folder and choose **Open in Terminal**, using a PowerShell tab. Copy and paste **one** of these commands, without changing any paths.

**With saved solutions:**

```sh
docker run --rm --network none --cpus 4 -v "${PWD}/solutions:/inputs:ro" -v "${PWD}/output:/output" ghcr.io/mbabramo/acesim-correlated-signals:2026-10-05 run --input /inputs --output /output/run --missing wait --workers 4
```

**From scratch, without saved solutions:**

```sh
docker run --rm --network none --cpus 4 -v "${PWD}/output:/output" ghcr.io/mbabramo/acesim-correlated-signals:2026-10-05 run --output /output/run --missing compute --workers 4
```

Docker downloads the software automatically. You do not need a GitHub account, a copy of the code, or separate .NET, TeX, font or PDF-tool installations.

### Without Docker

1. Install **.NET SDK 10.0.401 and the .NET 9 Runtime, TeX and fonts, and PDF tools**, following the [Windows/Linux installation instructions](https://github.com/mbabramo/ACESim4/blob/correlated-signals/ArticleReplication/INSTALL.md#run-without-docker).
2. Download and extract [the C# source ZIP](https://github.com/mbabramo/ACESim4/archive/refs/heads/correlated-signals.zip). Rename the extracted `ACESim4-correlated-signals` folder to `code` and place it inside `replication`. The `code` folder should directly contain `global.json` and `ArticleReplication`. If using saved solutions, keep `solutions` beside `code`.
3. Open PowerShell or a Linux terminal **inside `replication/code`**, and paste **one** of these commands.

**With saved solutions:**

```sh
dotnet run --project ArticleReplication -c Release -- rebuild --source . --output ../output --input ../solutions --missing wait --workers 4
```

**From scratch, without saved solutions:**

```sh
dotnet run --project ArticleReplication -c Release -- rebuild --source . --output ../output --missing compute --workers 4
```

Both commands rebuild the required C# projects before running. Keep an internet connection available for downloading build dependencies. Docker, Visual Studio, Git and Python are not required for this option.

### Finding the results

Leave the terminal open until the command finishes. All four options write the research collection to **`replication/output/run/article`**. The program creates the output folders and refuses to overwrite an existing run. Use a new `replication` folder for another run.

The commands use four workers on Windows or Linux with an Intel/AMD processor; the container was tested with four processors and 16 GB of memory. Each numerical solve remains single-threaded. The saved-solutions commands use `--missing wait` to avoid accidentally launching a slow search if a supplied file is missing. The from-scratch commands use `--missing compute` and read no saved solutions.

[Detailed instructions and settings](https://github.com/mbabramo/ACESim4/blob/correlated-signals/ArticleReplication/INSTALL.md) · [C# source code](https://github.com/mbabramo/ACESim4/tree/correlated-signals) · [Simulation inventory](Results/Aggregated%20Data/selected-primary-catalog.json)
