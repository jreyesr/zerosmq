import sys
sys.path.append("..") # HACK: Allow importing zerosmq.py from parent folder

import zerosmq
import random

zerosmq.init(sys.argv[0])
zerosmq.register_publish("SENSOR_DATA")
zerosmq.register_publish("ANOTHER_TOPIC")

import time
while True:
    data=random.random()+1

    zerosmq.log(f"Got {data} from sensor B")
    zerosmq.publish("SENSOR_DATA",data)
    time.sleep(1.4)
