from enum import Enum
from pydantic import BaseModel, Field

class SupportedExtension(str, Enum):
    CSV = ".csv"
    TSV = ".tsv"
    JSON = ".json"
    TXT = ".txt"
    VCF = ".vcf"
    BED = ".bed"

# Just some exemple
# class FileModel(BaseModel):
#     filename: str
#     extension: SupportedExtension
