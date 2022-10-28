import os
import csv
from file import File
from util import sha256sum, create_if_not_exist
from database import DataBase
from subprocess import Popen, PIPE, STDOUT

root_path = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\download\\download_file"
db = DataBase()


for app_pair_dir in os.listdir(root_path):
    download_mission = db.query_download_mission_by_lite_app_id(app_pair_dir)
    lite_app_id = download_mission[1]
    full_app_id = download_mission[3]

    if download_mission[5] != 0 or download_mission[2] != 1 or download_mission[4] != 1:
        continue

    lite_apk_path = os.path.join(root_path, app_pair_dir, lite_app_id + ".apk")
    full_apk_path = os.path.join(root_path, app_pair_dir, full_app_id + ".apk")

    if not os.path.exists(lite_apk_path) or not os.path.exists(full_apk_path):
        print("do not find app pair on path " + os.path.join(root_path, app_pair_dir))

    full_files = {}
    lite_files = {}

    full_path = os.path.join(root_path, app_pair_dir, full_app_id)
    lite_path = os.path.join(root_path, app_pair_dir, lite_app_id)

    create_if_not_exist(full_path)
    create_if_not_exist(lite_path)

    print("using apktool on {}".format('download/download_file/' + app_pair_dir + "/" + lite_app_id + ".apk"))
    p = Popen("apktool d {} -o \"{}\" -f".format('download/download_file/' + app_pair_dir + "/" + lite_app_id + ".apk",
                                                 lite_path),
              shell=True, stdout=PIPE, stderr=STDOUT)
    p.wait()

    print("using apktool on {}".format('download/download_file/' + app_pair_dir + "/" + full_app_id + ".apk"))
    p = Popen("apktool d {} -o \"{}\" -f".format('download/download_file/' + app_pair_dir + "/" + full_app_id + ".apk",
                                                 full_path),
              shell=True, stdout=PIPE, stderr=STDOUT)
    p.wait()

    for root, dirs, files in os.walk(full_path):
        for name in files:
            try:
                full_file_path = os.path.join(root, name).replace(full_path, "")
                full_file_size = os.path.getsize(os.path.join(root, name))
                full_file_hash = sha256sum(os.path.join(root, name))
                full_file = File(full_file_path, full_file_size, full_file_hash)
                full_files[full_file_path] = full_file
            except FileNotFoundError as e:
                print(e, os.path.join(root, name))

    for root, dirs, files in os.walk(lite_path):
        for name in files:
            try:
                lite_file_path = os.path.join(root, name).replace(lite_path, "")
                lite_file_size = os.path.getsize(os.path.join(root, name))
                lite_file_hash = sha256sum(os.path.join(root, name))
                lite_file = File(lite_file_path, lite_file_size, lite_file_hash)
                lite_files[lite_file_path] = lite_file
            except FileNotFoundError as e:
                print(e, os.path.join(root, name))

    same_file_same_hash = []
    same_file_different_hash = []
    full_unique_file = []
    lite_unique_file = []

    for full_file_path in full_files:
        full_file = full_files[full_file_path]

        if full_file_path not in lite_files:
            full_unique_file.append([full_file.file_path, full_file.size, full_file.file_hash])
            continue

        lite_file = lite_files.pop(full_file_path)

        if full_file.compare(lite_file):
            same_file_same_hash.append([full_file.file_path, 1, 1,
                                        lite_file.file_hash, full_file.file_hash, 1,
                                        lite_file.size, full_file.size, 1])
        else:
            same_size = 0
            if full_file.size == lite_file.size:
                same_size = 1
            same_file_different_hash.append([full_file.file_path, 1, 1,
                                             lite_file.file_hash, full_file.file_hash, 0,
                                             lite_file.size, full_file.size, same_size])

    for lite_file_path in lite_files:
        lite_file = lite_files[lite_file_path]

        if lite_file.file_hash not in full_files:
            lite_unique_file.append([lite_file.file_path, lite_file.size, lite_file.file_hash])

    file_stat_header = ["File Path",
                        "Lite", "Full",
                        "Lite Hash", "Full Hash", "Same Hash",
                        "Lite Size", "Full Size", "Same Size"]

    with open(os.path.join(root_path, app_pair_dir, "file_stat.csv"), "w", newline="") as w:
        writer = csv.writer(w)

        writer.writerow(file_stat_header)

        for _ in same_file_same_hash:
            writer.writerow(_)

        for _ in same_file_different_hash:
            writer.writerow(_)

        for _ in lite_unique_file:
            writer.writerow([_[0], 1, 0, _[2], "-", 0, _[1], "-", 0])

        for _ in full_unique_file:
            writer.writerow([_[0], 0, 1, "-", _[2], 0, "-", _[1], 0])

    db.update_compare_by_lite_app_id(lite_app_id, True)
