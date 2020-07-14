# consumer: 具体的处理方法，处理每一个 ReplayRequest
# 包括 adb 安装，跑 testcase，保留输出结果，发送回去，adb 卸载

from logging import exception

import jsonpickle
import json
import logging
import typing
import pika
import sys
from pathlib import Path
import base64

import traceback
import sys
import datetime
from time import sleep
from appium import webdriver

sys.path.insert(0,'..')

from mq_replay.docker_replay_mq_replaytask import *
from initialize_utils.adb_connect_install import adb_connect_install, adb_connect_uninstall_pkg

def run_test_case(adb_port: int, appium_port: int, replay_request: ReplayRequest, 
channel, current_status_line, 
adb_exe_path, local_apk_root, replay_output_full_path) -> bool:

    # NOTE: replay_output_full_path ends with /
    # subfolder: replay_adb, replay_page_sources, replay_screenshots
    logging.info(f"received request: {replay_request.apkName}")

    # step0. prepare param
    apk_path = Path(local_apk_root) / replay_request.apkName
    adb_connection_str = "localhost:" + str(adb_port)
    remote_addr = "http://localhost:"+str(appium_port)+"/wd/hub"

    # step1. install apk
    install_success = False
    try:
        install_success = adb_connect_install(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str, apk_path=apk_path)
    except:
        logging.exception(f"apk install error: {replay_request.apkName} @ {current_status_line}")

    if not install_success:
        logging.error(f"apk install failed: {replay_request.apkName} @ {current_status_line}")
        return False

    # step2. run test cases
    # for each test case
    # run -> read result -> package ReplayResponse -> send to queue
    for idx, testcase in enumerate(replay_request.replayCaseList):

        write_name = f"{replay_request.apkName}_t{testcase.testNumber}c{testcase.ctestNumber}_{replay_request.androidVersion}"

        # set up the response
        replay_response = ReplayResponse(success=True,
            errorMessage="not inited",
            pageSource="",
            imgBase64="",
            adbLog="",
            testcaseSummary=ReplayTestCaseSummary(
                apkName=replay_request.apkName,
                packageName=replay_request.packageName,
                androidVersion=replay_request.androidVersion,
                testNumber=testcase.testNumber,
                ctestNumber=testcase.ctestNumber,
                writeName=write_name
            )
        )
        
        # read test case code & load
        logging.info(f"running case {idx} (t{testcase.testNumber}c{testcase.ctestNumber}) of apk {replay_request.apkName}")
        code = testcase.fileContent
        logging.info(f"[*] read code len={len(code)}, executing...")
        code = code.replace("def test_function(", f"def test_function_{idx}(")
        code += """\n
    with open(f"replay/replay_screenshots/{write_name}.png", "wb") as f:
        f.write(base64.b64decode(driver.get_screenshot_as_base64()))"""
        
        # replace the replay output path!
        code = code.replace('open(f"replay/',f'open(f"{replay_output_full_path}')
        
        exec(code)
        logging.info(f"[*] test case load done, start replay...")
        logging.info(f"[DBG] remote_addr={remote_addr}, write_name={write_name}")
        
        # try to run the test case
        try:
            locals()[f"test_function_{str(idx)}"](remote_addr=remote_addr, desired_caps=replay_request.desiredCaps, write_name=write_name)
        except Exception as e:
            logging.exception(f"run case exception @ {write_name}")
            replay_response.success = False
            replay_response.errorMessage = str(e)

        # read the results
        if replay_response.success:
            output_root = Path(replay_output_full_path)
            with open(output_root / "replay_screenshots" / f"{write_name}.png", "rb") as screenshot_file:
                replay_response.imgBase64 = base64.b64encode(screenshot_file.read())
            with open(output_root / "replay_page_sources" / f"page_source_{write_name}.xml", "r") as xml_file:
                replay_response.pageSource = xml_file.read()
            with open(output_root / "replay_adb" / f"adblog_{write_name}.json", "r") as json_file:
                replay_response.adbLog = json_file.read()

        # send the result
        routing_key=f"{replay_request.apkName}.{replay_request.androidVersion}.{testcase.testNumber}.{testcase.ctestNumber}"
        channel.basic_publish(exchange="replay_response", routing_key=routing_key,body=jsonpickle.encode(replay_response))


    # step3. uninstall apk
    uninstall_success = False
    try:
        uninstall_success = adb_connect_uninstall_pkg(adb_exe_path=adb_exe_path, adb_connection_str=adb_connection_str, pkg_name=replay_request.packageName)
    except:
        logging.exception(f"apk uninstall error: {replay_request.apkName} @ {current_status_line}")
    # if uninstall failed, not big problem, but still need to be noted
    if not uninstall_success:
        logging.warning(f"apk uninstall failed: {replay_request.apkName} @ {current_status_line}")


    return True
