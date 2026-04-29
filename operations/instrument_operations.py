import csv
import os
from typing import List
from models.instrument import Instrument

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

FILE_PATH = os.path.join(DATA_DIR, "instruments.csv")

def load_instruments(include_deleted: bool = False) -> List[Instrument]:
    instruments = []
    try:
        with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["deleted"] = row.get("deleted", "False") == "True"
                instrument = Instrument(**row)
                if not include_deleted and instrument.deleted:
                    continue
                instruments.append(instrument)
    except FileNotFoundError:
        print("Archivo de instrumentos no encontrado")
    return instruments

def save_instruments(instruments: List[Instrument]):
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "name", "family", "deleted"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for instrument in instruments:
            writer.writerow(instrument.dict())

def add_instrument(new_instrument: Instrument) -> Instrument:
    instruments = load_instruments(include_deleted=True)
    if any(i.id == new_instrument.id for i in instruments):
        raise ValueError("Ya existe un instrumento con este ID")
    instruments.append(new_instrument)
    save_instruments(instruments)
    return new_instrument

def delete_instrument_by_id(instrument_id: int) -> bool:
    instruments = load_instruments(include_deleted=True)
    updated = False
    for instrument in instruments:
        if instrument.id == instrument_id and not instrument.deleted:
            instrument.deleted = True
            updated = True
            break
    if updated:
        save_instruments(instruments)
    return updated
