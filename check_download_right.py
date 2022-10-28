import os
from database import DataBase
from zipfile import ZipFile

db = DataBase()

for root, dirs, files in os.walk("download/download_file"):
    for file in files:
        lite_app_id = root.split("\\")[1]
        full_app_id = db.query_download_mission_by_lite_app_id(lite_app_id)[3]
        if file.endswith(".apk"):
            lite_app_id = root.split("\\")[1]
            # print(lite_app_id)
            full_app_id = db.query_download_mission_by_lite_app_id(lite_app_id)[3]
            result = os.popen("java -jar extract_manifest.jar \"" + os.path.join(root, file) + "\"").read()
            if len(result.split(":")) == 2:
                app_id = result.split(":")[1].strip()
                if app_id != lite_app_id and app_id != full_app_id:
                    print(os.path.join(root, file), app_id)
            else:
                print(os.path.join(root, file))
        elif file.endswith(".xapk"):
            flag = False
            with ZipFile(os.path.join(root, file), "r") as archive:
                for _ in archive.filelist:
                    filename = _.filename[:-4]
                    if filename == lite_app_id or filename == full_app_id:
                        flag = True
                        break
            if not flag:
                print(lite_app_id)
