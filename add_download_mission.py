import csv
from database import DataBase

db = DataBase()

download_task = []
with open("data/full_app_with_size_category.csv", encoding="utf8", errors="ignore") as r:
    reader = csv.reader(r)
    for _ in reader:
        if _[3] != "1":
            continue
        download_task.append([_[1], _[6]])

for _ in download_task:
    db.insert_download_mission(_[0], _[1])
