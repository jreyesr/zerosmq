Basics
======

Just like in ROS, a "node" is a program (in ZeROSMQ, a Python script) that communicates with other nodes. A "topic" is
a pipe over which nodes can exchange information. Topics follow the publisher-subscriber pattern. Many nodes can request
permission to publish on a certain topic, and many nodes can subscribe to the same topic, which enables them to receive
any messages sent by any publisher on that topic. All communications are handled by a "master" node, running on a
well-known port, which must be running before any other nodes.

For installation instructions, jump :ref:`here<installation>`.
For usage instructions, jump :ref:`here<usage>`. If you want to see an example, go :ref:`here<example-code>`.
