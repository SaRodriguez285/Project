from fastapi import FastAPI
from composer_operations import load_composers, save_composers
from Models.composer import Composer

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenido mi proyecto: La evolución musical"}

@app.get("/test-composer")
def test_composer():
    new_composer = Composer(
        id=1,
        name="Johann Sebastian Bach",
        birth_year=1685,
        nationality="German",
        era="Baroque"
    )

    #Guardar Lista del Compo
    save_composers([new_composer])

    #Cargar los Comps
    composers = load_composers()

    return composers

