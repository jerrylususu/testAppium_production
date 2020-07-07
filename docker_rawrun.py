from time import sleep

# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install
from initialize_utils.find_free_port import find_free_port

# 单纯运行在某个 version 上运行一个 apk，用于手动调试

# docker related config
# main configs
apk_path="/home/luzhirui/fdroid_1k6/com.mde.potdroid_80.apk"
image_name="budtmo/docker-android-x86-6.0"


gui_port=find_free_port()
appium_port=find_free_port()
emu_port=find_free_port()
adb_port=find_free_port()
print(f"[*] port config: gui={gui_port}, appium={appium_port}, emu={emu_port} ,adb={adb_port}")


# adb related config
adb_exe_path="/home/luzhirui/jerrylu/adb/platform-tools/adb"
adb_connection_str="localhost:" + str(adb_port)  # this is generated at runtime
# apk_path="/home/luzhirui/jerrylu/testAppium/dummy/pod/de.danoeh.antennapod.apk"
apk_path="/home/luzhirui/jerrylu/testAppium/dummy/dummy-jerrylu.apk"


# initialize
client = docker.from_env()
container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
adb_installed = adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
print(f"adb_installed: {adb_installed}")

remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

print("{*} remote addr: ", remote_addr)
input("seems prep done... press to start tear down...")

container.remove(force=True)
print("{*} container removed.")
