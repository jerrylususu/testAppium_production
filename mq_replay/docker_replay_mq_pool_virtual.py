# pool，准备所需要的 docker 镜像，并将结果写入对应文件

import json
import docker
import logging
import sys
import time

from docker.types import containers

sys.path.insert(0,'..')


from initialize_utils.find_free_port import find_free_port
from initialize_utils.get_valid_filename import get_valid_filename


if __name__ == "__main__":

    # consts.
    image_prefix = "budtmo/docker-android-x86-"

    # pre. setup logging
    logging.basicConfig(filename="pylog/pool_virtual.log", level=logging.INFO, format="%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    container_list = []
    status_line_list = []

    # step 0. get docker client
    client = docker.from_env()

    # step 1. read json
    with open("replay_pool.json","r") as f:
        pool_config = json.load(f)
    
    logging.info(pool_config)

    # use pool
    with open("pool_status","w") as fs:

        # step 2. start docker containers
        # 2a. start each one by one
        # 2b. store the results to a `status` file
        for version, count in pool_config.items():
            for idx in range(count):
                image_name = image_prefix + version
                container_name = get_valid_filename(image_name) + "_" + str(idx)
                print(container_name)

                # NOTE: only needs adb_port + appium_port
                gui_port=find_free_port()
                appium_port=find_free_port()
                emu_port=find_free_port()
                adb_port=find_free_port()

                container = client.containers.run(
                    image=image_name,
                    name=container_name,
                    detach=True, # return immediately
                    privileged=True, # give privileges
                    remove=True, # enable auto remove
                    environment={
                        "DEVICE": "Nexus 5",
                        "APPIUM": "true",
                        "APPIUM_HOST": "127.0.0.1",
                        "APPIUM_PORT": "4723"
                    },
                    ports={
                        "6080/tcp": str(gui_port),
                        "4723/tcp": str(appium_port),
                        "5554/tcp": str(emu_port),
                        "5555/tcp": str(adb_port)
                    }
                )

                container_list.append(container)

                # NOTE: status line format: id, adb_port, appium_port, version, idx, (virtual/physical), emu_port, gui_port
                status_line = f"{container.id},{adb_port},{appium_port},{version},{idx},virtual,{emu_port},{gui_port}"
                logging.info(status_line)
                status_line_list.append(status_line)

                fs.write(f"{status_line}\n")

                time.sleep(5) # to prevent too fast create
    
    # step 3. wait to tear down
    logging.info("all virtual device started...")
    input("input anything to start teardown")
    
    for idx, container in enumerate(container_list):
        status_line = status_line_list[idx]
        if container is not None:
            try:
                container.remove(force=True)
                logging.info(f"remove success {status_line}")
            except:
                logging.exception(f"remove failure {status_line}")
    
    logging.info("all removed...")