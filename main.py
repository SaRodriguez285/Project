from fastapi import FastAPI, HTTPException, Path
from typing import List
from operations.composer_operations import (load_composers, save_composers, delete_composer_by_id, add_composer)
from operations.work_operations import (load_works, delete_work_by_id, add_work, save_works)
from operations.instrument_operations import (load_instruments, save_instruments, add_instrument, delete_instrument_by_id)
from models.composer import Composer
from models.work import Work
from models.instrument import Instrument

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

@app.post("/composers", response_model=Composer)
def create_composer(composer: Composer):
    try:
        return add_composer(composer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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

@app.get("/composers", response_model=List[Composer])
def get_all_composers():
    return load_composers()

# WORKS

@app.get("/works", response_model=List[Work])
def get_all_works():
    return load_works()

@app.get("/works/by-composer/{composer_id}", response_model=List[Work])
def get_works_by_composer(composer_id: int = Path(..., description="ID del compositor")):
    works = load_works()
    filtered_works = [work for work in works if work.composer_id == composer_id]
    if not filtered_works:
        raise HTTPException(status_code=404, detail="No se encontraron obras para este compositor.")
    return filtered_works

@app.post("/works", response_model=Work)
def create_work(work: Work):
    try:
        return add_work(work)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/works/{work_id}", response_model=Work)
def update_work(work_id: int, updated_work: Work):
    works = load_works(include_deleted=True)
    for i, work in enumerate(works):
        if work.id == work_id and not work.deleted:
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

# INSTRUMENTS

@app.get("/instruments", response_model=List[Instrument])
def get_all_instruments():
    return load_instruments()

@app.get("/instruments/{instrument_id}", response_model=Instrument)
def get_instrument_by_id(instrument_id: int):
    instruments = load_instruments()
    for instrument in instruments:
        if instrument.id == instrument_id:
            return instrument
    raise HTTPException(status_code=404, detail="Instrumento no encontrado")

@app.post("/instruments", response_model=Instrument)
def create_instrument(instrument: Instrument):
    try:
        return add_instrument(instrument)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/instruments/{instrument_id}", response_model=Instrument)
def update_instrument(instrument_id: int, updated_instrument: Instrument):
    instruments = load_instruments(include_deleted=True)
    for i, instrument in enumerate(instruments):
        if instrument.id == instrument_id and not instrument.deleted:
            instruments[i] = updated_instrument
            save_instruments(instruments)
            return updated_instrument
    raise HTTPException(status_code=404, detail="Instrumento no encontrado o eliminado")

@app.delete("/instruments/{instrument_id}")
def delete_instrument(instrument_id: int):
    success = delete_instrument_by_id(instrument_id)
    if success:
        return {"message": f"Instrumento {instrument_id} marcado como eliminado."}
    else:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")