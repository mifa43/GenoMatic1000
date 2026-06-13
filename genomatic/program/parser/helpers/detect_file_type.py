from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
GENOMATIC_ROOT = PROJECT_ROOT / "genomatic"

SAMPLE_WORKING_DIR = GENOMATIC_ROOT / "genomatic1000_raw_input_samples"

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".tsv",
    ".json",
    ".txt",
    ".vcf",
    ".bed",
}


def detect_file_type(file_path: str | Path) -> str | None:
    file_extension = Path(file_path).suffix.lower()
    return file_extension if file_extension in SUPPORTED_EXTENSIONS else None