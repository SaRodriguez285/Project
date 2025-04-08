from fastapi import FastAPI
from composer_operations import load_composers, save_composers
from models.composer import Composer
from fastapi import HTTPException
from composer_operations import delete_composer_by_id

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

@app.delete("/delete-composer/{composer_id}")
def delete_composer(composer_id: int):
    success = delete_composer_by_id(composer_id)
    if success:
        return {"message": f"ID compositor {composer_id} marcado como eliminado."}
    else:
        raise HTTPException(status_code=404, detail=" Compositor no encontrado ")