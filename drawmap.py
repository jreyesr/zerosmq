import zerosmq
import sys
import time


zerosmq.init(sys.argv[0])
zerosmq.control_socket.send_string("REQUEST_MAP null null")
dotsource=zerosmq.control_socket.recv_string()

from graphviz import Source
s = Source(dotsource, filename="temp.gv", format="png")
s.view()
