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

@app.get("/composers/{composer_id}", response_model=Composer)
def get_composer_by_id(composer_id: int):
    composers = load_composers()
    for composer in composers:
        if composer.id == composer_id:
            return composer
    raise HTTPException(status_code=404, detail="Compositor no encontrado")

@app.put("/composers/{composer_id}", response_model=Composer)
def update_composer(composer_id: int, updated_composer: Composer):
    composers = load_composers(include_deleted=True)
    for i, composer in enumerate(composers):
        if composer.id == composer_id and not composer.deleted:
            composers[i] = updated_composer
            save_composers(composers)
            return updated_composer
    raise HTTPException(status_code=404, detail="Compositor no encontrado o eliminado")


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

