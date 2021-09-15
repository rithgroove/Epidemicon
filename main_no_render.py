import sys
import os
import yaml
import argparse
# adds the root of the git dir to the import path
# FIXME: Directory shenanigans
root_dir = os.getcwd()
sys.path.append(root_dir)
import lib.Map.Map as mmap
from lib.Simulation.Simulator import Simulator

configFileName = "config.yml"

requiredConfigs = [
    "OSMfile",
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
    "nr_step_size",
    "nr_day_to_simulate",
]

optionalConfig = [
    "buildConnFile",
    "pathfindFileName",
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
    for c in optionalConfig:
        if c not in config:
            config[c] = None

    return config

def parseArgs():
    global configFileName
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="sets the config file")
    parser.add_argument("--no_susceptible_stop", action="store_true", help="Interromps the execution if there are no more susceptible agents")
    args = parser.parse_args()
    
    if args.config_file:
        configFileName = args.config_file
    
    no_susceptible_stop = False
    if args.no_susceptible_stop:
        no_susceptible_stop = True

    return configFileName, no_susceptible_stop

def main():
    configFileName, no_susceptible_stop = parseArgs()

    c = read_validate_config(configFileName)

    stepSize = c["nr_step_size"] #5 minutes
    dayToSimulate = c["nr_day_to_simulate"]

    # Load the data
    gridSize = (c["gridHeight"], c["gridWidth"])
    osmMap = mmap.readFile(
        OSMfilePath = c["OSMfile"], 
        buildConnFile = c["buildConnFile"],
        grid = gridSize,
        buildingCSV = c["buildingConfigPath"])
    
    # Start Simulator
    sim = Simulator(
        osmMap = osmMap,
        jobCSVPath = c["jobsFile"],
        businessCVSPath = c["businessFile"],
        pathfindFileName = c["pathfindFileName"],
        agentNum = c["numberOfAgents"],
        threadNumber = c["threadNumber"],
        infectedAgent = c["infectedAgent"],
        vaccinationPercentage = c["vaccinationPercentage"],
        reportPath = c["reportDir"],
        reportInterval = c["reportInterval"])
        
    for x in range(0, dayToSimulate*24*3600, stepSize):
        _, seirStatus = sim.getAgentStatus()
        if no_susceptible_stop and seirStatus["Susceptible"] == 0: 
            break
        sim.step(stepSize = stepSize)

    sim.extract()
    sim.extractVisitLog()

if __name__ == "__main__":
    main()
    
