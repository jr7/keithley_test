import numpy as np
import pyqtgraph as pg
import os, sys
import signal
import time

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

    """
    dev.write(":SENSE:FUNCTION 'VOLT:DC'")
    dev.write(":FORMAT:ELEMENT READ")
    dev.write(":SYSTEM:AZERO:STATE OFF")
    dev.write(":SENSE:VOLT:DC:AVERAGE:STATE OFF")
    dev.write(":SENSE:VOLT:DC:NPLC 10")
    dev.write(":SENSE:VOLT:DC:RANGE 10")
    dev.write(":SENSE:VOLT:DC:DIGITS 4")
    dev.write(":TRIGGER:COUNT 1")
    dev.write(":SAMPLE:COUNT 1")
    dev.write(":TRIGGER:DELAY 0.0")
    dev.write(":DISP:ENABLE 1")
    """
    dev.write(":SENSE:FUNCTION 'RES'")
    dev.write(":FORMAT:ELEMENT READ")
    dev.write(":SYSTEM:AZERO:STATE OFF")

    dev.write(":SENSE:RES:AVERAGE:TCONT MOV")
    dev.write(":SENSE:RES:NPLC 10")

    dev.write(":SENSE:RES:RANGE 100000")
    dev.write(":SENSE:RES:DIGITS 4")

    dev.write(":TRIGGER:COUNT 1")
    dev.write(":SAMPLE:COUNT 1")
    dev.write(":TRIGGER:DELAY 0.0")
    dev.write(":DISP:ENABLE 1")

    return dev


class MainApp(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainApp, self).__init__()
        self.__initUI__()

    def __initUI__(self):

        self.datafile =  open(sys.argv[1], 'w')
        self.datafile.write("#Voltage : Time : Position\n")
        self.hbox = QtGui.QVBoxLayout(self)
        self.plot = pg.PlotWidget()

        self.field = QtGui.QSpinBox()
        self.position  = 0
        self.field.valueChanged[int].connect(self.set_position)

        self.hbox.addWidget(self.field)
        self.hbox.addWidget(self.plot)
        self.setLayout(self.hbox)
        self.setGeometry(500,500,1000,500)

        self.device = create_device()
        self.N = 200
        self.data = deque([0]*self.N, maxlen=self.N)
        self.x = np.arange(self.N)
        self.curve = self.plot.plot(self.data)
        self.show()

    def set_position(self, value):
        self.position = value

    def update(self):
        if self.device is not None:
            now = time.time()
            results = self.device.ask('READ?').split(',')[0]
            results = float(results[1:-3])

            dt = time.time() - now
            print   "Ohm: {} : Time : {} : Position : {}".format(results, time.time() -now, self.position)
            output =  "{} \t {} \t {}".format(results, time.time() -now, self.position)

            self.datafile.write(output + '\n')
            self.datafile.flush()
            self.data.append(results)
        else:
            self.data.append(np.random.rand())
        self.curve.setData(self.x, self.data)


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication([])
    dev = create_device()
    m = MainApp()
    t = QtCore.QTimer()
    t.timeout.connect(m.update)
    t.start(50) #QTimer takes ms
    app.exec_()
    m.datafile.close()

if __name__=='__main__':
    main()
