import apkutils
from time import sleep
import traceback
import sys
from appiumdriver_processlog.appiumdriver.util.ProcessText import delete_text
from appiumdriver_processlog.appiumdriver.AppiumDriver import appium_driver
from appiumdriver_processlog.processlog.ProcessLogFile import generate_test

# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install

# docker related config
image_name="budtmo/docker-android-x86-8.1"
gui_port=6080
appium_port=4723
emu_port=5564
adb_port=5565

# adb related config
adb_exe_path="/home/jerrylu/adb/platform-tools/adb"
adb_connection_str="localhost:" + str(adb_port)  # this is generated at runtime
apk_path="/home/jerrylu/mineapk/de.danoeh.antennapod.apk"

# analyse apk
apk = apkutils.APK(apk_path)
main_activity = apk.get_main_activity()
package = apk.get_manifest()['@package']
SDKversion = apk.get_manifest()['@android:compileSdkVersionCodename']

# appium desired caps
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = SDKversion
desired_caps['deviceName'] = 'emulator-5554' # This should be fine... They are all called `emulator-5554` internally inside container
desired_caps['appPackage'] = package
desired_caps['appActivity'] = main_activity
desired_caps['eventTimings'] = True
desired_caps['automationName'] = 'UIAutomator2'

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

# clear the last log
try:
    delete_text("log/appium.log")
except Exception as e:
    print(e)
    exc_type, exc_value, exc_traceback_obj = sys.exc_info()
    traceback.print_tb(exc_traceback_obj)


# initialize
client = docker.from_env()
container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

# main test loop
while test_num < 30:
    try:
        print("\n{} test:\n".format(test_num))
        appium_command = appium_driver(desired_caps, 100, activities, widgets, widgets_page_source, test_num, remote_addr=remote_addr, adb_exe_path=adb_exe_path)
        print("\n"+"appium_command:")
        print(appium_command)
        generate_test(appium_command, test_num, trigger_target_APIs)
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
coverage = len(widgets)/len(widgets_page_source)
print(str(coverage))

with open('report/report.txt', "w") as f:
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