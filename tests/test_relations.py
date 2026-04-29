from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenido" in response.json()["message"]

def test_get_all_composers():
    response = client.get("/composers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_composer_by_id():
    response = client.get("/composers/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Johann Sebastian Bach"

def test_filter_composers():
    response = client.get("/composers/filter?era=Classical")
    assert response.status_code == 200
    for composer in response.json():
        assert composer["era"] == "Classical"

def test_composer_instruments():
    response = client.get("/composers/2/instruments")  # Mozart
    assert response.status_code == 200
    instruments = response.json()
    assert "Violin" in instruments
    assert "Piano" in instruments
    assert "Trumpet" in instruments

def test_composer_not_found():
    response = client.get("/composers/999/instruments")
    assert response.status_code == 404

def test_get_all_works():
    response = client.get("/works")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_works_by_composer():
    response = client.get("/works/by-composer/2")  # Mozart
    assert response.status_code == 200
    for work in response.json():
        assert work["composer_id"] == 2

def test_work_instruments():
    response = client.get("/works/4/instruments")  # Symphony No. 40
    assert response.status_code == 200
    instruments = response.json()
    assert instruments == ["Violin", "Piano", "Trumpet"]

def test_work_not_found():
    response = client.get("/works/999/instruments")
    assert response.status_code == 404

def test_get_all_instruments():
    response = client.get("/instruments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_instrument_by_id():
    response = client.get("/instruments/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Violin"

def test_instrument_not_found():
    response = client.get("/instruments/999")
    assert response.status_code == 404