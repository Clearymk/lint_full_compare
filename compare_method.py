import json
import csv
import shutil
import time

from database import DataBase
from util import create_if_not_exist
import os
from subprocess import Popen, PIPE, STDOUT

root_path = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\download\\download_file"
simi_droid_path = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\code_compare\\SimiDroid\\artefacts"
db = DataBase()

for app_pair_dir in os.listdir(root_path):
    download_mission = db.query_download_mission_by_lite_app_id(app_pair_dir)
    lite_app_id = download_mission[1]
    full_app_id = download_mission[3]

    if download_mission[7] != 0 or download_mission[2] != 1 or download_mission[4] != 1:
        continue

    lite_apk_path = os.path.join(root_path, app_pair_dir, lite_app_id + ".apk")
    full_apk_path = os.path.join(root_path, app_pair_dir, full_app_id + ".apk")

    if not os.path.exists(lite_apk_path) or not os.path.exists(full_apk_path):
        print("do not find app pair on path " + os.path.join(root_path, app_pair_dir))
        print("----------")
        continue

    full_path = os.path.join(root_path, app_pair_dir, full_app_id)
    lite_path = os.path.join(root_path, app_pair_dir, lite_app_id)

    create_if_not_exist(full_path)
    create_if_not_exist(lite_path)

    shutil.copy(lite_apk_path, simi_droid_path)
    shutil.copy(full_apk_path, simi_droid_path)

    print("using SimiDroid on {} and {}".format(lite_app_id, full_app_id))
    os.chdir(simi_droid_path)

    p = Popen(['java', '-jar', 'SimiDroid.jar', lite_app_id + ".apk", full_app_id + ".apk"], stdout=PIPE, stderr=PIPE)
    p.wait()

    time.sleep(1)
    os.remove(os.path.join(simi_droid_path, lite_app_id + ".apk"))
    os.remove(os.path.join(simi_droid_path, full_app_id + ".apk"))

    if os.path.exists(os.path.join(root_path, app_pair_dir, "component_stat.csv")):
        os.remove(os.path.join(root_path, app_pair_dir, "component_stat.csv"))

    result_file = "{}-{}.json".format(lite_app_id, full_app_id)

    with open(result_file, encoding="utf8", errors="ignore") as r:
        method_data = json.load(r)

    method_conclusion = method_data['conclusion']
    method_verbose = method_data['verbose']

    method_header = []
    method_data = []

    for _ in method_conclusion:
        method_header.append(_)
        method_data.append(method_conclusion[_])

    with open(os.path.join(root_path, app_pair_dir, "method_stat.csv"), "a+", newline="") as w:
        writer = csv.writer(w)
        writer.writerow(method_header)
        writer.writerow(method_data)
        writer.writerow([])

    verbose_identical = method_verbose['identical']
    verbose_similar = method_verbose['similar']
    verbose_new = method_verbose['new']
    verbose_deleted = method_verbose['deleted']

    verbose_header = ["method_signature", "lite", "full", "is_similar"]
    verbose_data = []

    for _ in verbose_identical:
        verbose_data.append([_, 1, 1, 0])

    for _ in verbose_similar:
        verbose_data.append([_, 1, 1, 1])

    for _ in verbose_new:
        verbose_data.append([_, 1, 0, 0])

    for _ in verbose_deleted:
        verbose_data.append([_, 0, 1, 0])

    with open(os.path.join(root_path, app_pair_dir, "method_stat.csv"), "a+", newline="") as w:
        writer = csv.writer(w)
        writer.writerow(verbose_header)
        for _ in verbose_data:
            writer.writerow(_)

    os.remove(result_file)
    db.update_method_compare_by_lite_app_id(lite_app_id, True)
    print("----------")
