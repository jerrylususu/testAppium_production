import os
from time import sleep
from datetime import datetime
import subprocess

def adb_connect_install(adb_exe_path, adb_connection_str, apk_path, sleep_time=5):

    connected = False

    while not connected:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # return_code = os.system("/home/jerrylu/adb/platform-tools/adb connect localhost:5565")
        return_str = subprocess.check_output([adb_exe_path,"connect",adb_connection_str])
        print(current_time, return_str )
        if "refused" not in return_str.decode("utf8"):
            connected = True
            print("{!} Connected! Ready to install")
            break
        sleep(sleep_time)

    print("{!} Begin to install")

    installed = False
    check_strs = ["Success", "INSTALL_FAILED_ALREADY_EXISTS"]
    while not installed:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            install_str = subprocess.check_output([adb_exe_path,"-s",adb_connection_str,"install",apk_path])
            print(current_time)
            print(install_str )
            if any(check_str in install_str.decode("utf8") for check_str in check_strs):
                installed = True
                print("{!} Install success!")
                break
        except subprocess.CalledProcessError as e:
            print("{.} Device not ready yet.")
            sleep(sleep_time)

    print("{#} Install APK done. Now you may proceed.")


if __name__ == "__main__":
    print("{!} RUN AS INVIDUAL FILE")
    adb_connect_install(adb_exe_path="/home/jerrylu/adb/platform-tools/adb", adb_connection_str="localhost:5565",apk_path="/home/jerrylu/mineapk/de.danoeh.antennapod.apk")