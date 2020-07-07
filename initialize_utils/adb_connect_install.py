from docker_replay_multi import aapt_path
from analyseapk.AnalyseAPK import analyse_apk
import os
from time import sleep
from datetime import datetime
import subprocess

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout
from initialize_utils.timeout_fix import timeout_exception_wrapper


@timeout_exception_wrapper
@func_set_timeout(200)
def adb_connect_install(adb_exe_path, adb_connection_str, apk_path, sleep_time=5):

    connected = False

    while not connected:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # return_code = os.system("/home/luzhirui/jerrylu/adb/platform-tools/adb connect localhost:5565")
        return_str = subprocess.check_output([adb_exe_path,"connect",adb_connection_str])
        print(current_time, return_str )
        if "refused" not in return_str.decode("utf8"):
            connected = True
            print("{!} Connected! Ready to install")
            break
        sleep(sleep_time)

    print("{!} Begin to install")

    counter = 0

    installed = False
    check_strs = ["Success", "INSTALL_FAILED_ALREADY_EXISTS"]
    fail_strs = ["INSTALL_PARSE_FAILED","INSTALL_FAILED_NO_MATCHING_ABIS"]
    install_str = "".encode("utf8")
    while not installed:
        try:
            counter += 1
            if counter > 50:
                raise Exception(f"[!] install failed: exceed attempt limit!, last result: {install_str.decode('utf8')}")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            # install_str = subprocess.check_output(" ".join([adb_exe_path,"-s",adb_connection_str,"install",apk_path]), shell=True)
            install_str = subprocess.check_output([adb_exe_path,"-s",adb_connection_str,"install",apk_path], stderr=subprocess.STDOUT)
            print(current_time)
            print("result",install_str.decode("utf8") )
            if any(check_str in install_str.decode("utf8") for check_str in check_strs):
                installed = True
                print("{!} Install success!")
                break

        except subprocess.CalledProcessError as e:
            print(f"[.] Device not ready yet, current attempt {counter}")
            print("eoutput", e.returncode, e.output.decode("utf8"))
            install_str = e.output
            if any(check_str in install_str.decode("utf8") for check_str in check_strs):
                installed = True
                print("{!} Install success!")
                break
            if any(fail_str in e.output.decode("utf8") for fail_str in fail_strs):
                print("parse fail...")
                installed = False
                raise Exception(f"[!] install failed: parse failure!, last result: {e.output.decode('utf8')}")
                break
            sleep(sleep_time)

    print("{#} Install APK done. Now you may proceed.")
    return installed


def adb_connect_uninstall_pkg(adb_exe_path, adb_connection_str, pkg_name, sleep_time=5):

    connected = False

    while not connected:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # return_code = os.system("/home/luzhirui/jerrylu/adb/platform-tools/adb connect localhost:5565")
        return_str = subprocess.check_output([adb_exe_path,"connect",adb_connection_str])
        print(current_time, return_str )
        if "refused" not in return_str.decode("utf8"):
            connected = True
            print("{!} Connected! Ready to uninstall")
            break
        sleep(sleep_time)

    print("{!} Begin to install")

    counter = 0

    uninstalled = False
    check_strs = ["Success"]
    uninstall_str = "".encode("utf8")
    while not uninstalled:
        try:
            counter += 1
            if counter > 50:
                raise Exception(f"[!] uninstall failed: exceed attempt limit!, last result: {uninstall_str.decode('utf8')}")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            # install_str = subprocess.check_output(" ".join([adb_exe_path,"-s",adb_connection_str,"install",apk_path]), shell=True)
            install_str = subprocess.check_output([adb_exe_path,"-s",adb_connection_str,"uninstall",pkg_name], stderr=subprocess.STDOUT)
            print(current_time)
            print("result",install_str.decode("utf8") )
            if any(check_str in install_str.decode("utf8") for check_str in check_strs):
                uninstalled = True
                print("{!} Install success!")
                break

        except subprocess.CalledProcessError as e:
            print(f"[.] Device not ready yet, current attempt {counter}")
            print("eoutput", e.returncode, e.output.decode("utf8"))
            install_str = e.output
            if any(check_str in install_str.decode("utf8") for check_str in check_strs):
                uninstalled = True
                print("{!} Install success!")
                break
            sleep(sleep_time)

    print("{#} Uninstall APK done. Now you may proceed.")
    return uninstalled

def adb_connect_uninstall(adb_exe_path, adb_connection_str, apk_path, aapt_path, sleep_time=5):
    
    SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path)
    return adb_connect_uninstall_pkg(adb_exe_path, adb_connection_str, package, sleep_time)


if __name__ == "__main__":
    print("{!} RUN AS INVIDUAL FILE")
    adb_connect_install(adb_exe_path="/home/luzhirui/jerrylu/adb/platform-tools/adb", adb_connection_str="localhost:5565",apk_path="/home/luzhirui/jerrylu/sootOutput/de.danoeh.antennapod_1080095.apk")