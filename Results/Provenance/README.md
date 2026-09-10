# Provenance and relocation

`ALER production suite manifest.json` and `diagram inventory.json` are unchanged copies from the completed model run. Their hashes and internal source paths remain as originally recorded.

`article import manifest.json` records the source-to-repository mapping and SHA-256 hash for every imported file. CS004 files moved into `Results/CS004`; CS004ME files moved into `Supplemental materials/CS004ME`. This mapping is necessary because original manifest references were relative to a shared run directory.

The import verified all 3,983 copies against the source, both plan-manifest hashes against the suite manifest, and all 1,358 applicable PDF hashes against the original diagram inventory. The original inventory contains 1,361 PDFs; the excluded three are generic hidden-state/liability/damages illustrations that do not describe the revised principal specification.

The import manifest also lists the omitted compilation files and coordinator state. It does not characterize the retained research plots as publication-ready.

The pre-migration article checkpoint is `7e92fc01e1d7ff92bf0b07dbe80ac9ff021ce7b3`. The numerical source commit is `31d0f17836435a2b1a7cc3fc52a6dfcec0db3565`; the diagram source commit is `a991f31fa355d788981bf399251123c17f8ebc89` in ACESim4.
