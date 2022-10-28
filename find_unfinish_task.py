from database import DataBase

db = DataBase()

count = 0
for _ in db.query_download_mission():
    if _[2] == 0 or _[4] == 0:
        count += 1
        # print("lite do not download", _[1])
        # print(_[1])
    # if _[4] == 0:
    #     count += 1
    #     print("full do not download", _[1], _[3])
        # print(_[3])

print(count)
