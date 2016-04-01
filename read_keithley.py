import visa
import numpy as np
import time

import matplotlib
import matplotlib.animation as animation
matplotlib.use('Qt4Agg')


from collections import deque
import matplotlib.pyplot as plt

def main():
    rm = visa.ResourceManager('@py')
    device_name = rm.list_resources()[0]

    dev = rm.open_resource(device_name, read_termination='\r', send_end=True, baud_rate=19200)

    #print dev.query('*RST')
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

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    N = 50
    data = deque([0]*N, maxlen=N)

    line, = plt.plot(data, 'bo')
    ax1.set_ylim(-1, 6)

    def animate(i):
        results = dev.ask('READ?').split('#,')
        results = [x.split(',')[0] for x in results]
        new_data = [float((x.split('VDC')[0][1:])) for x in results]
        data.extend(new_data)
        line.set_ydata(data)

    ani = animation.FuncAnimation(fig, animate, frames=20)
    plt.show()

if __name__=='__main__':
    main()

