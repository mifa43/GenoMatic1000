import magic
import os
import pandas as pd



def load_dynamic_file(file_path: str):
    """
    Function used to detect file type (VCF, BED, CSV, TSV, JSON, lab report)
    """
    
    detect_file_type = magic.from_file(file_path, mime=True)
    print(f"Detected file type: {detect_file_type}")
    
load_dynamic_file("genomatic\genomatic1000_raw_input_samples\sample_pmp22_target.bed")