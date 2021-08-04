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
jobfile = "config/jobs.csv"

def main():
    filePath = f"osmData\{OSMfile}"
    
    # Load the data
    osmMap = mmap.readFile(filePath, buildConnFile=buildConnFile)
        
    # Start Simulator
    sim = Simulator.Simulator(jobfile, osmMap, agentNum=200)
    # x = threading.Thread(target=showData, args=(sim,))
    # x.start()
    sim.stepCount = 3600*8
    
    # Draw    
    view = View(mymap=osmMap, simulation=sim)
    app = Controller(model=sim, view=view)
    app.main_loop()

if __name__ == "__main__":
    main()
    