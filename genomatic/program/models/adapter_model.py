from pydantic import BaseModel

class AdapterModel(BaseModel):
    pass

class CSVAdapterModel(AdapterModel):
    sample_id: str
    assembly: str
    chromosome: str
    pos_start: int
    pos_end: int
    copy_number: int
    call: str
    gene: str
    caller: str
    quality: float