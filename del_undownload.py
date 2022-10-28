import csv
from database import DataBase

db = DataBase()
d_count = 0
data = []
tail_data = []

with open("data/full_app_with_size_category.csv", errors="ignore") as r:
    reader = csv.reader(r)
    count = -1
    for _ in reader:
        lite_app_id = _[1]
        count += 1
        if count == 0:
            data.append(_)
            count += 1
            continue

        if count >= 299:
            data.append(_)
            continue

        download_mission = db.query_download_mission_by_lite_app_id(lite_app_id)

        if download_mission[5] != 1 or download_mission[6] != 1:
            d_count += 1
            print(download_mission)
            if download_mission[2] == 1:
                tail_data.append([_[0], _[1], _[2], 0, _[4], _[5]])
        else:
            data.append(_)
with open("test.csv", "w", encoding="utf8", errors="ignore", newline="") as w:
    writer = csv.writer(w)
    for _ in data:
        writer.writerow(_)

    for _ in tail_data:
        writer.writerow(_)
