import zmq
import sys

def log(msg):
    print(f"[{filename}] {msg}")

publishers={}
subscribers={}

context=None
control_socket=None

def init(control_port=5555):
    global context, control_socket
    context = zmq.Context()

    control_socket = context.socket(zmq.REP)
    control_socket.bind("tcp://*:%d" % control_port)

def process_control_msg(msg):
    global publishers, subscribers
    msg=msg.strip().split(" ")
    assert len(msg)==3, "Malformed message {msg}"

    node_id=msg[1]
    topic=msg[2]

    if msg[0]=="REQUEST_PUB":
        log(f"{node_id} publishes on topic {topic}")
        if topic in publishers:
            publishers[topic][2].append(node_id)
            portnumber=publishers[topic][1]
        else:
            sock=context.socket(zmq.SUB)
            portnumber=sock.bind_to_random_port("tcp://*")
            sock.setsockopt(zmq.SUBSCRIBE,topic.encode("ascii"))
            publishers[topic]=(sock,portnumber,[node_id])
        control_socket.send_string(f"REQUEST GRANT {portnumber}")
    elif msg[0]=="REQUEST_SUB":
        log(f"{node_id} subscribed to topic {topic}")
        if topic in subscribers:
            subscribers[topic][2].append(node_id)
            portnumber=subscribers[topic][1]
        else:
            sock=context.socket(zmq.PUB)
            portnumber=sock.bind_to_random_port("tcp://*")
            subscribers[topic]=(sock,portnumber,[node_id])
        control_socket.send_string(f"REQUEST GRANT {portnumber}")
    elif msg[0]=="REQUEST_STOP_PUB":
        log(f"{node_id} stops publishing on topic {topic}")
        assert topic in publishers, f"No nodes are publishing on {topic}"
        assert node_id in publishers[topic][2], f"{node_id} was not publishing on {topic}"

        publishers[topic][2].remove(node_id)
    elif msg[0]=="REQUEST_STOP_SUB":
        log(f"{node_id} unsubscribes from topic {topic}")
        assert topic in subscribers, f"No nodes are subscribed to {topic}"
        assert node_id in subscribers[topic][2], f"{node_id} was not subscribed to {topic}"

        subscribers[topic][2].remove(node_id)
    elif msg[0]=="REQUEST_MAP":
        log(f"Printing topic map")
        string="""digraph G {
        edge [dir=forward, fontsize=8]
        node [shape=ellipse]
"""
        nodes=[]
        for topic in publishers:
            for publisher in publishers[topic][2]:
                if publisher not in nodes:
                    string+=f'\t{publisher.split(".")[0]} [label="{publisher.split(".")[0]}"]\n'
                    nodes.append(publisher)
        for topic in subscribers:
            for subscriber in subscribers[topic][2]:
                if subscriber not in nodes:
                    string+=f't{subscriber.split(".")[0]} [label="{suscriber.split(".")[0]}"]\n'
                    nodes.append(subscriber)
        for topic in publishers:
            for publisher in publishers[topic][2]:
                for subscriber in subscribers.get(topic, (None,None,[]))[2]:
                    string+=f'\t{publisher.split(".")[0]} -> {subscriber.split(".")[0]} [label="{topic.lower()}"]\n'

        string+="}"
        control_socket.send_string(string)


import time
def run():
    while True:
        try:
            process_control_msg(control_socket.recv_string(zmq.NOBLOCK))
        except zmq.ZMQError:
            pass

        for topic in publishers:
            try:
                message=publishers[topic][0].recv_string(zmq.NOBLOCK)
                if topic in subscribers:
                    subscribers[topic][0].send_string(f"{message}")
            except zmq.ZMQError:
                pass

if __name__ == '__main__':
    filename=sys.argv[0]
    init()
    run()
