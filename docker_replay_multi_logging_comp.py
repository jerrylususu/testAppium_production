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

from multi_logging import worker_init, logger_init

img_folder = Path("/home/luzhirui/jerrylu/testAppium/replay_evo2/replay_screenshots/")

# comp: 补全没有图片的
# 这个是权宜之计，之前会跑着跑着崩掉，是为了在第一次全量 replay 之后没有正常图片输出的那些

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
    """
    This runs multiple test case at the same time on a specific image container.
    """

    # find free ports
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

    # prepare container
    # WARNING: THESE ARE NOT LIGHTWEIGHT CONTAINERS! THEY ARE QUITE HEAVY!
    container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port, name=write_name)
    try:

        # try to install
        # this might lead to timeout, but should not hang up here...
        adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
    except Exception as e:
        # if adb install fail, try to remove the docker???
        print("adb install failed...")
        try:
            log_to_file(f"replay/replay_logs/replay.log_{write_name}", "adbinstall:"+str(e),now, write_name)
            container.remove(force=True)
            container = None
            logging.exception("adb exception happened")
            print("{*} container removed.")
        except FunctionTimedOut:
            logging.exception("adb install timed out")
        except Exception as e:
            logging.exception("adb exception handle failed")
            print(case.stem, e)
        finally:
            return write_name

    # by now, container should be ready, and the apk has been installed
    print("{*} remote addr: ", remote_addr)

    # run all the case one by one
    for idx, case in enumerate(replay_file_list):

        case = Path(case)

        replace_img_name = image_name.replace("/","_")

        # change the platform version
        # FIXME: OS 7.0 bug
        desired_caps['platformVersion'] = image_name.split("-")[-1]
 
        write_name = f"{case.stem}_{replace_img_name}"
        img_path = img_folder / ( write_name + ".png" )

        if img_path.exists():
            continue

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
        


        # try to run the test case
        try:
            locals()[f"test_function_{str(idx)}"](remote_addr=remote_addr, desired_caps=desired_caps, write_name=write_name)
            log_to_file(f"replay/replay_logs/replay.log_{write_name}", "SUCCESS!", now, write_name)
        except Exception as e:
            # failed
            logging.exception("run case exception happened")
            print(case.stem, e)
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            traceback.print_tb(exc_traceback_obj)
            log_to_file(f"replay/replay_logs/replay.log_{write_name}", "ERR:"+str(e), now, write_name)
            
            # if this is socket hangup, try again
            if "socket hang up" in str(e):
                logging.error("socket hang up")
                print("hangup retry1")
                try:
                    logging.info("hang up retry begin")
                    container.remove(force=True)
                    container = None
                    container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
                    adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
                    logging.info("hang up retry finish adb install")
                    try:
                        logging.info("retrying....")
                        test_function(remote_addr=remote_addr, desired_caps=desired_caps, write_name=case.stem)
                        logging.info("hang up retry done")
                        log_to_file(f"replay/replay_logs/replay.log_{write_name}", "SUCCESS! with retry", now, write_name)

                    except Exception as e:
                        logging.exception("hang up retry exception")
                        print(case.stem, e)
                        log_to_file(f"replay/replay_logs/replay.log_{write_name}", "ERR(retry):"+str(e), now, write_name)
                except FunctionTimedOut:
                    logging.exception("hang up retry adb install timed out")
                except Exception as e:
                    logging.exception("hang up retry exception")
                    logging.error(e)
                finally:
                    if container is not None:
                        container.remove(force=True)
                        container = None

        # finally:

    # at last, remove the container, if it is still there...
    try:
        if container is not None:
            container.remove(force=True)
            print("{*} container removed.")
        else:
            print("{*} container is null")
    except Exception as e:
        logging.exception("final exception happened")
        print(case.stem, e)
        log_to_file(f"replay/replay_logs/replay.log_{write_name}", "ERR(final):"+str(e), now, write_name)
    finally:
        print(write_name, "closing")
        return write_name

def only_sleep1(li):
    # NOT WORKING!
    for line in li:
        if line.strip() != "sleep(1)":
            return False
    return True


if __name__ == "__main__":
    q_listener, q = logger_init(file_location="pylogs/replay_multi.log")

    pool_size=10

    # mp.freeze_support()
    pool = mp.Pool(pool_size, worker_init, [q])

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

    # read the apk file list
    apk_list_path = "/home/luzhirui/jerrylu/0421_fdroid_rerun/all_fdroid_1k6.txt"
    with open(apk_list_path, "r") as f:
        apk_raw_paths = f.readlines()

    apk_files = [Path(i.strip()) for i in apk_raw_paths]

    print(apk_files)

    # for each apk, each as a batch
    for apk_path in apk_files:

        logging.info("starting on {}".format(apk_path))

        SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path)
        # min sdk parse error?
        if minSdk is None:
            logging.error("minsdk unknown!: {}".format(str(apk_path)))
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
        for file in list(Path("/home/luzhirui/jerrylu/testAppium/replay_evo2/output").iterdir()):
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

        # pool_size=len(image_name_list)

        # mp.freeze_support()
        # pool = mp.Pool(pool_size, worker_init, [q])
        task_list = []

        for image_name in image_name_list:
            task = pool.apply_async(run_cases_on_image, (apk_path, replay_file_list, image_name,))
            task_list.append(task)
        
        # pool.close()
        # pool.join()

        for idx, task in enumerate(task_list):
            print("local idx", idx, "total", len(task_list))
            try:
                logging.info(" ".join(["[*]",str(task.get(timeout=600)), "DONE!"]))
            except Exception as e:
                logging.exception("exception happened in main loop")
                print(e)

        # logging.info("ALL DONE!")
