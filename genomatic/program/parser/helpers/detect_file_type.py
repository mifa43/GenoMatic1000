from pathlib import Path

from models.supported_extensions import SupportedExtension

PROJECT_ROOT = Path(__file__).resolve().parents[4]
GENOMATIC_ROOT = PROJECT_ROOT / "genomatic"

SAMPLE_WORKING_DIR = GENOMATIC_ROOT / "genomatic1000_raw_input_samples"

def detect_file_type(file_path: str | Path) -> str | None:
    
    file_extension = Path(file_path).suffix.lower()
    
    try:
        return file_extension if file_extension in SupportedExtension(file_extension).value else None
    except ValueError:
        return None