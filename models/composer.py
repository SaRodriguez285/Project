from pydantic import BaseModel
from typing import List

class Composer(BaseModel):
    id: int
    name: str
    birth_year: int
    nationality: str
    era: str
    instruments: List[str] = [] 
    deleted: bool = False
