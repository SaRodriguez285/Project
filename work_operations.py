import csv
from typing import List
from models.work import Work

import os
os.makedirs("data", exist_ok=True)

FILE_PATH = "data/works.csv"

def load_works(include_deleted: bool = False) -> List[Work]:
    works = []
    try:
        with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["id"] = int(row["id"])
                row["composer_id"] = int(row["composer_id"])
                row["year_composed"] = int(row["year_composed"])
                row["deleted"] = row.get("deleted", "False") == "True"
                work = Work(**row)
                if not include_deleted and work.deleted:
                    continue
                works.append(work)
    except FileNotFoundError:
        print("Archivo de obras no encontrado")
    return works

def save_works(works: List[Work]):
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "composer_id", "title", "year_composed", "genre", "deleted"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for work in works:
            writer.writerow(work.dict())

def add_work(new_work: Work) -> Work:
    works = load_works(include_deleted=True)
    if any(w.id == new_work.id for w in works):
        raise ValueError("Ya existe una obra con este ID")
    works.append(new_work)
    save_works(works)
    return new_work

def delete_work_by_id(work_id: int) -> bool:
    works = load_works(include_deleted=True)
    updated = False

    for work in works:
        if work.id == work_id and not work.deleted:
            work.deleted = True
            updated = True
            break

    if updated:
        save_works(works)
    return updated