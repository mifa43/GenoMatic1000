# GenoMatic1000 PMP22 target snapshot

This package is the first local target bundle for PMP22 / CMT1A analysis.

## What this is

A local definition of the PMP22 target region on GRCh38:

- Gene: PMP22
- Ensembl Gene ID: ENSG00000109099
- Region: chr17:15,229,773-15,272,292, 1-based inclusive
- BED interval: chr17 15229772 15272292, 0-based half-open
- Strand: reverse/minus
- Main variant class for CMT1A: CNV / structural duplication, usually represented as SVTYPE=DUP or copy-number increase

## Files

- `pmp22_target_manifest.json` — machine-readable target definition.
- `pmp22_target_region.bed` — interval filter format for genomic tools.
- `pmp22_target_region.csv` — simple table for Pandas/Dash.
- `pmp22_ensembl_endpoints.txt` — Ensembl URLs to refresh raw data.
- `fetch_pmp22_ensembl_snapshot.py` — Windows-compatible Python downloader.

## Why this matters

For CMT1A, the first target is not an ordinary SNP list. The primary pattern is a structural/copy-number event affecting the PMP22 region. Your pipeline should therefore parse interval-level records and not only small variants.

Recommended VCF/SV INFO fields to inspect:

- SVTYPE
- END
- SVLEN
- CN or copy number-like fields
- CIPOS / CIEND
- IMPRECISE

Recommended genotype-level fields to inspect:

- GT
- CN
- GQ
- DR / DV or similar caller-specific evidence fields

## Assembly warning

Do not mix GRCh37 and GRCh38 coordinates. The interval in this package is intended for GRCh38/hg38.
