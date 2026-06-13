import pandas as pd
import numpy as np


class RawParser:
    
    def __init__(
        self,
        file_path: str
    ):
        self.file_path = file_path
    
    def _read_file(self) -> pd.DataFrame:
        pass
    
    def parse(self) -> pd.DataFrame:
        pass
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass