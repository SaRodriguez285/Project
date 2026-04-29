from pydantic import BaseModel
from typing import List

class Instrument(BaseModel):
    id: int
    name: str              # Ejemplo: "Violin", "Piano", "Organ"
    family: str            # Ejemplo: "Strings", "Keyboard", "Brass"
    deleted: bool = False
