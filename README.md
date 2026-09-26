# Correlated-signals litigation article

Revised 25 September 2026 in the existing repository structure. Eight figures and four tables cover the currently available results. Figure 7 replaces Table 4 in Welfare Analysis; Figure 8 replaces Table 6 in Multiple Equilibria; Table 5 labels the two unfinished grid contrasts. The prior typography, directional patterns and shared American/British strategy axes are restored. Table names and captions are separate from the table files. No manuscript reorganization or figure consolidation is introduced.

- [Figures](Figures/README.md)
- [Tables](Tables/README.md)
- [Individual simulations](Results/Individual%20simulations/README.md)
- [Aggregated data](Results/Aggregated%20Data/README.md)
- [Generated pairwise comparisons](Supplemental%20materials/Generated%20pairwise%20comparisons/README.md)
- [Equilibrium strategy changes](Supplemental%20materials/Equilibrium%20strategy%20changes/README.md)
- [Liability signals diagrams](Supplemental%20materials/Liability%20signals%20diagrams/README.md)
- [Game tree diagrams](Supplemental%20materials/Game%20tree%20diagrams/README.md)
- [Multiple equilibria](Supplemental%20materials/Multiple%20equilibria/README.md)
- [Equilibrium solution paths](Supplemental%20materials/Equilibrium%20solution%20paths/README.md)
- [Risk aversion utility curves](Supplemental%20materials/Risk%20aversion%20utility%20curves/README.md)

The main material says American and British. Trial-only fee shifting is a cost-1 extension. Agreement decisions remain part of every primary game. Technical evidence stays with Sources and Run records.

Curation excludes eight non-cost-1 trial-only profiles, 40 associated directed decomposition reports, duplicate color signal diagrams, superseded overviews and failed render caches. All underlying research records are preserved in the isolated workspace.

Still pending before final publication:

- Two British risk-averse cost-1 exact profiles: 8 signals/15 offers and 12 signals/8 offers.
- Their two welfare comparisons and eight strategic directions, followed by updated Table 5 and supplemental summaries.
- Fourth verified trajectory and interactive visual QA of the viewers.
- User choice on truth-map sensitivity exponents (proposed 0.5 and 2, baseline 1), or explicit omission.
- Complete final release evidence after the pending work; the reviewed available working collection has now been archived, synchronized and committed.

[Manuscript and bibliography](Article%20and%20bibliography/) remain in their existing folder. This is the reviewed available working collection, not a certificate of completed final publication. Historical generated material is preserved in the external hash-verified archive identified in Results/Run records/working-collection-update.json.

The manuscript now contains limited factual corrections and explicit italicized **Update needed** passages. See [revision notes](Article%20and%20bibliography/Revision%20notes.md); the substantive narrative remains for the author to revise.

Rebuild the available Results collection with `python .\generate_results.py`. [Reproduction instructions](Results/Run%20records/Reproduction/README.md) describe prerequisites, workers, validation and archived replacements. The command rebuilds the numerical code and reports from the saved profiles; it does not start equilibrium searches.
