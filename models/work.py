from pydantic import BaseModel
from typing import List

class Work(BaseModel):
    id: int
    composer_id: int
    title: str
    year_composed: int
    genre: str
    instruments: List[str] = []
    deleted: bool = False
