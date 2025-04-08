from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from models import Pet, PetResponse
from typing import List

app = FastAPI()

pets: List[Pet] =[
    Pet(name="Chispas", breed="Siames", birth=2022, kind="cat"),
    Pet(name="Pascal", breed="Persa", birth=2021, kind="cat"),
    Pet(name="Elefante", breed="Gran Danés", birth=2023, kind="dog"),
]

# Endpoint para crear una nueva mascota
@app.post("/pet", response_model=Pet)
async def create_pet(pet: Pet):
    pets.append(pet)
    return pet

# Endpoint para mostrar todas las mascotas (solo name y kind)
@app.get("/allpets", response_model=List[PetResponse])
async def show_all_pets():
    return [PetResponse(name=pet.name, kind=pet.kind) for pet in pets]

# Raíz de la API
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Saludo personalizado
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Manejador de errores personalizado
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Carambas, algo falló"},
    )

# Ruta que lanza un error (para pruebas)
@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)
