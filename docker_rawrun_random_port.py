from time import sleep

# jerrylu scripts
import docker
from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install
from initialize_utils.find_free_port import find_free_port


# docker related config
image_name="budtmo/docker-android-x86-8.0"
gui_port=6080
appium_port=4723
emu_port=5564
adb_port=5565

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

# print("[*] reconfiguring network start")
# no_internet_network = client.networks.get("no-internet")
# bridge_network = client.networks.get("bridge")
# no_internet_network.connect(container)
# bridge_network.disconnect(container)
# print("[*] reconfiguring network done")

remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

print("{*} remote addr: ", remote_addr)
input("seems prep done... press to start tear down...")

container.remove(force=True)
print("{*} container removed.")
