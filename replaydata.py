## EDIT FOR CONFIGURATION
# RECORDED_FILE: The filename containing a log file generated by recorddata.py
RECORDED_FILE="change-me.txt"
# SPEED: Enables faster/slower playback of data. Set higher than 1 for faster playback.
SPEED = 1.0

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

zerosmq.init(sys.argv[0])

if len(sys.argv)>1:
    RECORDED_FILE=sys.argv[1] # Allow user to pass the recorded file as a command line argument
TOPICS=set() # Will automatically handle the duplicates
with open(RECORDED_FILE) as f:
    for line in f:
        TOPICS.add(line.split(',')[1])

for topic in TOPICS:
    zerosmq.register_publish(topic)

with open(RECORDED_FILE) as f:
    next(millis_gen) # Initialize the millisecond counter
    for line in f:
        chunks=line.strip().split(',')
        while next(millis_gen)*SPEED<float(chunks[0]):
            pass
        zerosmq.publish(chunks[1],chunks[2])
