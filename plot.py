import numpy as np
import pyqtgraph as pg
import os, sys
import signal

from PyQt4 import QtCore, QtGui
from time import sleep
from collections import deque

import visa

def create_device():
    rm = visa.ResourceManager('@py')
    device_name = rm.list_resources()[0]

    dev = rm.open_resource(device_name, read_termination='\r',
                            send_end=True, baud_rate=19200)

    dev.write("*rst; status:preset; *cls")
    print "Reading Device: " + dev.query('*IDN?')

    dev.write(":SENSE:FUNCTION 'VOLT:DC'")
    dev.write(":FORMAT:ELEMENT READ")
    dev.write(":SYSTEM:AZERO:STATE OFF")
    dev.write(":SENSE:VOLT:DC:AVERAGE:STATE OFF")
    dev.write(":SENSE:VOLT:DC:NPLC 0.01")
    dev.write(":SENSE:VOLT:DC:RANGE 10")
    dev.write(":SENSE:VOLT:DC:DIGITS 4")
    dev.write(":TRIGGER:COUNT 1")
    dev.write(":SAMPLE:COUNT 1")
    dev.write(":TRIGGER:DELAY 0.0")
    dev.write(":DISP:ENABLE 0")
    return dev


class MainApp(QtGui.QWidget):
    def __init__(self, parent=None, device = None):
        super(MainApp, self).__init__()
        self.__initUI__()

    def __initUI__(self):

        self.hbox = QtGui.QHBoxLayout(self)
        self.plot = pg.PlotWidget()
        self.hbox.addWidget(self.plot)

        self.setLayout(self.hbox)
        self.setGeometry(500,500,1000,500)

        self.N = 100
        self.data = deque([0]*self.N, maxlen=self.N)

        self.x = np.arange(self.N)

        self.curve = self.plot.plot(self.data)

        self.show()
        self.device = device

    def update(self):
        if device:
            results = dev.ask('READ?').split('#,')
            results = [x.split(',')[0] for x in results]
            self.data.append(results)
        else:
            self.data.append(np.random.rand())
        self.curve.setData(self.x, self.data)


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication([])
    m = MainApp()
    t = QtCore.QTimer()
    t.timeout.connect(m.update)
    t.start(50) #QTimer takes ms
    app.exec_()

if __name__=='__main__':
    main()
