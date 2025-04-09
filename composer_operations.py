import csv
from typing import List
from models.composer import Composer

import os
os.makedirs("data", exist_ok=True)

FILE_PATH = "data/composers.csv"

def load_composers(include_deleted: bool = False) -> List[Composer]:
    composers = []
    try:
        with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:

                row["deleted"] = row.get("deleted", "False") == "True"
                composer = Composer(**row)
                if not include_deleted and composer.deleted:
                    continue
                composers.append(composer)
    except FileNotFoundError:
        print("Archivo no encontrado")
    return composers


def save_composers(composers: List[Composer]):
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "name", "birth_year", "nationality", "era", "deleted"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for composer in composers:
            writer.writerow(composer.dict())


def delete_composer_by_id(composer_id: int) -> bool:
    composers = load_composers(include_deleted=True)
    updated = False

    for composer in composers:
        if composer.id == composer_id and not composer.deleted:
            composer.deleted = True
            updated = True
            break

    if updated:
        save_composers(composers)
    return updated


def add_composer(new_composer: Composer) -> Composer:
    composers = load_composers(include_deleted=True)

    # Validar si ya existe un compositor con ese ID
    if any(c.id == new_composer.id for c in composers):
        raise ValueError("Ya existe un compositor con este ID")

    composers.append(new_composer)
    save_composers(composers)
    return new_composer