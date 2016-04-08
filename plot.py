import matplotlib
matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt

import numpy as np
import sys


def main():
    dname = sys.argv[1]
    d = np.genfromtxt(dname)
    resistance, time, position = d.T

    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    diff = np.diff(position)
    ids = np.argwhere(diff)

    for id in ids:
        ax1.axvline(id, color='red')

    ax1.plot(resistance)
    ax2.plot(position)

    plt.show()

if __name__=='__main__':
    main()
