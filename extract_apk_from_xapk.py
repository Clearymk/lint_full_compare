import os
from database import DataBase
from zipfile import ZipFile

db = DataBase()
PATH = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\download\\download_file"

for root, dirs, files in os.walk("download/download_file"):
    for file in files:
        if file.endswith(".xapk"):
            lite_app_id = root.split("\\")[1]
            full_app_id = db.query_download_mission_by_lite_app_id(lite_app_id)[3]
            with ZipFile(os.path.join(root, file), "r") as archive:
                for _ in archive.filelist:
                    filename = _.filename[:-4]
                    if filename == lite_app_id or filename == full_app_id:
                        archive.extract(_, os.path.join(PATH, lite_app_id))
                        print("extract " + _.filename + " to " + os.path.join(PATH, lite_app_id))
                        break
