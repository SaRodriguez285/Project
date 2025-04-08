import csv
from typing import List
from models.composer import Composer

import os
os.makedirs("data", exist_ok=True)

FILE_PATH = "data/composers.csv"

def load_composers() -> List[Composer]:
    composers = []
    try:
        with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                composers.append(Composer(**row))
    except FileNotFoundError:
        print("Archivo no encontrado")
    return composers


def save_composers(composers: List[Composer]):
    print("Guardando compositores")
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "name", "birth_year", "nationality", "era"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for composer in composers:
            print("Escribiendo:", composer.dict())
            writer.writerow(composer.dict())
