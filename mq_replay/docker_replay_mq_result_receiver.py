# result_receiver: 把 replay_response 队列中存储的结果写入文件

from enum import auto
import json
import logging
import base64
from pathlib import Path
import re
import sys

import pika
import jsonpickle

sys.path.insert(0,'..')

from mq_replay.docker_replay_mq_replaytask import *
# const.
replay_output_path = Path("/home/luzhirui/jerrylu/testAppium/replay/output")
enable_real_write = False


def callback(ch, method, peoperties, body):

    replay_response : ReplayResponse = jsonpickle.decode(body.decode("utf8"))
    write_name = replay_response.testcaseSummary.writeName

    logging.info(f"received: {write_name}")

    if enable_real_write:
        output_root = replay_output_path
        with open(output_root / "replay_screenshots" / f"{write_name}.png", "wb") as screenshot_file:
            screenshot_file.write(base64.b64decode(replay_response.imgBase64))
        with open(output_root / "replay_page_sources" / f"page_source_{write_name}.xml", "w") as xml_file:
            xml_file.write(replay_response.pageSource)
        with open(output_root / "replay_adb" / f"adblog_{write_name}.json", "w") as json_file:
            json_file.write(replay_response.adbLog)


    ch.basic_ack(delivery_tag=method.delivery_tag)
    pass

if __name__ == "__main__":
    
    # pre. setup logging
    logging.basicConfig(filename="pylog/receiver.log", level=logging.INFO, format="%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    recv_connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", heartbeat=0))
    recv_channel = recv_connection.channel()
    recv_channel.exchange_declare(exchange="replay_response",exchange_type="topic")

    recv_queue_name = "all_receive"
    recv_queue = recv_channel.queue_declare(recv_queue_name,durable=True,exclusive=False)
    recv_channel.queue_bind(exchange="replay_response", queue=recv_queue_name, routing_key="#")

    recv_channel.basic_consume(queue=recv_queue_name, on_message_callback=callback,auto_ack=False)

    recv_channel.start_consuming()
    
    
    pass