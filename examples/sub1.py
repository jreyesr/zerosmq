import sys
sys.path.append("..") # HACK: Allow importing zerosmq.py from parent folder

import zerosmq
import time

zerosmq.init(sys.argv[0])
zerosmq.register_publish("PROCESSED_DATA")
time.sleep(1)
zerosmq.subscribe("SENSOR_DATA")
zerosmq.subscribe("COMMANDS")

stopped=False
while True:
    message=zerosmq.receive_any()
    if not message:
        continue
    if message[0]=="SENSOR_DATA" and not stopped:
        zerosmq.log(f"Received data {message[1]} from sensor. Processing...")
        zerosmq.publish("PROCESSED_DATA",2*float(message[1]))
    elif message[0]=="COMMANDS" and message[1]=="STOP":
        zerosmq.log(f"Received stop command! Ending data processing")
        stopped=True
