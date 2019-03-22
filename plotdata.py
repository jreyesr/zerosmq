## EDIT FOR CONFIGURATION
# TIME_SPAN: Sets the length of the full plot in seconds
TIME_SPAN=5
# TOPICS: Specifies which topics will be watched
TOPICS=["BARO","BARO_AVG"]

## EDITS NOT REQUIRED FROM NOW ON
COLORS=['#009933','r','b']

import zerosmq
import sys
from time import sleep
import GS_timing
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

zerosmq.init(sys.argv[0])
sleep(1)
for t in TOPICS:
    zerosmq.subscribe(t)

def millis():
    start_time=GS_timing.millis()
    while True:
        yield GS_timing.millis()-start_time
millis_gen=millis()

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle(f'{", ".join(TOPICS)} monitor')

plt = win.addPlot()
#plt.setAutoVisibleOnly(y=True)
plt.setLabels(bottom="seconds",left=", ".join(TOPICS))
plt.addLegend()
curves = []
for i,t in enumerate(TOPICS):
    curves.append(plt.plot(pen=pg.mkPen(COLORS[i%len(COLORS)], width=1),name=t))
datas = [[] for _ in curves]
def update():
    global curves, datas
    for i,t in enumerate(TOPICS):
        msg=zerosmq.receive(t)
        if msg or datas[i]:
            datas[i].append((next(millis_gen)/1000,float(msg[1]) if msg else datas[i][-1][1]))
        while datas[i] and (next(millis_gen)/1000-datas[i][0][0])>TIME_SPAN:
            datas[i].pop(0)
        curves[i].setData(np.array(datas[i]))

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
