from fastapi import FastAPI, HTTPException, Path
from typing import List
from composer_operations import (load_composers, save_composers, delete_composer_by_id, add_composer)
from work_operations import (load_works, save_works, delete_work_by_id, add_work)
from models.composer import Composer
from models.work import Work

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenido a mi proyecto: evolución de la música"}

# ENDPOINTS COMPOSER

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

@app.get("/composers/filter", response_model=List[Composer])
def filter_composers(era: str = None, nationality: str = None):
    composers = load_composers()
    if era:
        composers = [c for c in composers if c.era.lower() == era.lower()]
    if nationality:
        composers = [c for c in composers if c.nationality.lower() == nationality.lower()]
    return composers

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

# ENDPOINTS WORK

@app.post("/works")
def create_work(work: Work):
    try:
        added = add_work(work)
        return {"message": "Obra añadida exitosamente", "work": added}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/works", response_model=List[Work])
def get_all_works():
    return load_works()

@app.delete("/delete-work/{work_id}")
def delete_work(work_id: int):
    success = delete_work_by_id(work_id)
    if success:
        return {"message": f"ID obra {work_id} marcada como eliminada."}
    else:
        raise HTTPException(status_code=404, detail="Obra no encontrada")

@app.get("/works/by-composer/{composer_id}", response_model=List[Work])
def get_works_by_composer(composer_id: int = Path(..., description="ID del compositor")):
    works = load_works()
    filtered_works = [work for work in works if work.composer_id == composer_id]
    if not filtered_works:
        raise HTTPException(status_code=404, detail="No se encontraron obras para este compositor.")
    return filtered_works
