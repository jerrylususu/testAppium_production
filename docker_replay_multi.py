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

import json

from appium import webdriver

from analyseapk.AnalyseAPK import analyse_apk
from appiumdriver_processlog.appiumdriver.util.ProcessText import delete_text
from appiumdriver_processlog.appiumdriver.AppiumDriver import appium_driver
from appiumdriver_processlog.processlog.ProcessLogFile import generate_test

import multiprocessing.dummy as mp

import logging

import base64

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout

def log_to_file(path, content, time, write_name):
    with open(path, "a") as f:
        f.write(str(time))
        f.write("\n")
        f.write(write_name)
        f.write("\n")
        f.write(content)
        f.write("\n")
        f.write("--------")
        f.write("\n")

def run_cases_on_image(apk_path, replay_file_list, image_name):
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
    apkname = Path(apk_path).name
    replace_img_name = image_name.replace("/","_")

    write_name = f"{apkname}_{replace_img_name}"
    now = datetime.datetime.now()
    container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port, name=write_name)
    try:
        adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
    except Exception as e:
        try:
            container.remove(force=True)
            print("{*} container removed.")
        except Exception as e:
            print(case.stem, e)
        return write_name
        log_to_file(f"replay/replay_logs/replay.log_{write_name}", "adbinstall:"+str(e),now, write_name)


    print("{*} remote addr: ", remote_addr)

    for idx, case in enumerate(replay_file_list):
        case = Path(case)
        print("{*} running case: "+str(case)+" with image: "+image_name+" apk:"+str(apk_path))
        with open(case, "r", encoding="utf8") as f:
            code = "\n".join(f.readlines())
        print(f"[*] read code len={len(code)}, executing...")
        code = code.replace("def test_function(", f"def test_function_{idx}(")
        code += """\n
    with open(f"/home/luzhirui/jerrylu/testAppium/replay/replay_screenshots/{write_name}.png", "wb") as f:
        f.write(base64.b64decode(driver.get_screenshot_as_base64()))"""
        exec(code)

        print(f"[*] test case load done, start replay...")
        print(f"[DBG] remote_addr={remote_addr}, write_name={case.stem}")
        
        now = datetime.datetime.now()
        current_date_str = now.strftime("%Y%m%d_%H%M%S")
        
        replace_img_name = image_name.replace("/","_")

        desired_caps['platformVersion'] = image_name.split("-")[-1]

        write_name = f"{case.stem}_{replace_img_name}"

        try:
            locals()[f"test_function_{str(idx)}"](remote_addr=remote_addr, desired_caps=desired_caps, write_name=write_name)
            log_to_file(f"replay/replay_logs/replay.log_{write_name}", "SUCCESS!", now, write_name)
        except Exception as e:
            print(case.stem, e)
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            traceback.print_tb(exc_traceback_obj)
            log_to_file(f"replay/replay_logs/replay.log_{write_name}", "ERR:"+str(e), now, write_name)
            if "socket hang up" in str(e):
                print("hangup retry1")
                container.remove(force=True)
                container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
                adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
                try:
                    test_function(remote_addr=remote_addr, desired_caps=desired_caps, write_name=case.stem)
                    log_to_file(f"replay/replay_logs/replay.log_{write_name}", "SUCCESS! with retry", now, write_name)
                except Exception as e:
                    print(case.stem, e)
                    log_to_file(f"replay/replay_logs/replay.log_{write_name}", "ERR(retry):"+str(e), now, write_name)
        # finally:
    try:
        container.remove(force=True)
        print("{*} container removed.")
    except Exception as e:
        print(case.stem, e)
        log_to_file(f"replay/replay_logs/replay.log_{write_name}", "ERR(final):"+str(e), now, write_name)
    finally:
        print(write_name, "closing")
        return write_name

def only_sleep1(li):
    for line in li:
        if line.strip() != "sleep(1)":
            return False
    return True


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='replay-multi.log', 
    filemode='a')

# basic config
adb_exe_path="/home/luzhirui/jerrylu/adb/platform-tools/adb"
aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"
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


apk_list_path = "/home/luzhirui/jerrylu/0421_fdroid_rerun/replay_evo2_remaining3.txt"
with open(apk_list_path, "r") as f:
    apk_raw_paths = f.readlines()

apk_files = [Path(i.strip()) for i in apk_raw_paths]

print(apk_files)

for apk_path in apk_files:

    SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path)

    if minSdk is None:
        print("minsdk unknown!")
        continue

    # appium desired caps
    try:
        Android_version = APIlevel_androidversion[str(SDKversion)]
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = Android_version
        desired_caps['deviceName'] = 'emulator-5554' # This should be fine... They are all called `emulator-5554` internally inside container
        desired_caps['appPackage'] = package
        desired_caps['appActivity'] = main_activity
        desired_caps['eventTimings'] = True
        desired_caps['automationName'] = 'UIAutomator2'
        desired_caps['autoGrantPermissions'] = True # auto grant permission


        minSdk_ver = APIlevel_androidversion[str(minSdk)]
    except KeyError:
        minSdk_ver = "10"

    version_li = []
    for k,v in APIlevel_androidversion.items():
        if int(k) >= minSdk:
            version_li.append(v)
    image_name_list = [f"budtmo/docker-android-x86-{i}" for i in version_li]


    # image_name_list = ["budtmo/docker-android-x86-10.0","budtmo/docker-android-x86-9.0","budtmo/docker-android-x86-8.1","budtmo/docker-android-x86-8.0","budtmo/docker-android-x86-7.1.1","budtmo/docker-android-x86-7.0","budtmo/docker-android-x86-6.0","budtmo/docker-android-x86-5.1.1","budtmo/docker-android-x86-5.0.1"]
    # image_name_list = ["budtmo/docker-android-x86-9.0"]
    # replay_file_list = ["replay/output/testcase_de.danoeh.antennapod_instrumentation_ctest_37_test2.py"]
    # replay_file_list = list(Path("/home/luzhirui/jerrylu/testAppium/replay/output").iterdir())
    replay_file_list = []
    for file in list(Path("/home/luzhirui/jerrylu/testAppium/replay/output").iterdir()):
        if apk_path.stem in file.stem:
            with open(str(file),"r",encoding="utf8") as f:
                content = f.readlines()
            if not only_sleep1(content) or len(content) <= 5:  #FIXME: that's broken test
                replay_file_list.append(file)
            else:
                print("skipping "+str(file))

    print(replay_file_list)

    if len(replay_file_list) == 0:
        continue

    pool_size=8

    with mp.Pool(processes=pool_size) as pool:
        task_list = []
        for image_name in image_name_list:
            task = pool.apply_async(run_cases_on_image, (apk_path, replay_file_list, image_name,))
            task_list.append(task)
        for task in task_list:
            try:
                print("[*]",str(task.get(timeout=400)), "DONE!")
            except Exception as e:
                print(e)

    logging.info("ALL DONE!")
