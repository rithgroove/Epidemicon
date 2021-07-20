import sys
import os
sys.path.append(os.path.join(os.getcwd() , ".."))
import lib.Map.Map as map
import lib.Renderer.Renderer as renderer
from lib.Renderer.GraphViewer import showData
from lib.Renderer.LocationStatistic import showPieChart
import threading
import lib.Simulation.Simulator as Simulator

dataDirectory = os.path.join("..","osmData")
filename = "TX-To-TU.osm"
filepath = os.path.join(dataDirectory,filename)
buildConnFile = "buildingConnection.csv"

buildingConfigPath = os.path.join("..","config","tsukuba-tu-building-data.csv")
osmMap = map.readFile(filepath, buildConnFile=buildConnFile, buildingCSV = buildingConfigPath)
sim = Simulator.Simulator("../config/jobs.csv",osmMap,agentNum = 240,threadNumber = 12, infectedAgent = 10)

stepLength = 300 #step length in simulation seconds
for i in range(0,30*24*3600,stepLength):
	print(i)
	sim.step(stepLength)

sim.extract()
print("finished")
