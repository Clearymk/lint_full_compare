import os
from database import DataBase
from get_permission import AppPermission
import csv

root_path = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\download\\download_file"
db = DataBase()

for app_pair_dir in os.listdir(root_path):
    download_mission = db.query_download_mission_by_lite_app_id(app_pair_dir)
    lite_app_id = download_mission[1]
    full_app_id = download_mission[3]

    if download_mission[6] != 0 or download_mission[2] != 1 or download_mission[4] != 1:
        continue

    lite_apk_path = os.path.join(root_path, app_pair_dir, lite_app_id + ".apk")
    full_apk_path = os.path.join(root_path, app_pair_dir, full_app_id + ".apk")

    if not os.path.exists(lite_apk_path) or not os.path.exists(full_apk_path):
        print("do not find app pair on path " + os.path.join(root_path, app_pair_dir))

    full_app_permission = AppPermission("download/download_file/" + lite_app_id + "/" + full_app_id + ".apk")
    full_app_permission.get_app_permission()
    lite_app_permission = AppPermission("download/download_file/" + lite_app_id + "/" + lite_app_id + ".apk")
    lite_app_permission.get_app_permission()

    permission_stat_header = ["Permission", "Lite", "Full"]
    with open(os.path.join(root_path, app_pair_dir, "permission_stat.csv"), "w", newline="") as w:
        writer = csv.writer(w)

        writer.writerow(permission_stat_header)

        for _ in full_app_permission.permissions & lite_app_permission.permissions:
            writer.writerow([_, 1, 1])

        for _ in full_app_permission.permissions - lite_app_permission.permissions:
            writer.writerow([_, 0, 1])

        for _ in lite_app_permission.permissions - full_app_permission.permissions:
            writer.writerow([_, 1, 0])
    db.update_permission_compare_by_lite_app_id(lite_app_id, True)
