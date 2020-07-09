from dataclasses import dataclass
from typing import List
import jsonpickle
import sys
import marshmallow_dataclass
import json

sys.path.insert(0,'..')

from mq_replay.docker_replay_mq_replaytask import ReplayRequest

@dataclass
class Hello:
    name: str
    year: int
    t: List[str]


if __name__ == "__main__":
    req = Hello(name="1", year=2020, t=["a","b"])
    body = jsonpickle.encode(req)

    print(body)
    # body = """{"name": "1", "year": 2020, "t": ["a", "b"]}"""

    HelloSchema = marshmallow_dataclass.class_schema(Hello)
    received = HelloSchema().loads(body, unknown="exclude")

    # ReplayRequestSchema = marshmallow_dataclass.class_schema(ReplayRequest)
    # received = ReplayRequestSchema().load(body)

    # received = jsonpickle.decode(body)

    print(received)
    

