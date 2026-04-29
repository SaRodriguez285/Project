from fastapi import FastAPI, HTTPException, Path
from typing import List
from operations.composer_operations import (load_composers, save_composers, delete_composer_by_id, add_composer)
from operations.work_operations import (load_works, delete_work_by_id, add_work, save_works)
from models.composer import Composer
from models.work import Work

app = FastAPI(title="Music Catalog API")

@app.get("/")
def root():
    return {"message": "Bienvenido a mi proyecto: evolución de la música"}

# COMPOSERS

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

@app.delete("/composers/{composer_id}")
def delete_composer(composer_id: int):
    success = delete_composer_by_id(composer_id)
    if success:
        return {"message": f"ID compositor {composer_id} marcado como eliminado."}
    else:
        raise HTTPException(status_code=404, detail="Compositor no encontrado")

@app.post("/composers", response_model=Composer)
def create_composer(composer: Composer):
    try:
        return add_composer(composer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/composers", response_model=List[Composer])
def get_all_composers():
    return load_composers()

# WORKS

@app.post("/works", response_model=Work)
def create_work(work: Work):
    try:
        return add_work(work)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/works", response_model=List[Work])
def get_all_works():
    return load_works()

@app.put("/works/{work_id}", response_model=Work)
def update_work(work_id: int, updated_work: Work):
    works = load_works(include_deleted=True)
    for i, work in enumerate(works):
        if work.id == work_id and not work.deleted:
            # Reemplazar el registro con el nuevo objeto enviado
            works[i] = updated_work
            save_works(works)
            return updated_work
    raise HTTPException(status_code=404, detail="Obra no encontrada o eliminada")


@app.delete("/works/{work_id}")
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
