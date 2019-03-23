.. _installation:

Installation
============

0. ZeROSMQ has been tested on Python 3.7.1, but it *should* also
   work on Python 3.6 (earlier versions won't work because ZeROSMQ uses `f-strings <https://www.python.org/dev/peps/pep-0498/>`_).
1. ZeROSMQ requires `pyzmq <https://github.com/zeromq/pyzmq>`_.
   If you wish to use :ref:`the graphing tool<graphing-nodes>`, you also need
   to install `graphviz <https://github.com/xflr6/graphviz>`_.
   If you wish to use :ref:`the live plotter<plotting-data>`, you also need to install `pyqtgraph <http://www.pyqtgraph.org/>`_.
   It is highly recommended to install `GNU Parallel <https://www.gnu.org/software/parallel/>`_ for sanity-preservation purposes:
   you can run all nodes with a single shell script, in parallel, get all outputs in the same window, and
   close them with a single ``Ctrl+C``. See :ref:`the "Shell script"<shell-script>` section for details on the recommended shell script.
2. Copy the ``zerosmq.py`` and ``zerosmq-master.py`` files to a folder of your choice.
   If you want to graph the nodes, also copy ``drawmap.py``. If you want to plot any topic, also copy ``plotdata.py``.
3. Add any nodes that you want to the same folder. See :ref:`Usage<usage>` for the code that you should use in the nodes.
4. Run the master node (``python zerosmq-master.py`` or similar) and any other nodes (``python <your-node>.py``).
   If you have :ref:`GNU Parallel and a shell script<shell-script>`, execute ``./run.sh`` instead
   (assuming your shell script is called ``run.sh``).
