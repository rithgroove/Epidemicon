import sys
import os
import threading
# adds the root of the git dir to the import path
# FIXME: Directory shenanigans
root_dir = os.getcwd()
sys.path.append(root_dir)
import lib.Map.Map as mmap
from lib.Renderer.Controller import Controller
import lib.Simulation.Simulator as Simulator
from lib.Renderer.GraphViewer import showData

OSMfile = "TX-To-TU.osm"
buildConnFile = "buildingConnection.csv"

def main():
    filePath = os.path.join(root_dir, "osmData", OSMfile)
    
    # Load the data
    osmMap = mmap.readFile(filePath, buildConnFile=buildConnFile)
        
    # Start Simulator
    # sim = None
    sim = Simulator.Simulator("config/jobs.csv", osmMap, agentNum=1000)
    x = threading.Thread(target=showData, args=(sim,))
    x.start()
    sim.stepCount = 3600*8
    
    # Draw    
    app = Controller(osmMap, sim)
    app.mainloop()

if __name__ == "__main__":
    main()
    