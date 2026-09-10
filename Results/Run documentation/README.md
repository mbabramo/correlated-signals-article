# Run documentation

This folder explains where the results came from and how to reproduce or check them. These are supporting records rather than additional scientific results. They retain the model code versions, completed-run status, source filenames, and file hashes (checksums that detect changed files).

`ALER production suite manifest.json` and `diagram inventory.json` are unchanged copies from the completed model run. Their hashes and internal source paths remain as originally recorded.

`article import manifest.json` records the source-to-repository mapping and SHA-256 hash for every imported file. Main results are in `Results`, with individual simulations, aggregated data, and process logs in descriptive subfolders. Multiple-equilibrium results are in `Supplemental materials/Multiple equilibria`. This mapping is necessary because original manifest references were relative to a shared run directory. The import manifest was updated when the folders were renamed, and every imported file was verified again against its recorded SHA-256 hash.

`CS004 run manifest.json` records the main production plan. The multiple-equilibrium plan manifest remains with those results under `Supplemental materials/Multiple equilibria/CS004ME run manifest.json`.

The import verified all 3,983 copies against the source, both plan-manifest hashes against the suite manifest, and all 1,358 applicable PDF hashes against the original diagram inventory. The original inventory contains 1,361 PDFs; the excluded three are generic hidden-state/liability/damages illustrations that do not describe the revised principal specification.

The import manifest also lists the omitted compilation files and coordinator state. It does not characterize the retained research plots as publication-ready.

The pre-migration article checkpoint is `7e92fc01e1d7ff92bf0b07dbe80ac9ff021ce7b3`. The initial import is committed as `af9a3a1ba6562b9c487f9f0bc670be0df93731eb`. The numerical source commit is `31d0f17836435a2b1a7cc3fc52a6dfcec0db3565`; the diagram source commit is `a991f31fa355d788981bf399251123c17f8ebc89` in ACESim4.
