from time import sleep
import traceback
import sys

from analyseapk.AnalyseAPK import analyse_apk
from appiumdriver_processlog.appiumdriver.util.ProcessText import delete_text
from appiumdriver_processlog.appiumdriver.AppiumDriver import appium_driver
from appiumdriver_processlog.processlog.ProcessLogFile import generate_test

# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install
from initialize_utils.find_free_port import find_free_port

# GenerateTests - 对单个 apk 生成测试样例
# 旧版，现在都是用 _multi 的批量版本

# analyse apk
# wsj.reader_sp.apk
apk_path="/home/luzhirui/jerrylu/0421_fdroid_rerun/evo_apk/a2dp.Vol_137.apk-insted.apk"
aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"
SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path)
# main_activity = "wsj.ui.IssueActivity"

# org.npr.one.apk
# apk_path="/home/luzhirui/jerrylu/testAppium/0406apks/org.npr.one.apk"
# SDKversion, package, main_activity, minSdk = analyse_apk(apk_path)
# main_activity = "org.npr.one.StartActivity"

# us.mitene.apk
# apk_path="/home/luzhirui/jerrylu/testAppium/0406apks/us.mitene.apk"
# SDKversion, package, main_activity, minSdk = analyse_apk(apk_path)
# main_activity = "us.mitene.app.startup.ui.StartupActivity"


from pathlib import Path
apk_name = Path(apk_path).stem

# docker related config
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
# SDKversion =
Android_version = APIlevel_androidversion[str(SDKversion)]
image_name="budtmo/docker-android-x86-{}".format(Android_version)
# gui_port=6080
# appium_port=4723
# emu_port=5564
# adb_port=5565
gui_port=find_free_port()
appium_port=find_free_port()
emu_port=find_free_port()
adb_port=find_free_port()

# adb related config
adb_exe_path="/home/luzhirui/jerrylu/adb/platform-tools/adb"
adb_connection_str="localhost:" + str(adb_port)  # this is generated at runtime

# appium desired caps
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = Android_version
desired_caps['deviceName'] = 'emulator-5554' # This should be fine... They are all called `emulator-5554` internally inside container
desired_caps['appPackage'] = package
desired_caps['appActivity'] = main_activity
desired_caps['eventTimings'] = True
desired_caps['automationName'] = 'UIAutomator2'
desired_caps['autoGrantPermissions'] = True

# test related data containers
test_num = 0
# record target APIs triggered
trigger_target_APIs = set()
# record activities triggered
activities = set()
# record widgets triggered
widgets = set()
# record widgets in page_source
widgets_page_source = set()

# initialize
client = docker.from_env()
container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

# print("[*] reconfiguring network start")
# no_internet_network = client.networks.get("no-internet")
# bridge_network = client.networks.get("bridge")
# no_internet_network.connect(container)
# bridge_network.disconnect(container)
# print("[*] reconfiguring network done")

# main test loop
while test_num < 30:
    try:
        print("\n{} test:\n".format(test_num))
        appium_command = appium_driver(desired_caps, 100, activities, widgets, widgets_page_source, test_num, remote_addr=remote_addr, adb_exe_path=adb_exe_path, apk_name=apk_name, adb_port=adb_port)
        print("\n"+"appium_command:")
        print(appium_command)
        generate_test(appium_command, test_num, trigger_target_APIs, apk_name=apk_name)
    except Exception as e:
        print(e)
        print("error: {}".format(test_num) + "test")
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_tb(exc_traceback_obj)
    test_num += 1
    sleep(5)

# tear down: remove container
container.remove(force=True)
print("{*} container removed.")

# output & save results
print("triggered activities:")
print(activities)
print("triggered executable elements:")
print(widgets)
print("triggered target APIs:")
print(trigger_target_APIs)
print("all achievable executable elements")
print(widgets_page_source)
print("widget coverage:")
try:
    coverage = len(widgets)/len(widgets_page_source)
except Exception as e:
    coverage = -1
print(str(coverage))

with open(f'report/{apk_name}_report.txt', "w") as f:
    f.write("triggered activities:"+"\n")
    f.write(str(activities)+"\n")
    f.write("triggered executable elements:"+"\n")
    f.write(str(widgets)+"\n")
    f.write("triggered target APIs:"+"\n")
    f.write(str(trigger_target_APIs)+"\n")
    f.write("all achievable executable elements"+"\n")
    f.write(str(widgets_page_source)+"\n")
    f.write("widget coverage:"+"\n")
    f.write(str(coverage))
