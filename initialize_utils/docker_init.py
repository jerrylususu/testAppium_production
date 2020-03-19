import docker

def docker_init(client, image_name="budtmo/docker-android-x86-8.1", gui_port=6080, appium_port=4723, emu_port=5564, adb_port=5565):
    # client = docker.from_env() # now is a param
    run_container = client.containers.run(
        image=image_name,
        # command="echo hello world",
        # name="py_based_android_container", # better leave random generated to prevent duplication
        detach=True, # return immediately
        privileged=True, # give privileges
        remove=True, # enable auto remove
        environment={
            "DEVICE": "Nexus 5",
            "APPIUM": "true",
            "APPIUM_HOST": "127.0.0.1",
            "APPIUM_PORT": "4723"
        },
        # volumes={   # using adb to install, no need to map
        #     "/home/jerrylu/mineapk": {
        #         "bind": "/root/tmp",
        #         "mode": "ro"
        #     }
        # },
        ports={
            "6080/tcp": str(gui_port),
            "4723/tcp": str(appium_port),
            "5554/tcp": str(emu_port),
            "5555/tcp": str(adb_port)
        }
    )
    print("{*} container started:",run_container.id)
    return run_container

if __name__ == "__main__":
    print("{!} RUN AS INVIDUAL FILE")
    client = docker.from_env()
    container = docker_init(client=client, image_name="budtmo/docker-android-x86-8.1", gui_port=6080, appium_port=4723, emu_port=5564, adb_port=5565)