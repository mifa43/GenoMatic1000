# Unutar main.py
from parser.helpers.detect_file_type import SAMPLE_WORKING_DIR
from parser.raw_parser import RawParser


vcf_path = SAMPLE_WORKING_DIR / "sample_pmp22_cnv.vcf"
bed_path = SAMPLE_WORKING_DIR / "sample_pmp22_target.bed"
csv_path = SAMPLE_WORKING_DIR / "sample_cnv_segments.csv"
tsv_path = SAMPLE_WORKING_DIR / "sample_ensembl_features.tsv"
json_path = SAMPLE_WORKING_DIR / "sample_ensembl_pmp22_lookup_subset.json"
text_path = SAMPLE_WORKING_DIR / "sample_lab_report_synthetic.txt"

# vcf_df = RawParser(vcf_path).read()
# bed_df = RawParser(bed_path).read()
# csv_df = RawParser(csv_path).read()
# tsv_df = RawParser(tsv_path).read()
# json_df = RawParser(json_path).read()
# text_df = RawParser(text_path).read()

# print(vcf_df)
# print(bed_df)
# print(csv_df)
# print(tsv_df)
# print(json_df)
# print(text_df)

# print(vcf_df.columns.tolist())
# print(bed_df.columns.tolist())
# print(csv_df.columns.tolist())
# print(tsv_df.columns.tolist())
# print(json_df.columns.tolist())
# print(text_df.columns.tolist())