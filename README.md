# ZeROSMQ

ZeROSMQ is a Python library that implements ROS-like inter-process communication by using ["topics" and "nodes"](https://wiki.ros.org/Topics).
The communications are handled by [ZeroMQ](http://zeromq.org/) in the most inefficient way possible.

## Basics
Just like in ROS, a "node" is a program (in ZeROSMQ, a Python script) that communicates with other nodes. A "topic" is
a pipe over which nodes can exchange information. Topics follow the publisher-subscriber pattern. Many nodes can request
permission to publish on a certain topic, and many nodes can subscribe to the same topic, which enables them to receive
any messages sent by any publisher on that topic. All communications are handled by a "master" node, running on a
well-known port, which must be running before any other nodes.

For installation instructions, jump [here](#installation). For usage instructions, jump [here](#usage).

## Installation
0. ZeROSMQ has been tested on Python 3.7.1, but it _should_ also
work on Python 3.6 (earlier versions won't work because ZeROSMQ uses [f-strings](https://www.python.org/dev/peps/pep-0498/)).
1. ZeROSMQ requires [pyzmq](https://github.com/zeromq/pyzmq). If you wish to use [the graphing tool](#graphing-nodes-and-topics), you also need
to install [graphviz](https://github.com/xflr6/graphviz). It is highly recommended to install [GNU Parallel](https://www.gnu.org/software/parallel/) for sanity-preservation purposes: you can run all nodes with a single shell script, in parallel, get all outputs in the same window, and close them with a single `Ctrl+C`. See [the "Shell script"](#shell-script) section for details on the recommended shell script.
2. Copy the `zerosmq.py` and `zerosmq-master.py` files to a folder of your choice. If you want to graph the nodes, also copy `drawmap.py`.
3. Add any nodes that you want to the same folder. See [Usage](#usage) for the code that you should use in the nodes.
4. Run the master node (`python zerosmq-master.py` or similar) and any other nodes (`python <your-node>.py`). If you have [GNU Parallel and a shell script](#shell-script), execute `./run.sh` instead (assuming your shell script is called `run.sh`).

## Usage
The master node is already provided and you should not need to alter it. The rest of the work should happen in your own nodes.
### Initialization
You will need to `import zerosmq` in your nodes. After that, you should call `zerosmq.init(LABEL)`, replacing LABEL by a string which  will appear on any message sent by that node to `log(msg)`. LABEL should be different for each node. You can use `sys.argv[0]` for LABEL, which will tag messages with the filename of the script (note that this will not work as intended if you run multiple instances of the same script in parallel).
### Registering for publications and subscribing
You need to register for publications before you can publish on a certain topic. To do so, call `zerosmq.register_publish("SOME_TOPIC")`, replacing SOME_TOPIC by a more appropriate label. **Labels must be a single word!** If your label has spaces, replace them by underscores or delete them. In its present form, ZeROSMQ makes no effort whatsoever to ensure that topics have a single word, and ZeroMQ expects topics to have a single word, so it is your job to ensure it.

You also need to subscribe to a topic before you receive updates for it. To do so, call `zerosmq.subscribe("SOME_TOPIC")`, replacing SOME_TOPIC with the desired topic. The same warning applies regarding whitespace and single words.

Note: it is recommended to register for all publications first, then wait for a while, and then subscribe. This gives the master time to process all registrations. You can do so, for example, by calling `import time` and then calling `time.sleep(1)` between `zerosmq.register_publish()` calls and `zerosmq.subscribe()` calls (obviously, you must order them so that `zerosmq.register_publish()` calls appear first). This sleeps the node for one second and gives any other nodes time to announce their own publications.

### Publishing
After registering for publication on a specific topic with `zerosmq.register_publish(topic)`, you may use `zerosmq.publish(topic,message)` to send a message to all nodes that subscribed to that topic. The same warnings about single words on topics apply here. Messages must be strings (there is no automatic type conversion like in ROS, or at least not yet). Messages can have spaces, though. There is no length limitation.

If you attempt to call `zerosmq.publish(topic,message)` before calling `zerosmq.register_publish(topic)`, the node will ~~fail catastrophically and destroy Earth~~ stop execution because of an AssertionError.

### Subscribing
After a node has subscribed to a topic with `zerosmq.subscribe(topic)`, it can call `zerosmq.receive(topic)` to receive one update from that topic, if an update is available. If there are more updates pending, you must call `zerosmq.receive(topic)` to get them, one at a time. If there are no updates available for that topic, `zerosmq.receive(topic)` will return None, which will signal that there are no messages left at the moment.

If you want to receive a message from _any_ topic (maybe you just subscribed to a single topic, or you don't care which topic you receive, maybe for a logger) you may use `zerosmq.receive_any()`. This function checks all subscribed topics and returns the first message that it finds, if any. If none of the subscribed topics have a new message, it returns None.

If you attempt to call `zerosmq.receive(topic)` before calling `zerosmq.subscribe(topic)`, the node will ~~also fail catastrophically and destroy Earth~~ also stop execution, just as if you attempted to publish before registering.

### Utilities
* By default, the master runs its control service on port TCP 5555. If you don't want to use it (maybe it's already taken, or maybe it's blocked) you can change it: in the master, find the call to `init()`, at the end, and override the default port (`init(12345)`, for example). This will start the master on your custom port. After that, on all nodes, you need to also override the port in the `zerosmq.init('TAG')` call, by changing it to `zerosmq.init('TAG', 12345)`.
* There is a logging function that uses the tag that you passed to `zerosmq.init()`. To use it, call `zerosmq.log('some message')` from anywhere in your code, after `zerosmq.init()`. This will print the message that you passed, plus a tag at the beginning to help you distinguish it from other nodes' messages.
* There are `zerosmq.unsubscribe('topic')` and `zerosmq.stop_publishing('topic')` functions, which stop a subscription and publications in a given topic, respectively. (WARNING: Untested! Use at your own risk!)
* There is a graphing utility which creates an image showing all nodes and their communications. It is described [here](#graphing-nodes-and-topics).

## Shell script
If you installed GNU Parallel, you can run all nodes from a single shell script, and get all their outputs on the same console. This saves time and effort, since you would typically have multiple consoles open, one for each node. This route will probably not work if a node needs input or otherwise interacts with the user, but it works fine for the standard "data collection into data processing into data output/logging" workflow that tends to happen in ROS.

To run all nodes from a single script, do the following:
1. Create a shell script. Name it however you want (this documentation will use `run.sh`)
2. Write the following line in the script:
> parallel --ungroup --jobs 0 python ::: ../zerosmq-master.py &lt;your-first-node.py&gt; &lt;your-second-node.py&gt; &lt;your-third-node.py&gt;

3. (Of course, you should change `<your-first-node.py>` for your actual first node, and so on). There is no limit to the number of nodes (well, there probably is, but I haven't found it yet). You may need to change the Python interpreter to `python3.7` or similar, if you have more interpreters.
4. All nodes will run on a single console window. The output from all nodes will appear on it (that's why you should _really_ use the `log(msg)` function provided with the library, instead of `print()`). If you press `Ctrl+C`, all nodes will be stopped, including the master node.


## Graphing nodes and topics
There is an utility that allows you to graph a network of all nodes, plus any topics that connect them. It was inspired by [rqt_graph on ROS](http://wiki.ros.org/rqt_graph), minus the nice colors and interactivity. The file `drawmap.py` contains said utility. To use it:
0. Ensure that you have the `graphviz` Python module installed.
1. Run the master node and any other nodes, as usual.
2. When all nodes are up and running, execute `drawmap.py` (`python drawmap.py` or similar).
3. The script should generate and create a PNG image with a map of any nodes and the topics that connect them. If you don't see the image, it should be on the same folder, under the name `temp.gv.png`. The file `temp.gv` is the [DOT source](https://graphviz.gitlab.io/_pages/doc/info/lang.html) which generated the image, should you want it.

## Technical details
(Skipping this section is heavily recommended. Read at your own risk)

ZeROSMQ uses ZeroMQ and its implementation of PUB-SUB sockets to build a publisher-subscriber system. The master runs a control service on TCP port 5555 by default. Any other nodes connect to it and request permission to publish or subscribe to a topic. The master responds by creating dedicated sockets for every topic on a random dynamic port, if required, and sending its port number to the requester.

When a node first requests permission to publish on a certain topic, the master creates a SUB socket and sends its port number to the node. The node creates a PUB socket, which allows it to send publications to the node. If another node requests permission to publish on the same node, the master reuses the same socket (ZeroMQ allows multiple processes to share a socket).

(Note: The master expects that no nodes will subscribe to a topic before at least one node has registered for publishing on it. If this rule is not respected, bad things may happen. This is the reason for the 1-second delay recommended [above](#registering-for-publications-and-subscribing))

When a node first requests permission to subscribe to a topic, the master creates a PUB socket and sends its port number to the node. The node creates a SUB socket, which enables it to receive messages. The same reusing of sockets happens here.

The master spends almost all its time (except when it's attending a request from a node) scanning the control socket for requests and all its open SUB sockets (which correspond to PUB sockets on publisher nodes) for incoming messages. When a message appears on any SUB socket (which corresponds to a certain topic), the message is copied to the matching PUB socket (which corresponds to SUB sockets on subscriber nodes), if such socket exists.

In effect, the master acts as a "post exchange". All messages arrive at the master and are forwarded from there. Queues are handled by ZeroMQ.
