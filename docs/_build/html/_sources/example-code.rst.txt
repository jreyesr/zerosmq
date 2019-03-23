.. _example-code:

Example code
============

There is some example code in the ``examples/`` directory. The code implements two publisher nodes and two
subscriber nodes. The two publisher nodes (``pub1.py`` and ``pub2.py``) simulate two redundant sensors which measure
the same value. Since no actual sensors are present, the values are randomized. Both nodes publish data
on topic SENSOR_DATA. The first subscriber node (``sub1.py``) processes the value (it multiplies it by two)
and publishes the "processed data" on topic PROCESSED_DATA. The second subscriber node (``sub2.py``) reads the
processed data. If the processed data has a value over 3 (maybe an overrange condition?) it sends back a signal
on the topic COMMANDS, which orders nodes to stop data collection. Nodes ``pub1.py`` and ``sub1.py`` listen to this order.
Node ``pub2.py`` doesn't listen to it, so it continues generating data after the first publisher has stopped.

When you run ``./run.sh`` on the ``examples/`` directory, you will see all nodes subscribing and registering for publication.
After that, you will see nodes ``pub1.py`` and ``pub2.py`` printing their "sensor data" and sending it to the same topic
(SENSOR_DATA). ``sub1.py`` will print its received data. ``sub2.py`` will print all received data and, if necessary,
send the stop signal. When the stop signal is sent, ``pub1.py`` (identified as Sensor A) and ``sub1.py`` will stop
operations. ``pub2.py`` (identified as Sensor B) will continue generating data, but ``sub1.py`` will no longer process it.

At any moment, you can call ``python ../drawmap.py`` from the ``examples/`` folder to create the topic map. Both the
source code and the image are included.

Also, you can call ``python ../plotdata.py`` from the ``examples/`` folder (after editing the file so that TOPICS
contains only the SENSOR_DATA topic) to plot the data sent by the fake sensors.
