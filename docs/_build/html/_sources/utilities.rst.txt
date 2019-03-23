Utilities
=========

ZeROSMQ contains several utilities that help development and data visualization:

* By default, the master runs its control service on port TCP 5555.
  If you don't want to use it (maybe it's already taken, or maybe it's blocked) you can change it:
  in the master, find the call to ``init()``, at the end, and override the default port (``init(12345)``, for example).
  This will start the master on your custom port. After that, on all nodes, you need to also override the port
  in the ``zerosmq.init('TAG')`` call, by changing it to ``zerosmq.init('TAG', 12345)``.
* There is a logging function that uses the tag that you passed to ``zerosmq.init()``.
  To use it, call ``zerosmq.log('some message')`` from anywhere in your code, after ``zerosmq.init()``.
  This will print the message that you passed, plus a tag at the beginning to help you distinguish it from other nodes' messages.
* There are ``zerosmq.unsubscribe('topic')`` and ``zerosmq.stop_publishing('topic')`` functions,
  which stop a subscription and publications in a given topic, respectively.

.. warning::
  These functions are not tested. Use at your own risk.

* There is a graphing utility which creates an image showing all nodes and their communications.
  It is described :ref:`here<graphing-nodes>`.
* There is also a plotting utility which can show a graph of any topic or set of topics, in real time.
  It is described :ref:`here<plotting-data>`.

.. toctree::
   :maxdepth: 1
   :caption: Utilities

   graphing-nodes
   plotting-data
