import sys
import os
import threading
# adds the root of the git dir to the import path
# FIXME: Directory shenanigans
root_dir = os.getcwd()
sys.path.append(root_dir)
import lib.Map.Map as mmap
from lib.Renderer.Controller import Controller
from lib.Renderer.Controller import View
import lib.Simulation.Simulator as Simulator
from lib.Renderer.GraphViewer import showData

OSMfile = "TX-To-TU.osm"
buildConnFile = "buildingConnection.csv"
jobfile = "jobs.csv"
buildingTaggingConfigFile = "tsukuba-tu-building-data.csv"

def main():
    filePath = os.path.join("osmData",OSMfile)
    buildConnFilePath = os.path.join("example",buildConnFile)
    jobfilePath = os.path.join("config",jobfile)
    buildingTaggingConfigFilePath = os.path.join("config",buildingTaggingConfigFile)
    
    # Load the data
    osmMap = mmap.readFile(filePath, buildConnFile=buildConnFilePath, buildingCSV = buildingTaggingConfigFilePath)
        
    # Start Simulator
    sim = Simulator.Simulator(jobfilePath, osmMap, agentNum=200)
    # x = threading.Thread(target=showData, args=(sim,))
    # x.start()
    #sim.stepCount = 3600*8
    
    # Draw    
    view = View(mymap=osmMap, simulation=sim)
    app = Controller(model=sim, view=view)
    app.main_loop()
    sim.extract()

if __name__ == "__main__":
    main()
    
