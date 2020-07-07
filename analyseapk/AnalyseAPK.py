import re

import apkutils
import os
from time import sleep
from datetime import datetime
import subprocess

def analyse_apk(apk_path, aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"):
    targetSdk, package, main_activity, minSdk = None, "UNKNOWN", "UNKNOWN", None
    try:
        return_str =subprocess.check_output([aapt_path,"dump","badging", apk_path])
        decode_li = return_str.decode("utf8").split("\n")
        package = decode_li[0].replace("'","").split(" ")[1].replace("name=","")
        for line in decode_li:
            if line.startswith("sdkVersion:"):
                minSdk = int(line.replace("'","").split(":")[1])
            if line.startswith("targetSdkVersion:"):
                targetSdk = int(line.replace("'","").split(":")[1])
            if line.startswith("launchable-activity"):
                main_activity = line.split(" ")[1].replace("'","").replace("name=","")
    except Exception as e:
        print(e)
        with open("analyze_log.log", "a") as f:
            f.write(f"{apk_path}\n{str(e)}\n")
    finally:
        return targetSdk, package, main_activity, minSdk

# def analyse_apk(path):
#     apk = apkutils.APK(path)

#     manifest_string = apk.get_mini_mani()
#     main_activity = None
#     ptn = r'<activity .*?android:name="([^"]*?)"[^<>]*?>.*?<action android:name="android.intent.action.MAIN">.*?</activity>'
#     result = re.search(ptn, manifest_string)
#     if result:
#         main_activity = result.groups()[0]

#     manifest = apk.get_manifest()
#     package = apk.get_manifest()['@package']
#     uses_sdk = manifest['uses-sdk']
#     minSdk = uses_sdk.get('@android:minSdkVersion', '')
#     targetSdk = uses_sdk.get('@android:targetSdkVersion', '')

#     return targetSdk, package, main_activity, minSdk