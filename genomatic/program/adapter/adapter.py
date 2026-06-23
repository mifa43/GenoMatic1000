import pandas as pd

from models.supported_extensions import SupportedExtension

class Adapter:
    
    def __init__(self):
        pass
    
    def adopt(self, df: pd.DataFrame, target_format: str) -> pd.DataFrame:
        """Adoopts `df` and formats it to the `target_format` if not specified, returns None.

        Args:
            df (pd.DataFrame): DataFrame to be adopted.\
            target_format (str): Target format for the DataFrame if supported (see `SupportedExtension`).

        Returns:
            pd.DataFrame: Converted DataFrame in the target format if supported, otherwise None.
        """
        if target_format == SupportedExtension.BED.value:
            return self._to_bed(df)
    
    def _to_bed(self, df: pd.DataFrame) -> pd.DataFrame:
        """Converts a DataFrame to BED format.

        Args:
            df (pd.DataFrame): DataFrame to be converted.

        Returns:
            pd.DataFrame: Converted DataFrame in BED format.
        """
        
        # Read about BED format in file_formats_and_standards.md
        REQUIRED_BED_COLUMNS = ["chrom", "chromStart", "chromEnd"]
        OPTIONAL_BED_COLUMNS = ["name", "score", "strand"]