Publishing
==========

After registering for publication on a specific topic with ``zerosmq.register_publish(topic)``,
you may use ``zerosmq.publish(topic,message)`` to send a message to all nodes that subscribed to that topic.
The same warnings about single words on topics apply here. Messages must be strings
(there is no automatic type conversion like in ROS, or at least not yet). Messages can have spaces, though.
There is no length limitation.

.. warning::
   If you attempt to call ``zerosmq.publish(topic,message)`` before calling ``zerosmq.register_publish(topic)``,
   the node will stop execution because of an AssertionError.
