from time import sleep

# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install, adb_connect_uninstall, adb_connect_uninstall_pkg
from initialize_utils.find_free_port import find_free_port

# 单纯运行在某个 version 上运行一个 apk，用于手动调试
# 用于测试能否正常 uninstall apk

# docker related config
# main configs
apk_path="/home/luzhirui/fdroid_1k6/com.mde.potdroid_80.apk"
image_name="budtmo/docker-android-x86-8.0"


gui_port=find_free_port()
appium_port=find_free_port()
emu_port=find_free_port()
adb_port=find_free_port()
print(f"[*] port config: gui={gui_port}, appium={appium_port}, emu={emu_port} ,adb={adb_port}")


# adb related config
adb_exe_path="/home/luzhirui/jerrylu/adb/platform-tools/adb"
adb_connection_str="localhost:" + str(adb_port)  # this is generated at runtime
apk_path="/home/luzhirui/jerrylu/testAppium/dummy/dummy-jerrylu.apk"
aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"

# initialize
client = docker.from_env()
container = docker_init(client=client, image_name=image_name, gui_port=gui_port, appium_port=appium_port, emu_port=emu_port, adb_port=adb_port)
adb_installed = adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
print(f"adb_installed: {adb_installed}")

remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

print("{*} remote addr: ", remote_addr)



input("s2: start uninstall apk1")

adb_uninstalled = adb_connect_uninstall(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path,aapt_path=aapt_path)
print(f"adb_uninstalled: {adb_uninstalled}")




input("s3: start install apk2")

apk_path="/home/luzhirui/fdroid_1k6/de.danoeh.antennapod_1080095.apk"
adb_installed = adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,apk_path=apk_path)
print(f"adb_installed: {adb_installed}")



input("s4: start uninstall apk2")


pkg_name="de.danoeh.antennapod"
adb_uninstalled = adb_connect_uninstall_pkg(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str,pkg_name=pkg_name)
print(f"adb_uninstalled: {adb_uninstalled}")



input("s5: remove container")

container.remove(force=True)
print("{*} container removed.")
