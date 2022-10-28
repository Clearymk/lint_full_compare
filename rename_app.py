import os
from database import DataBase

root_path = "D:\\PyCharm 2021.2.1\\code\\lint_full_compare\\download\\download_file"
db = DataBase()

for root, dirs, files in os.walk(root_path):
    for file in files:
        lite_app_id = root.split("\\")[-1]
        download_mission = db.query_download_mission_by_lite_app_id(lite_app_id)
        full_app_id = download_mission[3]
        if download_mission[2] != 1 or download_mission[4] != 1:
            continue

        if file.endswith(".apk"):
            result = os.popen("java -jar extract_manifest.jar \"" + os.path.join(root, file) + "\"").read()
            if len(result.split(":")) == 2:
                app_id = result.split(":")[1].strip()
                if app_id in file:
                    continue
                if app_id == lite_app_id or app_id == full_app_id:
                    pass
                    os.rename(os.path.join(root_path, lite_app_id, file),
                              os.path.join(root_path, lite_app_id, app_id + ".apk"))
                    print("rename file " + os.path.join(root_path, lite_app_id, file)
                          + " to " + os.path.join(root_path, lite_app_id, app_id + ".apk"))
                else:
                    print("app id is not same on file " + os.path.join(lite_app_id, file))
            else:
                print("error on the file " + os.path.join(lite_app_id, file))
