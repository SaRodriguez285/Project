from pydantic import BaseModel
from typing import Optional

class Composer(BaseModel):
    id: int
    name: str
    birth_year: int
    nationality: str
    era: str  # Baroque, Classical, Romantic
    deleted: Optional[bool] = False
    
class Work(BaseModel):
    id: int
    composer_id: int
    title: str
    year_composed: int
    genre: str  #Orchestral, Choral, Opera  .
    deleted: Optional[bool] = False
