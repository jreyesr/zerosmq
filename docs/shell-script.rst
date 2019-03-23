.. _shell-script:

Shell script
============

If you installed GNU Parallel, you can run all nodes from a single shell script, and get all their outputs
on the same console. This saves time and effort, since you would typically have multiple consoles open,
one for each node. This route will probably not work if a node needs input or otherwise interacts with the user,
but it works fine for the standard "data collection into data processing into data output/logging"
workflow that tends to happen in ROS.

To run all nodes from a single script, do the following:

1. Create a shell script. Name it however you want (this documentation will use ``run.sh``)
2. Write the following line in the script:

.. code-block:: bash

   parallel --ungroup --jobs 0 python ::: ../zerosmq-master.py <your-first-node.py> <your-second-node.py> <your-third-node.py>

3. (Of course, you should change ``<your-first-node.py>`` for your actual first node, and so on).
4. There is no limit to the number of nodes (well, there probably is, but I haven't found it yet).
   You may need to change the Python interpreter to ``python3.7`` or similar, if you have more interpreters.
5. All nodes will run on a single console window. The output from all nodes will appear on it
   (that's why you should *really* use the ``log(msg)`` function provided with the library, instead of ``print()``).
   If you press ``Ctrl+C``, all nodes will be stopped, including the master node.
