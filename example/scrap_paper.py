#!/usr/bin/env python
# coding: utf-8

# # Load Library
# load global library

# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
# from time import time
# from random import random
# 
# plt.ion()
# # set up the figure
# fig = plt.figure()
# plt.xlabel('Time')
# plt.ylabel('Value')
# 
# plt.show(block=False)
# 
# def mypause(interval):
#     backend = plt.rcParams['backend']
#     if backend in matplotlib.rcsetup.interactive_bk:
#         figManager = matplotlib._pylab_helpers.Gcf.get_active()
#         if figManager is not None:
#             canvas = figManager.canvas
#             if canvas.figure.stale:
#                 canvas.draw()
#             canvas.start_event_loop(interval)
#             return
# 
# 
# t0 = time()
# t = []
# y = []
# while True:
#     t.append( time()-t0 )
#     y.append( random() )
#     plt.gca().clear()
#     plt.plot( t , y )
#     mypause(1)

# In[1]:


import sys
import os


# import random
# infectionPercentage = (-23.28 * 0) + 10.0
# print(infectionPercentage)
# test = random.randint(0,int(100*100))
# print(f"{test} vs {int(infectionPercentage*100)}")

# import matplotlib.pyplot

# load local library

# In[2]:


sys.path.append(os.path.join(os.getcwd() , ".."))
import lib.Map.Map as map
import lib.Renderer.Renderer as renderer
from lib.Renderer.GraphViewer import showData
import threading
import lib.Simulation.Simulator as Simulator


# In[3]:


print(map.Map.__doc__)


# In[4]:



print(map.readFile.__doc__)


# In[5]:


dataDirectory = os.path.join("..","osmData")
filename = "TX-To-TU.osm"
filepath = os.path.join(dataDirectory,filename)


# In[6]:


osmMap = map.readFile(filepath)


# In[7]:


print(osmMap)


# In[9]:


sim = Simulator.Simulator("../config/jobs.csv",osmMap,agentNum = 1000)


# In[12]:


x = threading.Thread(target=showData, args=(sim,))
x.start()
sim.stepCount = 3600*8


# In[ ]:


renderer.render(osmMap,sim)


# In[ ]:


sim.history


# In[ ]:





# 

# showData(sim)

# 
# sim.stepCount = 3600*8

# x = threading.Thread(target=renderer.render, args=(osmMap,sim,))
# x.start()

# showData(sim)

# a = [(45,'for', 24), (3,'Geeks', 8), (20,'Geeks', 30)] 
# a.sort(key=lambda x:x[1])
# a

# result

# print(osmMap.buildingsMap["b586"])
# print(osmMap.buildingsMap["b586"].node)
# print(osmMap.buildingsMap["b586"].entryPoint)
# 

# for x in sim.agents:
#     print(x.mainJob.isWorking(0,8))

# agent = sim.agents[1]

# agent.step(0,8,steps=15)

# sim.currentHour()

# print(agent.activeSequence)

# osmMap.findPath(agent,agent.mainJob.building)

# x = agent.currentNode.getMovementSequence(agent.mainJob.building.node)
# print (x)

# print(agent.currentNode)
# print(agent.home.node())

# agent.mainJob.isWorking(0,8)

# agent.mainJob.workdays

# b = agent.currentNode.getMovementSequence(agent.mainJob.building.node)  
# print(b)

# from lib.Map.PathFinder import searchPath
# distance, sequence = searchPath(osmMap,agent.currentNode,agent.mainJob.building.node)  

# sequence

# distance

# agent.setMovementSequence(activeSequence)

# agent.currentNode.addMovementSequence(sequence.clone())      

# 
