.. ZeROSMQ documentation master file, created by
   sphinx-quickstart on Fri Mar 22 08:09:18 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ZeROSMQ's documentation!
===================================

ZeROSMQ is a Python library that implements ROS-like inter-process communication by using `topics and nodes <https://wiki.ros.org/Topics>`_.
The communications are handled by `ZeroMQ <http://zeromq.org/>`_ in the most inefficient way possible.

ZeROSMQ allows Python programs to pass messages to each other, while at the same time decoupling the implementation of
the different programs. It is especially suited for data collection applications, where a program can read data
from a sensor and broadcast it in real time, so that other, independent programs can receive and process it.

ZeROSMQ's basic usage is as follows:

.. code-block:: python

  # In data publishers
  import zerosmq
  zerosmq.init("publisher")
  zerosmq.register_publish("SOME_TOPIC") # Report intention to publish on topic SOME_TOPIC
  while True:
    data=read_some_sensor()
    zerosmq.publish("SOME_TOPIC",data) # Send the sensor data to the topic
    sleep(1) # Sleep for a second


  # In data subscribers
  import zerosmq
  zerosmq.init("subscriber")
  zerosmq.subscribe("SOME_TOPIC") # Subscribe to SOME_TOPIC to receive any messages sent to it
  while True:
    data=zerosmq.receive("SOME_TOPIC") # Try to receive an update
    if data: # If data is not None, then show it
      print(data)

ZeROSMQ also contains some utilities that aid in debugging and using the library:

* A program that shows a graph of all nodes and how they communicate (see :ref:`graphing-nodes` for more information).
* A program that plots the data sent to a topic or group of topics (see :ref:`plotting-data` for more information).

ZeROSMQ's code is hosted `on GitHub <https://github.com/jreyesr/zerosmq>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   basics
   installation
   usage
   shell-script
   technical-details
   utilities
   example-code
