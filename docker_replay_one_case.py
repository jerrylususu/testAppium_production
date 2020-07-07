from time import sleep
from pathlib import Path
import datetime
import traceback
# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install
from initialize_utils.find_free_port import find_free_port

import traceback
import sys

from analyseapk.AnalyseAPK import analyse_apk
from appiumdriver_processlog.appiumdriver.util.ProcessText import delete_text
from appiumdriver_processlog.appiumdriver.AppiumDriver import appium_driver
from appiumdriver_processlog.processlog.ProcessLogFile import generate_test

# replay_one_case: 只在某个特定 version 上 replay 某个特定 case
# 一般用于 debug，或尝试复现可能被检测到的异常
# 使用之前需要手动起 docker，然后把对应的端口填到下面
# 旧版本，现在主要使用 replay_one_case_multi

# 所有需要设定的值
# --- 开始
apk_path="/home/luzhirui/fdroid_1k6/com.mde.potdroid_80.apk"
case = "/home/luzhirui/jerrylu/testAppium/replay/output/testcase_com.mde.potdroid_80.apk-insted_ctest_1_test0.py"
img = "6.0"
adb_port = 37453
appium_port = 41109
# --- 结束

adb_exe_path="/home/luzhirui/jerrylu/adb/platform-tools/adb"
aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"
adb_connection_str="localhost:" + str(adb_port)  # this is generated at runtime
remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"


SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path)


APIlevel_androidversion = {
    '21': '5.0.1',
    '22': '5.1.1',
    '23': '6.0',
    '24': '7.0',
    '25': '7.1.1',
    '26': '8.0',
    '27': '8.1',
    '28': '9.0',
    '29': '10.0'
}


Android_version = APIlevel_androidversion[str(SDKversion)]
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = img
desired_caps['deviceName'] = 'emulator-5554' # This should be fine... They are all called `emulator-5554` internally inside container
desired_caps['appPackage'] = package
desired_caps['appActivity'] = main_activity
desired_caps['eventTimings'] = True
desired_caps['automationName'] = 'UIAutomator2'
desired_caps['autoGrantPermissions'] = True

write_name = f"{case}_{img}"
print("{*} running case: "+str(case))
with open(case, "r", encoding="utf8") as f:
    code = "\n".join(f.readlines())
print(f"[*] read code len={len(code)}, executing...")
exec(code)
print(remote_addr)

print(f"[*] test case load done, start replay...")

try:
    test_function(remote_addr=remote_addr, desired_caps=desired_caps, write_name=write_name)
except Exception as e:
    tb = traceback.format_exc()
    print(case)
    print(e)
    print(tb)

print("done")