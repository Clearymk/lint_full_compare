import json
import csv
import shutil

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
        continue

    full_path = os.path.join(root_path, app_pair_dir, full_app_id)
    lite_path = os.path.join(root_path, app_pair_dir, lite_app_id)

    create_if_not_exist(full_path)
    create_if_not_exist(lite_path)

    shutil.copy(lite_apk_path, simi_droid_path)
    shutil.copy(full_apk_path, simi_droid_path)

    print("using SimiDroid on {} and {}".format(lite_app_id, full_app_id))
    os.chdir(simi_droid_path)
    p = Popen("java -jar SimiDroid.jar {} {}".format(lite_app_id + ".apk",
                                                     full_app_id + ".apk"),
              shell=True, stdout=PIPE, stderr=STDOUT)
    p.wait()
    print(p.communicate())

    os.remove(os.path.join(simi_droid_path, lite_app_id + ".apk"))
    os.remove(os.path.join(simi_droid_path, full_app_id + ".apk"))

    result_file = "{}-{}.json".format(lite_app_id, full_app_id)

    with open(result_file) as r:
        component_data = json.load(r)

    component_conclusion = component_data['conclusion']
    component_verbose = component_data['verbose']

    conclusion_header = []
    conclusion_data = []

    for _ in component_conclusion:
        conclusion_header.append(_)
        conclusion_data.append(component_conclusion[_])

    with open(os.path.join(root_path, app_pair_dir, "component_stat.csv"), "a+", newline="") as w:
        writer = csv.writer(w)
        writer.writerow(conclusion_header)
        writer.writerow(conclusion_data)
        writer.writerow([])

    verbose_identical = component_verbose['identical']
    verbose_similar = component_verbose['similar']
    verbose_new = component_verbose['new']
    verbose_deleted = component_verbose['deleted']

    verbose_header = ["component_type", "component_name", "lite", "full", "is_similar"]
    verbose_data = []
    verbose_data_dict = {}

    for _ in verbose_identical:
        component_type, verbose_component = _.split(":")
        if component_type in verbose_data_dict:
            verbose_data_dict[component_type].append(verbose_component)
        else:
            verbose_data_dict[component_type] = [verbose_component]

    for component_type in verbose_data_dict:
        for component in verbose_data_dict[component_type]:
            verbose_data.append([component_type, component, 1, 1, 0])

    verbose_data_dict = {}

    for _ in verbose_similar:
        component_type, verbose_component = _.split(":")
        if component_type in verbose_data_dict:
            verbose_data_dict[component_type].append(verbose_component)
        else:
            verbose_data_dict[component_type] = [verbose_component]

    for component_type in verbose_data_dict:
        for component in verbose_data_dict[component_type]:
            verbose_data.append([component_type, component, 1, 1, 1])

    verbose_data_dict = {}

    for _ in verbose_new:
        component_type, verbose_component = _.split(":")
        if component_type in verbose_data_dict:
            verbose_data_dict[component_type].append(verbose_component)
        else:
            verbose_data_dict[component_type] = [verbose_component]

    for component_type in verbose_data_dict:
        for component in verbose_data_dict[component_type]:
            verbose_data.append([component_type, component, 1, 0, 0])

    verbose_data_dict = {}

    for _ in verbose_deleted:
        component_type, verbose_component = _.split(":")
        if component_type in verbose_data_dict:
            verbose_data_dict[component_type].append(verbose_component)
        else:
            verbose_data_dict[component_type] = [verbose_component]

    for component_type in verbose_data_dict:
        for component in verbose_data_dict[component_type]:
            verbose_data.append([component_type, component, 0, 1, 0])

    os.remove(result_file)

    with open(os.path.join(root_path, app_pair_dir, "component_stat.csv"), "a+", newline="") as w:
        writer = csv.writer(w)
        writer.writerow(verbose_header)
        for _ in verbose_data:
            writer.writerow(_)

    db.update_component_compare_by_lite_app_id(lite_app_id, True)