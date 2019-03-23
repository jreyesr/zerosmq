.. _graphing-nodes:

Graphing nodes
==============

There is an utility that allows you to graph a network of all nodes, plus any topics that connect them.
It was inspired by `rqt_graph on ROS <http://wiki.ros.org/rqt_graph>`_, minus the nice colors and interactivity.
The file `drawmap.py` contains said utility. To use it:

0. Ensure that you have the ``graphviz`` Python module installed.
1. Run the master node and any other nodes, as usual.
2. When all nodes are up and running, execute ``drawmap.py`` (``python drawmap.py`` or similar).
3. The script should generate and create a PNG image with a map of any nodes and the topics that connect them.
   If you don't see the image, it should be on the same folder, under the name ``temp.gv.png``.
   The file ``temp.gv`` is the `DOT source <https://graphviz.gitlab.io/_pages/doc/info/lang.html>`_ which generated the image, should you want it.

See below for an example diagram. ``pub1`` and ``pub2`` both generate sensor data and send it to ``sub1``. ``sub1``
processes it and publishes the processed data, which is received by ``sub2``. ``sub2`` monitors the processed data and,
if a certain condition is met, will command both ``pub1`` and ``sub1`` to stop their activities, but not ``pub2``.

.. image:: temp.gv.png
