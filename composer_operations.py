import csv
from typing import List
from Models.composer import Composer

FILE_PATH = "data/composers.csv"

def load_composers() -> List[Composer]:
    composers = []
    try:
        with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                composers.append(Composer(**row))
    except FileNotFoundError:
        pass
    return composers


def save_composers(composers: List[Composer]):
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "name", "birth_year", "nationality", "era"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for composer in composers:
            writer.writerow(composer.dict())