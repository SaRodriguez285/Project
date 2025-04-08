from pydantic import BaseModel
from typing import Optional

class Composer(BaseModel):
    id: int
    name: str
    birth_year: int
    nationality: str
    era: str  # Baroque, Classical, Romantic