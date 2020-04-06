from time import sleep
from pathlib import Path
# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install
from initialize_utils.find_free_port import find_free_port

# docker related config
# image_name="budtmo/docker-android-x86-9.0"

adb_exe_path="/home/jerrylu/adb/platform-tools/adb"
apk_path="/home/jerrylu/mineapk/de.danoeh.antennapod.apk"

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554' # This should be fine... They are all called `emulator-5554` internally inside container
desired_caps['appPackage'] = 'de.danoeh.antennapod'
desired_caps['appActivity'] = 'de.danoeh.antennapod.activity.SplashActivity'
desired_caps['eventTimings'] = True
desired_caps['automationName'] = 'UIAutomator2'

# image_name_list = ["budtmo/docker-android-x86-9.0","budtmo/docker-android-x86-8.0","budtmo/docker-android-x86-7.0"]
image_name_list = ["budtmo/docker-android-x86-9.0"]
replay_file_list = ["replay_cases/replay_attempt/replay_main.py"]

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
        test_function(remote_addr=remote_addr, desired_caps=desired_caps, write_name=case.stem)


    container.remove(force=True)
    print("{*} container removed.")