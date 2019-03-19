import sys
sys.path.append("..") # HACK: Allow importing zerosmq.py from parent folder

import zerosmq
import time

zerosmq.init(sys.argv[0])
zerosmq.register_publish("COMMANDS")

time.sleep(1)
zerosmq.subscribe("PROCESSED_DATA")

while True:
    message=zerosmq.receive("PROCESSED_DATA")
    if message:
        zerosmq.log(f"Received data {message[1]} from processor")
        if float(message[1])>3:
            zerosmq.log("Data too high! Stopping processor")
            zerosmq.publish("COMMANDS","STOP")
