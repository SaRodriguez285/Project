from pydantic import BaseModel
from typing import Optional, List


class Composer(BaseModel):
    id: int
    name: str
    birth_year: int
    nationality: str
    era: str
    instruments: List[int] = []   # IDs de instrumentos asociados
    deleted: bool = False