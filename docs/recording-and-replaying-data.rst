.. _recording-and-replaying-data:

Recording and replaying data
============================

ZeROSMQ contains code to record all published data (or a subset of it) to a file, and allow its playback later, which will produce the same
effects as when the data was obtained the first time. It is inspired by
`ROS's bags <https://wiki.ros.org/ROS/Tutorials/Recording%20and%20playing%20back%20data>`_, and contained in the files
``recordddata.py`` and ``replaydata.py``. Furthermore, the speed at which data is replayed can be configured.

Recording data
--------------

To record data:

1. Open the ``recorddata.py`` file. The variable TOPICS at the top controls which topics will be recorded (for example,
   if a node subscribes to topic A, processes its data and publishes the processed data on topic B, you may not want to
   record B, since when you play back the data messages of topic B will appear twice, once from the recorded data and
   once from the node's processing of topic A's recorded data). If you wish to record all data, leave TOPICS as it is.
2. Save the ``recorddata.py`` file.
3. Run the master node and any other nodes, as usual.
4. When you wish to start recording data, execute ``recorddata.py`` (``python recorddata.py`` or similar).
5. A file called "RecordData_thecurrentdate.txt" will be created ("thecurrentdate" is the *actual* current date).

Replaying data
--------------

To replay recorded data:

1. Open the ``replaydata.py`` file and edit the variable RECORDED_FILE, at the top, to contain the filename of the recording
   that you want to play back. If you want to have faster/slower playback, set the SPEED variable. A value of
   1.0 will cause real-time playback. Higher values will cause faster playback, and slower values will cause slower
   playback. A value of 0 would completely stop playback.

.. warning::
   The maximum speed-up achievable depends on your computer (or so it appears). I haven't been able to obtain a speed-up
   greater than 2 or so, and at that speed the script spends its entire time sending data, with no pauses. Further speed-ups
   are desired, so feel free to add them in if you can.

.. note::
   You can also set the file name by passing it as a console argument to ``replaydata.py`` (``python replaydata.py yourfilename.txt``).
   If you do so, you don't need to edit ``replaydata.py``.

2. Save the ``replaydata.py`` file.
3. Run the master node and any **data processing** nodes (don't run data generators).

.. warning::
   When playing back data, ensure that you don't execute any nodes that publish on any topics that you recorded. If
   you do so, you will get duplicated data. You can only record sensor data (if you are doing a data acquisition project)
   and delay all data processing to the playback stage. Otherwise, you can record all topics (sensor data and processed data),
   but you shouldn't run the data processors on the playback stage.

4. Run the ``replaydata.py`` file (``python replaydata.py`` or similar).
5. The ``replaydata`` node will scan the file, find all recorded topics, register for publication on all of them and
   publish all saved messages. Any listening nodes will experience the same effect as if the real data generators were publishing.
