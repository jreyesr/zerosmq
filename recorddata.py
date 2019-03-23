## EDIT FOR CONFIGURATION
# TOPICS: The topics to record. Leave empty to record all topics
TOPICS=[]

## EDITS NOT REQUIRED FROM NOW ON
import zerosmq
import sys
from time import sleep, ctime
import GS_timing

def millis():
    start_time=GS_timing.millis()
    while True:
        yield GS_timing.millis()-start_time
millis_gen=millis()
next(millis_gen)

zerosmq.init(sys.argv[0])

sleep(1)

if not TOPICS:
    TOPICS=zerosmq.get_list_of_topics()

for topic in TOPICS:
    zerosmq.subscribe(topic)

with open("RecordData_"+ctime().replace(" ","_")+".txt", "w") as f:
    try:
        while True:
            msg=zerosmq.receive_any()
            if msg:
                f.write(f"{next(millis_gen)},{msg[0]},{msg[1]}\r\n")
    except KeyboardInterrupt:
        print("Ending data collection")
