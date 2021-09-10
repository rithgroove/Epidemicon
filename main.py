import sys
import os
import yaml
# adds the root of the git dir to the import path
# FIXME: Directory shenanigans
root_dir = os.getcwd()
sys.path.append(root_dir)
import lib.Map.Map as mmap
from lib.Renderer.Controller import Controller
from lib.Renderer.Controller import View
from lib.Simulation.Simulator import Simulator

configFileName = "config.yml"

requiredConfigs = [
    "OSMfile",
    "buildConnFile",
    "jobsFile",
    "businessFile",
    "numberOfAgents",
    "buildingConfigPath",
    "threadNumber",
    "infectedAgent",
    "vaccinationPercentage",
    "windowWidth",
    "windowHeight",
    "reportDir",
    "reportInterval",
]

def read_validate_config(file_path):
    config = None
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    err = False
    errMessage = "Missing required attributes in config file: "
    for c in requiredConfigs:
        if c not in config:
            err = True
            errMessage += c + " "
    if err:
        raise NameError(errMessage)

    return config

def main():
    c = read_validate_config(configFileName)

    
    # Load the data
    gridSize = (c["gridHeight"], c["gridWidth"])
    osmMap = mmap.readFile(c["OSMfile"], c["buildConnFile"], gridSize, c["buildingConfigPath"])

    # nodeDict = {}
    # for n in osmMap.nodes:
    #     if n.hashId not in nodeDict:
    #         nodeDict[n.hashId] = []
    #     nodeDict[n.hashId].append(n)

    # for i in nodeDict:
    #     aux = nodeDict[i]       
    #     if len(aux) > 1:
    #         lat = aux[0].coordinate.lat
    #         for node in aux:
    #             if node.coordinate.lat != lat:
    #                 print("AAAA")
    #         lon = aux[0].coordinate.lon
    #         for node in aux:
    #             if node.coordinate.lon != lon:
    #                 print("BBBB")
    #         print(aux[0].hashId)

    # Start Simulator
    sim = Simulator(
        osmMap, 
        c["jobsFile"],
        c["businessFile"],
        c["numberOfAgents"], 
        c["threadNumber"], 
        c["infectedAgent"], 
        c["vaccinationPercentage"],
        c["reportDir"],
        c["reportInterval"])

    # Draw    
    windowSize = (c["windowWidth"], c["windowHeight"])
    view = View(mymap=osmMap, simulation=sim, window_size=windowSize)
    app = Controller(model=sim, view=view)
    app.main_loop()
    sim.extract()

if __name__ == "__main__":
    main()
    
