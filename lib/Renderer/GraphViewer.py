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
    color = {}
    color["Susceptible"] = "#3333CC"
    color["Exposed"] = "#CCCC33"
    color["Infectious"] = "#CC3333"
    color["Recovered"] = "#33CC33"
    lastStepCount = 0
    while True:
        if (lastStepCount != sim.stepCount):
            ax = plt.gca()
            ax.clear()
            ax.set_ylim((0,len(sim.agents)+5))
            ax.set_ylabel('number of agent')
            ax.set_xlabel('time (hours)')
            for x in sim.history.keys():
                plt.plot(sim.timeStamp, sim.history[x],label = x,color = color[x])
            if (sim.history.keys().__len__() != 0):
                ax.legend()
            lastStepCount = sim.stepCount
            mypause(10)