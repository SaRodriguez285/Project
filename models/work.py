from pydantic import BaseModel
from typing import Optional, List


class Work(BaseModel):
    id: int
    composer_id: int
    title: str
    year_composed: int
    genre: str
    instruments: List[int] = []   # IDs de instrumentos que suenan
    deleted: bool = False