import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from time import time
from random import random

def showData(sim):
    plt.ion()
    # set up the figure
    fig = plt.figure()
    plt.xlabel('Time')
    plt.ylabel('population')

    plt.show(block=False)

    def mypause(interval):
        backend = plt.rcParams['backend']
        if backend in matplotlib.rcsetup.interactive_bk:
            figManager = matplotlib._pylab_helpers.Gcf.get_active()
            if figManager is not None:
                canvas = figManager.canvas
                if canvas.figure.stale:
                    canvas.draw()
                canvas.start_event_loop(interval)
                return


    t0 = time()
    t = []
    y = []
    while True:
        plt.gca().clear()
        for x in sim.history.keys():
            plt.plot(sim.timeStamp, sim.history[x])
        mypause(1)