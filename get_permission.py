import re
import subprocess
import os

os.environ["ANDROID_HOME"] = "D:\\AndroidSDK"


class AppPermission:
    def __init__(self, apk_path):
        self.apkPath = apk_path
        self.aapt_path = self.get_aapt()
        self.permissions = set()

    @staticmethod
    def get_aapt():
        if "ANDROID_HOME" in os.environ:
            root_dir = os.path.join(os.environ["ANDROID_HOME"], "build-tools")
            for path, subdir, files in os.walk(root_dir):
                if "aapt.exe" in files:
                    return os.path.join(path, "aapt.exe")
        else:
            return "ANDROID_HOME not exist"

    def get_app_permission(self):
        p = subprocess.Popen(self.aapt_path + " dump permissions %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        match = re.compile(": name='(\S+)'").findall(output.decode())
        if match is not None:
            for permission in match:
                self.permissions.add(permission)


if __name__ == '__main__':
    apkPath = "test_file/cn.wps.moffice_eng.apk"
    app_permission = AppPermission(apkPath)
    app_permission.get_app_permission()
