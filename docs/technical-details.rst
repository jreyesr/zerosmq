Technical details
=================
.. note::
	(Skipping this section is heavily recommended. Read at your own risk)

ZeROSMQ uses ZeroMQ and its implementation of PUB-SUB sockets to build a publisher-subscriber system.
The master runs a control service on TCP port 5555 by default. Any other nodes connect to it
and request permission to publish or subscribe to a topic. The master responds by creating dedicated sockets
for every topic on a random dynamic port, if required, and sending its port number to the requester.

When a node first requests permission to publish on a certain topic, the master creates a SUB socket
and sends its port number to the node. The node creates a PUB socket, which allows it to send publications to the node.
If another node requests permission to publish on the same node, the master reuses the same socket
(ZeroMQ allows multiple processes to share a socket).

.. warning::
  The master expects that no nodes will subscribe to a topic before at least one node has registered
  for publishing on it. If this rule is not respected, bad things may happen.
  This is the reason for the 1-second delay recommended :ref:`here<registering-for-publications-and-subscribing>`.

When a node first requests permission to subscribe to a topic, the master creates a PUB socket
and sends its port number to the node. The node creates a SUB socket, which enables it to receive messages.
The same reusing of sockets happens here.

The master spends almost all its time (except when it's attending a request from a node) scanning the control socket
for requests and all its open SUB sockets (which correspond to PUB sockets on publisher nodes) for incoming messages.
When a message appears on any SUB socket (which corresponds to a certain topic), the message is copied
to the matching PUB socket (which corresponds to SUB sockets on subscriber nodes), if such socket exists.

In effect, the master acts as a "post exchange". All messages arrive at the master and are forwarded from there.
Queues are handled by ZeroMQ.

The topic graphing code is handled by Graphviz. Graphviz takes files in DOT code
(a certain specialized graph-drawing language that describes all nodes, edges and connections between nodes).
The DOT source code is generated on-the-fly by the master and sent to the client that requested it
(yes, it's horribly hacky, but it appears to work). The client receives the source code
and passes it to the ``graphviz`` library, which accepts raw DOT source code and generates an image from it.
