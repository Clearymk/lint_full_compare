from database import DataBase
import os
import csv


def init_callback_dict():
    callback_methods = dict()
    with open("callback_method") as r:
        for line in r.readlines():
            callback_methods[line.strip()] = [0, 0]
    return callback_methods


db = DataBase()
root_path = "test_file"
listener_header = ["listener", "lite count", "full count"]

for _ in db.query_download_mission():
    if _[2] == 1 and _[4] == 1 and _[9] == 0:
        lite_app_id = _[1]
        full_app_id = _[3]

        if not os.path.exists(os.path.join(root_path, lite_app_id)):
            # db.update_listener_compare_by_lite_app_id(lite_app_id, False)
            continue

        callback_methods = init_callback_dict()

        for decode_file in os.listdir(os.path.join(root_path, lite_app_id, lite_app_id)):
            if not decode_file.startswith("smali"):
                continue

            lite_smali_dir = os.path.join(root_path, lite_app_id, lite_app_id, decode_file)

            if not os.path.isdir(lite_smali_dir):
                continue

            for root, dirs, files in os.walk(lite_smali_dir):
                for file in files:
                    if not file.endswith(".smali"):
                        continue

                    try:
                        with open(os.path.join(root, file), encoding="utf8", errors="ignore") as r:
                            for line in r.readlines():
                                if not line.startswith(".method"):
                                    continue
                                for callback_method in callback_methods:
                                    if line.__contains__(callback_method):
                                        callback_methods[callback_method][0] += 1
                                        break
                    except FileNotFoundError as e:
                        print(e)

        for decode_file in os.listdir(os.path.join(root_path, lite_app_id, full_app_id)):
            if not decode_file.startswith("smali"):
                continue

            full_smali_dir = os.path.join(root_path, lite_app_id, full_app_id, decode_file)

            if not os.path.isdir(full_smali_dir):
                continue

            for root, dirs, files in os.walk(full_smali_dir):
                for file in files:
                    if not file.endswith(".smali"):
                        continue

                    try:
                        with open(os.path.join(root, file), encoding="utf8", errors="ignore") as r:
                            for line in r.readlines():
                                if not line.startswith(".method"):
                                    continue
                                for callback_method in callback_methods:
                                    if line.__contains__(callback_method):
                                        callback_methods[callback_method][1] += 1
                                        break
                    except FileNotFoundError as e:
                        print(e)
        with open(os.path.join(root_path, lite_app_id, "listener_compared.csv"), "w", newline="") as w:
            writer = csv.writer(w)
            writer.writerow(listener_header)
            for _ in callback_methods:
                writer.writerow([_, callback_methods[_][0], callback_methods[_][1]])
    print("-------")
