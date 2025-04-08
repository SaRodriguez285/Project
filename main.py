from fastapi import FastAPI
from composer_operations import load_composers, save_composers
from models.composer import Composer

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenido a mi proyecto: evolución de la musica"}

@app.get("/test-composer")
def test_composer():

    new_composer = Composer(
        id=1,
        name="Johann Sebastian Bach",
        birth_year=1685,
        nationality="German",
        era="Baroque"
    )

    save_composers([new_composer])
    composers = load_composers()
    return composers
