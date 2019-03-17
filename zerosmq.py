import zmq
from inspect import stack
import re

def log(msg):
    print(f"[{filename}] {msg}")

context=None
control_socket=None
filename=""

pub_topics={}
sub_topics={}

def init(msg_tag,control_port=5555):
    global context, control_socket, filename
    filename=msg_tag
    context = zmq.Context()

    control_socket = context.socket(zmq.REQ)
    control_socket.connect(f"tcp://localhost:{control_port}")

def subscribe(topic):
    global sub_topics
    control_socket.send_string(f"REQUEST_SUB {filename} {topic}")

    response=control_socket.recv_string()
    assigned_port=re.findall("^REQUEST GRANT (\d+)",response)[0]
    assert assigned_port
    sock=context.socket(zmq.SUB)
    sock.setsockopt(zmq.SUBSCRIBE,topic.encode("ascii"))
    sock.connect(f"tcp://localhost:{assigned_port}")

    sub_topics[topic]=(sock,assigned_port)

def unsubscribe(topic):
    global sub_topics

    assert topic in sub_topics, f"Atempted to unsubscribe from topic {topic}, but not subscribed to it"
    control_socket.send_string(f"REQUEST_STOP_SUB {filename} {topic}")

    response=control_socket.recv_string()
    assert response=="REQUEST GRANT", f"Unexpected response: {response}"
    del sub_topics[topic]

def register_publish(topic):
    global pub_topics
    control_socket.send_string(f"REQUEST_PUB {filename} {topic}")

    response=control_socket.recv_string()
    assigned_port=re.findall("^REQUEST GRANT (\d+)",response)[0]
    assert assigned_port, "Expected to receive a port"
    sock=context.socket(zmq.PUB)
    sock.connect(f"tcp://localhost:{assigned_port}")

    pub_topics[topic]=(sock,assigned_port)

def stop_publishing(topic):
    global pub_topics

    assert topic in pub_topics, f"Atempted to stop publishing on topic {topic}, but not registered for it"
    control_socket.send_string(f"REQUEST_STOP_PUB {filename} {topic}")

    response=control_socket.recv_string()
    assert response=="REQUEST GRANT", f"Unexpected response: {response}"
    del pub_topics[topic]

def publish(topic,msg):
    assert topic in pub_topics, f"Attempting to publish on topic {topic} before registering for it"
    pub_topics[topic][0].send_string(f"{topic} {msg}")

def receive(topic):
    assert topic in sub_topics, f"Attempting to receive data from topic {topic} before subscribing to it"
    try:
        msg=sub_topics[topic][0].recv_string(zmq.NOBLOCK)
        return (topic,' '.join(msg.split(' ')[1:]))
    except zmq.ZMQError:
        return None

def receive_any():
    for topic in sub_topics:
        msg=receive(topic)
        if msg:
            return msg
    return None
