# producer，仅负责抓取样例，生成任务

import json
import logging
import sys
from sys import version_info
import time
from pathlib import Path
from time import sleep
from typing import List
import re

import pika
import jsonpickle


sys.path.insert(0,'..')

from mq_replay.docker_replay_mq_replaytask import *

from initialize_utils.docker_init import docker_init
from initialize_utils.adb_connect_install import adb_connect_install
from initialize_utils.find_free_port import find_free_port
from analyseapk.AnalyseAPK import analyse_apk

if __name__ == "__main__":
    
    # pre. setup logging
    logging.basicConfig(filename="pylog/producer.log", level=logging.INFO, format="%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # consts.
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
    replay_testcase_path = "/home/luzhirui/jerrylu/testAppium/replay_0714_mqdebug/output"
    testcase_name_regex = re.compile("testcase_(.+)-insted_ctest_(\d+)_test(\d+)")

    # create the queue
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", heartbeat=0))
    channel = connection.channel()

    channel.exchange_declare(exchange='replay_request', exchange_type='topic')


    # param.
    # NOTE: 输入 apk list，注意使用原版，不要使用插桩之后的版本    
    apk_list_path = "/home/luzhirui/jerrylu/0417_fdroid_1k6_api_rerun/all_fdroid_1k6.txt"
    with open(apk_list_path, "r") as f:
        apk_raw_paths = f.readlines()

    apk_files = [Path(i.strip()) for i in apk_raw_paths]

    for apk_path in apk_files:

        logging.info("starting on {}".format(apk_path))

        SDKversion, package, main_activity, minSdk = analyse_apk(apk_path, aapt_path)
        # min sdk parse error?
        if minSdk is None or SDKversion is None or main_activity is None or SDKversion is None:
            logging.error(f"apk parse failed: SDKversion, package, main_activity, minSdk = {(SDKversion, package, main_activity, minSdk)}")
            continue
        

        # appium desired caps
        desired_caps = {}
        try:
            Android_version = APIlevel_androidversion[str(SDKversion)]
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
            minSdk_ver = "10.0" # FIXME: 这里和 docker_replay_multi_logging.py 不一样，之前是 10

        version_li = []
        for k,v in APIlevel_androidversion.items():
            if int(k) >= minSdk:
                version_li.append(v)
        image_name_list = [f"budtmo/docker-android-x86-{i}" for i in version_li]

        replay_testcase_list: List[ReplayTestCase] = []

        for file in list(Path(replay_testcase_path).iterdir()):
            if apk_path.stem in file.stem:
                with open(str(file),"r",encoding="utf8") as f:
                    content = f.readlines()
                
                apk_name_in_test, testn, ctestn = re.match(testcase_name_regex, file.stem).groups()

                if len(content) > 0:
                    testcase = ReplayTestCase(
                        testNumber=testn,
                        ctestNumber=ctestn,
                        fileContent=content
                    )
                    replay_testcase_list.append(testcase)

                # NOTE: 在 convert 的时候就做过滤，不要等到现在，因为已经带上了上下文，没法搞了
                # if not only_sleep1(content) or len(content) <= 5:  #FIXME: that's broken test
                #     replay_file_list.append(file)
                # else:
                #     print("skipping "+str(file))

        logging.info(f"{apk_path.stem}, len(testcase)={len(replay_testcase_list)}")
                
        if len(replay_testcase_list) == 0:
            continue

        # for each android version
        for v in version_li:
            # NOTE: routing key: version.(virtual/physical)
            routing_key = f"{v}.virtual"

            # setup version info
            desired_caps["platformVersion"] = v

            # create the message?
            replay_request = ReplayRequest(
                apkName=apk_path.name,
                packageName=package,
                androidVersion=v,
                replayCaseList=replay_testcase_list,
                desiredCaps = desired_caps
            )

            channel.basic_publish(exchange="replay_request", routing_key=routing_key, body=jsonpickle.encode(replay_request))
            pass


    # when ends, close connection of rabbitmq
    connection.close()

    pass
