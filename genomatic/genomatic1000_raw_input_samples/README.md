# GenoMatic1000 raw input sample fixtures

These files are parser fixtures, not diagnostic data.

Files:
- sample_pmp22_cnv.vcf: synthetic VCF structural variant records for PMP22 DUP and DEL.
- sample_pmp22_target.bed: BED interval examples using 0-based half-open coordinates.
- sample_cnv_segments.csv: common lab/CNV-caller segment style table.
- sample_ensembl_features.tsv: Ensembl-like gene/transcript/exon feature table.
- sample_ensembl_pmp22_lookup_subset.json: subset from local Ensembl REST snapshot.
- sample_lab_report_synthetic.txt: synthetic plain-text lab report style fixture.

Recommended parser target: convert all examples into one StandardEvent object with assembly, chrom, start, end, variant_class, event_direction, copy_number, target_gene, overlap_fraction, and mapped_standard_systems.
