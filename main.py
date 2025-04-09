from fastapi import FastAPI, HTTPException
from typing import List
from composer_operations import (load_composers, save_composers, delete_composer_by_id, add_composer)
from models.composer import Composer

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenido a mi proyecto: evolución de la música"}

@app.get("/init-bach")
def init_bach():
    bach = Composer(
        id=1,
        name="Johann Sebastian Bach",
        birth_year=1685,
        nationality="German",
        era="Baroque"
    )
    save_composers([bach])
    return {"message": "Compositor Bach registrado", "composer": bach}

@app.delete("/delete-composer/{composer_id}")
def delete_composer(composer_id: int):
    success = delete_composer_by_id(composer_id)
    if success:
        return {"message": f"ID compositor {composer_id} marcado como eliminado."}
    else:
        raise HTTPException(status_code=404, detail="Compositor no encontrado")

@app.post("/composers")
def create_composer(composer: Composer):
    try:
        added = add_composer(composer)
        return {"message": "Compositor añadido exitosamente", "composer": added}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/composers", response_model=List[Composer])
def get_all_composers():
    return load_composers()
