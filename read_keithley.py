import visa
import numpy as np
import time
import matplotlib
import matplotlib.animation as animation
matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt

def main():
    rm = visa.ResourceManager('@py')
    device_name = rm.list_resources()[0]

    dev = rm.open_resource(device_name, read_termination='\r', send_end=True)

    print dev.query('*IDN?')

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    data = []
    def animate(i):
        time.sleep(0.1)
        d = float((dev.ask('READ?').split('VDC')[0][1:]))

        data.append(d)
        x = np.arange(len(data))
        ax1.clear()
        ax1.plot(x, data, 'bo--')

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

if __name__=='__main__':
    main()

