import os
import shutil

from database import DataBase

src_path = "C:\\Users\\10952\\Desktop\\download"
dest_path = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\download\\download_file"
db = DataBase()

for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith(".apk"):
            lite_app_id = root.split("\\")[-1]
            download_mission = db.query_download_mission_by_lite_app_id(lite_app_id)

            if not os.path.exists(os.path.join(dest_path, lite_app_id)):
                os.mkdir(os.path.join(dest_path, lite_app_id))

            shutil.copy(os.path.join(root, file), os.path.join(dest_path, lite_app_id))
            print("copy file " + os.path.join(root, file) + " to " + os.path.join(dest_path, lite_app_id))

            if file[:-4] == lite_app_id:
                db.update_lite_download_mission(1, lite_app_id)
            elif file[:-4] == download_mission[3]:
                db.update_full_download_mission(1, file[:-4])
            else:
                print("app id do not match " + os.path.join(root, file))
