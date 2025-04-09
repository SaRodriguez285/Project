from pydantic import BaseModel
from typing import Optional

class Work(BaseModel):
    id: int
    composer_id: int
    title: str
    year_composed: int
    genre: str
    deleted: Optional[bool] = False
