.. _registering-for-publications-and-subscribing:

Registering for publications and subscribing
============================================
You need to register for publications before you can publish on a certain topic.
To do so, call ``zerosmq.register_publish("SOME_TOPIC")``, replacing SOME_TOPIC by a more appropriate label.

.. warning::
	**Labels must be a single word!**

If your label has spaces, replace them by underscores or delete them. In its present form, ZeROSMQ makes no effort
whatsoever to ensure that topics have a single word, and ZeroMQ expects topics to have a single word,
so it is your job to ensure it.

You also need to subscribe to a topic before you receive updates for it. To do so, call ``zerosmq.subscribe("SOME_TOPIC")``,
replacing SOME_TOPIC with the desired topic. The same warning applies regarding whitespace and single words.

Note: it is recommended to register for all publications first, then wait for a while, and then subscribe.
This gives the master time to process all registrations. You can do so, for example, by calling ``import time``
and then calling ``time.sleep(1)`` between ``zerosmq.register_publish()`` calls and ``zerosmq.subscribe()``
calls (obviously, you must order them so that ``zerosmq.register_publish()`` calls appear first). This sleeps the node 
for one second and gives any other nodes time to announce their own publications.
