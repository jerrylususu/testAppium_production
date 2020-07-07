from time import sleep
from pathlib import Path
import datetime
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


# docker related config
# image_name="budtmo/docker-android-x86-9.0"

adb_exe_path="/home/luzhirui/jerrylu/adb/platform-tools/adb"
aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"

# apk_path="/home/luzhirui/jerrylu/mineapk/de.danoeh.antennapod.apk"
apk_path = "/home/luzhirui/jerrylu/testAppium/dummy/dummy-photo.apk"

SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path)
# appium desired caps
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
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = Android_version
desired_caps['deviceName'] = 'emulator-5554' # This should be fine... They are all called `emulator-5554` internally inside container
desired_caps['appPackage'] = package
desired_caps['appActivity'] = main_activity
desired_caps['eventTimings'] = True
desired_caps['automationName'] = 'UIAutomator2'


image_name_list = ["budtmo/docker-android-x86-8.0"]
# image_name_list = ["budtmo/docker-android-x86-9.0"]
# replay_file_list = ["replay/output/testcase_de.danoeh.antennapod_instrumentation_ctest_37_test2.py"]
# replay_file_list = list(Path("/home/luzhirui/jerrylu/testAppium/replay/output").iterdir())
replay_file_list = ["/home/luzhirui/jerrylu/testAppium/replay/output/testcase_dummy-app-hdr-fucked_ctest_11_test1.py"]
# cnt = 0
# for file in list(Path("/home/luzhirui/jerrylu/testAppium/replay/output").iterdir()):
#     if "dummy-app-hdr-fucked" in file.stem:
#         replay_file_list.append(file)
#         cnt += 1
#     if cnt > 5:
#         break

print(replay_file_list)

for image_name in image_name_list:
    gui_port=find_free_port()
    appium_port=find_free_port()
    emu_port=find_free_port()
    adb_port=find_free_port()
    print(f"[*] port config: gui={gui_port}, appium={appium_port}, emu={emu_port} ,adb={adb_port}")

    # adb related config
    adb_connection_str="localhost:" + str(adb_port)  # this is generated at runtime
    remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

    # initialize
    client = docker.from_env()
    container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
    adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)

    print("{*} remote addr: ", remote_addr)

    for case in replay_file_list:
        case = Path(case)
        print("{*} running case: "+str(case)+" with image: "+image_name)
        with open(case, "r", encoding="utf8") as f:
            code = "\n".join(f.readlines())
        print(f"[*] read code len={len(code)}, executing...")
        exec(code)

        print(f"[*] test case load done, start replay...")
        print(f"[DBG] remote_addr={remote_addr}, write_name={case.stem}")
        
        now = datetime.datetime.now()
        current_date_str = now.strftime("%Y%m%d_%H%M%S")
        
        replace_img_name = image_name.replace("/","_")

        desired_caps['platformVersion'] = image_name.split("-")[-1]

        write_name = f"{case.stem}_{replace_img_name}"

        try:
            test_function(remote_addr=remote_addr, desired_caps=desired_caps, write_name=write_name)
            with open(f"replay/replay_logs/replay.log_{write_name}","a") as f:
                f.write(str(now))
                f.write("\n")
                f.write(case.stem)
                f.write("\n")
                f.write("SUCCESS!")
                f.write("\n")
                f.write("--------")
                f.write("\n")
        except Exception as e:
            print(case.stem, e)
            with open(f"replay/replay_logs/replay.log_{write_name}","a") as f:
                f.write(str(now))
                f.write("\n")
                f.write(case.stem)
                f.write("\n")
                f.write(str(e))
                f.write("\n")
                f.write("--------")
                f.write("\n")
            if "socket hang up" in str(e):
                print("hangup retry1")
                container.remove(force=True)
                container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
                adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
                try:
                    test_function(remote_addr=remote_addr, desired_caps=desired_caps, write_name=write_name)
                    with open(f"replay/replay_logs/replay.log_{write_name}","a") as f:
                        f.write(str(now))
                        f.write("\n")
                        f.write(case.stem)
                        f.write("\n")
                        f.write("SUCCESS!")
                        f.write("\n")
                        f.write("--------")
                        f.write("\n")
                except Exception as e:
                    print(case.stem, e)
                    with open(f"replay/replay_logs/replay.log_{write_name}","a") as f:
                        f.write(str(now))
                        f.write("\n")
                        f.write(case.stem)
                        f.write("\n")
                        f.write("err2")
                        f.write("\n")
                        f.write(str(e))
                        f.write("\n")
                        f.write("--------")
                        f.write("\n")



                

    container.remove(force=True)
    print("{*} container removed.")