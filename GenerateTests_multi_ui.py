from time import sleep
import traceback
import sys

from analyseapk.AnalyseAPK import analyse_apk
from appiumdriver_processlog.appiumdriver.util.ProcessText import delete_text
from appiumdriver_processlog.appiumdriver.AppiumDriver import appium_driver, appium_driver_ui
from appiumdriver_processlog.processlog.ProcessLogFile import generate_test

# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install
from initialize_utils.find_free_port import find_free_port
from pathlib import Path
import multiprocessing.dummy as mp
import base64

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout

def run_single_apk_task(apk_path):

    print(f"[!] current processing {apk_path}")
    apk_path = str(apk_path)
    container = None
    apk_name = Path(apk_path).stem


    success_finish = True
    try:
        # analyse apk
        # apk_path="/home/luzhirui/jerrylu/mineapk/de.danoeh.antennapod.apk"
        print(f"[!] analyse...")
        aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"
        package = "UNKNOWN"
        SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path=aapt_path)
        if package == "UNKNOWN":
            return "analyze_apk_failed..."
        print(SDKversion, package, main_activity, minSdk)
        SDKversion = str(SDKversion)

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
        Android_version = APIlevel_androidversion[SDKversion]
        image_name="budtmo/docker-android-x86-{}".format(Android_version)
        # image_name="budtmo/docker-android-x86-{}".format("9.0")

        gui_port=find_free_port()
        appium_port=find_free_port()
        emu_port=find_free_port()
        adb_port=find_free_port()
        print(f"[*] {apk_name}: port config: gui={gui_port}, appium={appium_port}, emu={emu_port} ,adb={adb_port}")
        with open("port.log", "a") as port_log:
            port_log.write(f"[*] {apk_name}: port config: gui={gui_port}, appium={appium_port}, emu={emu_port} ,adb={adb_port}")
            port_log.write("\n")

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
        print(f"[!] setting up docker...")
        client = docker.from_env()
        container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
        print(f"[!] starting install apk...")
        adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
        remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

        # main test loop
        print(f"[!] entering main test loop...")
        while test_num < 3:
            # try:
            print("\n{} test:\n".format(test_num))
            appium_command = appium_driver_ui(desired_caps, 100, activities, widgets, widgets_page_source, test_num, remote_addr=remote_addr, adb_exe_path=adb_exe_path, apk_name=apk_name, adb_port=adb_port)
            print("\n"+"appium_command:")
            print(appium_command)
            generate_test(appium_command, test_num, trigger_target_APIs, apk_name=apk_name)

            # except Exception as e:
            #     print(e)
            #     print("error: {}".format(test_num) + "test")
            #     exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            #     traceback.print_tb(exc_traceback_obj)
            test_num += 1
            sleep(5)



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

        print(f"[!] saving to report...")
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

        print("-----------DONE---------------")
    except FunctionTimedOut as e:
        success_finish = False

        with open(f"generate_logs/{apk_name}.log", "a") as f:
            f.write(str(e))
        print(f"[!] error {e}")
        print("-----------ERROR LAST---------------")
    except Exception as e:

        success_finish = False

        with open(f"generate_logs/{apk_name}.log", "a") as f:
            f.write(str(e))
        print(f"[!] error {e}")
        print("-----------ERROR LAST---------------")
    finally:
        # tear down: remove container
        try:
            if container is not None:
                container.remove(force=True)
        except Exception as e2:
            with open(f"generate_logs/{apk_name}.log", "a") as f:
                f.write(str(e2))
                print(f"[!] error {e2}")

        with open(f"generate_logs/{apk_name}.log", "a") as f:
            f.write("\nsuccess finish:"+str(success_finish))
        print("{*} container removed.")
    
    return apk_path

if __name__ == "__main__":
    # load apk from path
    # apk_folder_path = "/home/luzhirui/jerrylu/signed_apks_fdroid"
    # apk_folder_path = Path(apk_folder_path)
    # apk_file_list = []
    # for f in apk_folder_path.iterdir():
    #     if f.name.endswith(".apk"):
    #         apk_file_list.append(f)

    # apk_file_list = [Path("/home/luzhirui/jerrylu/testAppium/0408apks/de.danoeh.antennapod_instrumentation.apk")]

    # load apk from file
    apk_file_list = []
    # with open("/home/luzhirui/jerrylu/0421_fdroid_rerun/evo_fdroid_list_full.txt","r") as f:
    #     lines = f.readlines()
    lines = ["/home/luzhirui/jerrylu/mineapk/de.danoeh.antennapod.apk"]
    apk_file_list = [Path(i.strip()) for i in lines]
    # apk_file_list = apk_file_list[0:1]
    print(f"[*] current apk list: {apk_file_list}")

    pool_size=8

    with mp.Pool(processes=pool_size) as pool:
        task_list = []
        for apk_path in apk_file_list:
            task = pool.apply_async(run_single_apk_task, (apk_path,))
            task_list.append(task)
        for task in task_list:
            print("[*]",task.get(), "DONE!")

    print("ALL DONE!")

