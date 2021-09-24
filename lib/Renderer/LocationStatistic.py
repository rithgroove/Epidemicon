import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from time import time
from random import random

def showPieChart(sim):
    plt.ion()
    # set up the figure
    
    



    fig, ax1 = plt.subplots()
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
    label = []
    sizes = []
    lastStepCount = 0
    while True:
        if (lastStepCount != sim.stepCount):
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            summary = {}
            for agent in sim.agents:
                if agent.infection is not None:
                    if agent.infection.location not in summary: 
                        summary[agent.infection.location]=0
                    summary[agent.infection.location] += 1
            
            for key in summary.keys():
                label.append(key)
                sizes.append(summary[key])
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            
            ax1.legend()
            lastStepCount = sim.stepCount
            mypause(10)