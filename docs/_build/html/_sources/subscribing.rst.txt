Subscribing
===========

After a node has subscribed to a topic with ``zerosmq.subscribe(topic)``, it can call ``zerosmq.receive(topic)``
to receive one update from that topic, if an update is available. If there are more updates pending,
you must call ``zerosmq.receive(topic)`` to get them, one at a time. If there are no updates available for that topic,
``zerosmq.receive(topic)`` will return None, which will signal that there are no messages left at the moment.

If you want to receive a message from *any* topic (maybe you just subscribed to a single topic, or you don't care
which topic you receive, maybe for a logger) you may use ``zerosmq.receive_any()``. This function checks
all subscribed topics and returns the first message that it finds, if any.
If none of the subscribed topics have a new message, it returns None.

.. warning::
   If you attempt to call ``zerosmq.receive(topic)`` before calling ``zerosmq.subscribe(topic)``, 
   the node will also stop execution, just as if you attempted to publish before registering.
