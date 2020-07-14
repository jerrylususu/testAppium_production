# runner: 真正执行 consumer 中规定的 consume 函数

import json
import logging
from logging import log

import jsonpickle
import sys
from sys import version_info
import time
from pathlib import Path
from time import sleep
import pika
import jsonpickle

sys.path.insert(0,'..')

from mq_replay.docker_replay_mq_replaytask import *
from mq_replay.docker_replay_mq_consumer import run_test_case

def consume(ch, method, peoperties, body, send_channel, 
contianer_id, adb_port, appium_port, android_version, device_type, current_status_line,
adb_exe_path, local_apk_root, replay_output_full_path):

    replay_request = jsonpickle.decode(body.decode("utf8"))

    logging.info(f"received!: {replay_request.apkName}")

    run_test_case(adb_port=adb_port,
    appium_port=appium_port,
    replay_request=replay_request,
    channel=send_channel,
    current_status_line=status_line,
    adb_exe_path=adb_exe_path,
    local_apk_root=local_apk_root,
    replay_output_full_path=replay_output_full_path)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    pass

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("err: incorrect number of arguments")
        print("usage: runner.py [status_line]")


    # consts.
    # TODO!
    adb_exe_path = "/home/luzhirui/jerrylu/adb/platform-tools/adb"
    local_apk_root = "/home/luzhirui/google_play_3k/"
    # NOTE: needs to end with /
    replay_output_full_path = "/home/luzhirui/jerrylu/testAppium/replay_0714_mqdebug/"

    # step1. parse the input status line
    status_line = sys.argv[1].strip()
    status_arr = status_line.split(",")

    contianer_id, adb_port, appium_port, android_version, _ ,device_type = status_arr[0:6]
    logging.info(f"contianer_id, adb_port, appium_port, android_version, device_type: {(contianer_id, adb_port, appium_port, android_version, device_type)}")
    adb_port, appium_port = int(adb_port), int(appium_port)  
    log_identifier = f"{android_version}_{device_type}_{contianer_id[0:4]}"

    logging.basicConfig(filename=f"pylog/runner/{log_identifier}.log", level=logging.INFO, format="%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # step2. queues
    # prepare recv/send queue
    # bind send
    recv_connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", heartbeat=0))
    recv_channel = recv_connection.channel()
    recv_channel.exchange_declare(exchange="replay_request",exchange_type="topic")

    send_connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", heartbeat=0))
    send_channel = send_connection.channel()
    send_channel.exchange_declare(exchange="replay_response",exchange_type="topic")

    recv_channel.basic_qos(prefetch_count=1)

    recv_queue_name = f"{android_version}_{device_type}"
    recv_queue = recv_channel.queue_declare(recv_queue_name,durable=True,exclusive=False)
    recv_channel.queue_bind(exchange="replay_request", queue=recv_queue_name, routing_key=f"{android_version}.{device_type}")
    
    # step3. set up callback
    recv_channel.basic_consume(queue=recv_queue_name, 
        on_message_callback=lambda ch, method, peoperties, body: consume(ch, method, peoperties, body, 
        send_channel, contianer_id, adb_port, appium_port, android_version, device_type, status_line,
        adb_exe_path, local_apk_root, replay_output_full_path), 
        auto_ack=False)
    recv_channel.start_consuming()

    pass