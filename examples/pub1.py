import sys
sys.path.append("..") # HACK: Allow importing zerosmq.py from parent folder

import zerosmq
import random
import time

zerosmq.init(sys.argv[0])
zerosmq.register_publish("SENSOR_DATA")
zerosmq.register_publish("ANOTHER_TOPIC")
time.sleep(1)
zerosmq.subscribe("COMMANDS")

import time
while True:
    message=zerosmq.receive("COMMANDS")
    if message and message[1]=="STOP":
        zerosmq.log("Emergency stop! Ending data collection")
        break

    data=random.random()+1

    zerosmq.log(f"Got {data} from sensor A")
    zerosmq.publish("SENSOR_DATA",data)
    time.sleep(1)
