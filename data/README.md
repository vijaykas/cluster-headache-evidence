# Data provenance

Every file here is derived from a public source by a script in `scripts/`.
Nothing is hand-entered except where noted, and nothing is patient data.

Re-running the matching script regenerates the file. Where a source has its
own licence or terms of use, those govern the underlying data; this
repository licenses only its compilation and derived analysis.

| File(s) | Source | Script |
| --- | --- | --- |
| `trial_people.json` | ClinicalTrials.gov API v2 | `fetch_trials.py`, `who_runs_trials.py` |
| `gtex_bg.json`, `gtex_risk.json`, `gtex_targets.json`, `htr7_gtex.json` | GTEx v8 median gene expression | `gtex.py`, `gtex_bg.py`, `ht7_gtex.py` |
| `eqtl_hits.json` | GTEx v8 single-tissue eQTLs | `eqtl_lookup.py` |
| `human_genes.tsv` | background gene set for enrichment testing | `gtex_bg.py` |
| `acts_*.json`, `approved.json`, `chembl_profiles.json`, `receptor_*.csv` | ChEMBL human activity data | `chembl_profiles.py`, `signature.py`, `screen_5ht7.py` |
| `aid_*.csv`, `gtopdb_5ht7_human.csv`, `ht7_pubchem.json` | IUPHAR/Guide to Pharmacology curated ligand tables, via PubChem | `ht7_pubchem.py` |
| `ht7_specificity.csv`, `dual_profile.csv`, `dual_tissue_top.csv` | derived from the above | `ht7_specificity.py`, `dual_profile.py`, `ht7_dual_test.py` |
| `pubmed_*.json`, `authors.json`, `ht7_scn.json` | PubMed E-utilities | `pubmed_counts.py`, `pubmed_ht7.py`, `who_publishes.py`, `ht7_scn.py` |
| `ht7_clinical.json` | ClinicalTrials.gov + PubMed | `ht7_clinical.py` |
| `nih_ch_grants.json` | NIH RePORTER API v2 | `nih_grants.py`, `nih_grants2.py` |
| `opentargets_genes.json` | Open Targets GraphQL | `opentargets.py` |
| `chart_rows.json`, `scatter.json` | derived plotting inputs | `ht7_dual_test.py` |

## Removed before publication

ClinicalTrials.gov returns investigator email addresses and phone numbers. Those
are public at source, but republishing them as a bulk file turns them into a
harvestable list, and no analysis here uses them. `scripts/sanitise_data.py`
strips them. Run it after any fetch that touches ClinicalTrials.gov.

## Hand-entered values

A small number of figures could not be fetched and were taken from published
papers. They are marked in the scripts where they appear:

- BOL-148 receptor affinities, from Lewis et al. 2023.
- Frovatriptan 5-HT7 functional data, from Comer 2002.
- 5-HT1B/1D/1F agonist potencies used in `dual_profile.py`, from the
  literature cited in `docs/analyses.md`.
- Clinical-effect labels in `ht7_specificity.py` and `dual_profile.py`,
  summarising the trial record in `docs/evidence-log.md`.

## Known gaps

- Winsvold 2023 full GWAS summary statistics are not public; lead variants only.
- ChEMBL was returning HTTP 500 during the Analysis 6 work, which is why the
  curated pharmacology is reached through PubChem rather than ChEMBL or the
  Guide to Pharmacology API (the latter requires a key).
- A UKRI Gateway to Research query failed to filter and returned unrelated
  projects; UK funding is therefore unmeasured, not absent.
