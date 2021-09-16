import csv
from lib.Map.Map import Map
#import random
import multiprocessing
import atexit
from .JobClass import JobClass
from .Agent import Agent, getAgentKeys
from .Home import Home
from .Infection import Infection
from .BasicInfectionModel import BasicInfectionModel
from .StepThread import StepThread
from .TimeStamp import TimeStamp
from .Business import Business
import os
from os.path import join
from lib.Map.MovementSequence import reconstruct, reconstructByHashId
import datetime
import csv
from .VisitLog import VisitLog, getVisitKey
from pathlib import Path
import time
import numpy as np
from .MedicalTesting import MedicalTesting
from .PCRResult import getPCRResultKey

summaryFieldnames = [
    'Day',
    'Hour',
    'Minute',
    'CurrentStep',
    'Susceptible',
    'Exposed',
    'Infectious',
    'Recovered',
    'Dead'
]

detailsFieldnames = [
    'infectedAgentId',
    'infectedAgentProfession',
    'originAgentId',
    'originAgentProfession',
    'location',
    'lat',
    'lon',
    'nodeId',
    'exposedTimeStamp',
    'exposedDay',
    'exposedHour',
    'exposedMinute',
    'incubationDuration',
    'infectiousTimeStamp',
    'infectiousDay',
    'infectiousHour',
    'infectiousMinute',
    'recoveryDuration',
    'recoveredTimeStamp',
    'recoveredDay',
    'recoveredHour',
    'recoveredMinute',
    'symptomaticTimeStamp',
    'symptomaticDay',
    'symptomaticHour',
    'symptomaticMinute',
    'severeTimeStamp',
    'severeDay',
    'severeHour',
    'severeMinute',
    'deadTimeStamp',
    'deadDay',
    'deadHour',
    'deadMinute',
]

def readCVS (cvsPath):
    with open(cvsPath) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data_dict = [row for row in csv_reader]
    return data_dict

class Simulator:
    """
    [Class] Simulator
    The main simulator class
    
    Properties:
        - osmMap = [Map] the map used to simulate it
        - jobClasses = [array] array of jobClasses
        - agents = [array] array of agents
        - unshuffledAgents = [array] array of agents the agent is sorted based on their id 
        - stepCount = [int] current step count which represent how many simulated seconds from the beggining of the simulation
        - history = [Dictionary] of SEIR status that was staged after each step was finished
        - historyTimeStamp = [array]  the timestamp of the history properties (used for drawing graph)
        - threadNumber = [int] how many thread this simulator allowed to create when doing pathfinding
        - lastHour = [int] last calculated hour, used to trigger pathfinding.
        - vaccinationPercentage = [float] percentage of people that got the vaccine in the simulation.
        - infectionHistory = [array] array of infection that happened in our simulation
        - reportPath = [string] path for the records
        - reportInterval = [int] how many step do we want to wait before we extract the data
        - reportCooldown = [int] the current value of report interval
        - infectionModel = [InfectionModel] the infection model
        - pathfindFile = [file] file to read/write the paths from node to node
        - pathfindDict = [dict] dictionary to check for already calculated paths
        
    Don't Access Properties:
        - returnDict = [array] (DO NOT USE) array of dictionary that was returned by the thread 
        - activitiesDict = [array] (DO NOT USE) array of dictionary that was returned by the thread 
        - queue = [array] (DO NOT USE) array of queues that was returned by the thread 
        - threads = [array] (DO NOT USE) array of StepThreads that was returned by the thread 
        
    """
    def __init__(self,
                osmMap,
                jobCSVPath,
                businessCVSPath,
                pathfindFileName,
                agentNum = 1000,
                threadNumber = 4,
                infectedAgent = 5,
                vaccinationPercentage = 0.0,
                reportPath="report",
                reportInterval=10,
                infectionModel = None,
                seed = 1000):
        """
        [Constructor]
        The constructor for Simulator class

        Properties:
            - osmMap = [Map] the map used to simulate it
            - jobCSVPath = [string] path to the job.csv
            - businessCSVPath = [string] path to the business.csv
            - agentNum = [int] number of agent that will be generated
            - threadNumber = [int] how many thread this simulator allowed to create when doing pathfinding
            - infectedAgent = [int] how many agents are infected at the beginning of our simulation
            - vaccinationPercentage = [float] percentage of people that got the vaccine in the simulation.
            - reportPath = [string] path for the records
            - reportInterval = [int] how many step do we want to wait before we extract the data
            - infectionModel = [InfectionModel] the infection model
            - pathfindFileName = [string] file to save/load the paths found in the execution
        """
        self.rng = np.random.default_rng(seed)
        self.jobClasses = []
        self.osmMap = osmMap
        jobClassData = readCVS(jobCSVPath)
        for jobClass in jobClassData:
            temp = JobClass(jobClass)
            temp.buildings = osmMap.buildingsDict.get(temp.place)
            self.jobClasses.append(temp)
        self.agents = []
        self.unshuffledAgents = []
        self.timeStamp = TimeStamp()
        self.businessDict = self.generateBusinesses(businessCVSPath, osmMap)
        self.history = {}
        self.history ["Susceptible"] = []
        self.history ["Exposed"] = []
        self.history ["Infectious"] = []
        self.history ["Recovered"] = []
        self.historyTimeStamp = []
        self.threadNumber = threadNumber
        self.returnDict = None
        self.activitiesDict = None
        self.lastHour = -1
        self.vaccinationPercentage = vaccinationPercentage
        self.tester = MedicalTesting(self.rng,0.99) #set PCR to 99% accuracy
        self.testResults = []
        self.generateAgents(agentNum, infectedAgent)
        self.splitAgentsForThreading()
        self.infectionHistory = []
        self.queue = []
        self.threads = []
        self.reportPath = self.createReportDir(reportPath)
        self.reportInterval = reportInterval
        self.reportCooldown = reportInterval
        self.visitHistory = []
        self.calculating = False
        if infectionModel is None:
            self.infectionModel = BasicInfectionModel(self,self.osmMap)
        else:
            self.infectionModel = infectionModel
        self.infectionModel.setRNG(self.rng)

        # pathFindFile
        self.pathfindFile = None
        self.pathfindDict = {}
        if pathfindFileName is not None:
            Path(pathfindFileName).touch()
            self.pathfindFile = open(pathfindFileName, "r+")
            self.pathfindDict = self.buildPathfindDict()
        self.nodeHashIdDict = {}
        for n in self.osmMap.roadNodes:
            self.nodeHashIdDict[n.hashId] = n

        atexit.register(self.cleanup)

    def cleanup(self):
        """
        [Method] cleanup
        Closes the open files in the object
        """
        if self.pathfindFile is not None:
            self.pathfindFile.close()

    def buildPathfindDict(self):
        """
        [Method] buildPathfindDict
        Method that creates an dictionary in the format: [Dict[startNodeHashId: int, [Dict[finishNodeHasId: int, MovementSequence]]]]
        that is used to avoid recalculating paths that were already calculated

        Return: [Dict[wayID: str, ("min_dist": int, "entryCoordinate": Coordinate)]]
        """
        print("Start building pathfind dict")
        startTime = time.time()
        pathfindDict={}
        if self.pathfindFile is not None:
            for line in self.pathfindFile.readlines():
                if line[-1:] == "\n": # remove \n at the end of line if necessary
                    line = line[:-1]
                try:
                    startNodeId, finishNodeId, distance, sequenceString = line.split(";")
                    startNodeId = int(startNodeId)
                    finishNodeId = int(finishNodeId)

                    sequence = (eval(sequenceString), float(distance))

                    if startNodeId not in pathfindDict:
                        pathfindDict[startNodeId] = {}
                    pathfindDict[startNodeId][finishNodeId] = sequence
                except ValueError:
                    # This exception occurs if the split does not return the correct number of arguments
                    # This means that or the csv is invalid or the line is wrong, in any case the process continues
                    continue
        print("Building pathfind dict took %.2fs"%(time.time() - startTime))
        return pathfindDict

    def addSequenceToFile(self, sequence):
        """
        [Method] addSequenceToFile
        Adds a MovementSequence to the self.pathfindDict and to the self.pathfindFile.
        It assumes the dictionary is on par with the pathfindFile

        Parameters: 
            - sequence = MovementSequence, sequence to be added to the file and to the dictionary

        """
        startNode = sequence.origin
        finishNode = sequence.destination
        if startNode.hashId not in self.pathfindDict:
            self.pathfindDict[startNode.hashId] = {}
        if finishNode.hashId not in self.pathfindDict[startNode.hashId]:
            self.pathfindDict[startNode.hashId][finishNode.hashId] = sequence

            if self.pathfindFile is not None:
                seqToSave=[]
                for mvVector in sequence.sequence:
                    start = mvVector.startingNode.hashId
                    finish = mvVector.destinationNode.hashId
                    seqToSave.append((start,finish))
                line = f"{startNode.hashId};{finishNode.hashId};{sequence.totalDistance};{seqToSave}\n"
                self.pathfindFile.write(line)


    def generateBusinesses(self, businessCVSPath, osmMap) :
        businessTypeInfoArr = {}
        businessDictByType = {}
        for line in readCVS(businessCVSPath):
            businessType = line["building_type"]
            businessTypeInfoArr[businessType] = line
            businessDictByType[businessType] = []
        for building in osmMap.buildings:
            if building.type not in businessTypeInfoArr:
                continue
            businessTypeInfo = businessTypeInfoArr[building.type]
            b = Business(building, businessTypeInfo,self.rng)
            businessDictByType[building.type].append(b)
        return businessDictByType

    def createReportDir(self, reportPath):
        """
        [Method] createReportdir
        Method to create the report directory

        Properties:
            - reportPath = [string] path for the records
        """
        current_time = datetime.datetime.now()
        new_dir = current_time.strftime("%Y%m%d-%H%M")
        path = os.path.join(reportPath, new_dir)
        Path(path).mkdir(parents=True, exist_ok=True)

        return path

    def generateAgents(self, count, infectedAgent = 5):
        """
        [Method] generateAgents
        Method to create the report directory

        Properties:
            - count = [int] number of agent that will be generated
            - infectedAgent = [int] how many agents are infected at the beginning of our simulation
        """
        total = 0
        houses = []
        houses.extend(self.osmMap.buildingsDict['residential'])
        houses.extend(self.osmMap.buildingsDict['house'])
        houses.extend(self.osmMap.buildingsDict['apartments'])
        #last line of defense, if somehow the building doesn't have node, remove it
        agentId = 0
        for x in houses:
            if x.node is None:
                houses.remove(x)
                
        for x in self.jobClasses:
            total += x.populationProportion
        for x in self.jobClasses:
            temp = int(x.populationProportion*count/float(total))
            ageRange = x.maxAge - x.minAge
            for i in range(0,temp):             
                agent = Agent(agentId, self.osmMap, x.minAge+self.rng.integers(0, ageRange), x, self.businessDict,self.rng, self.tester)
                agentId +=1         
                self.agents.append(agent)
                self.unshuffledAgents.append(agent)
        for x in range(0,count- len(self.agents)):
            x = self.jobClasses[0]
            temp = int(x.populationProportion*count/float(total))
            ageRange = x.maxAge - x.minAge
            agent = Agent(agentId, self.osmMap, x.minAge+self.rng.integers(0, ageRange), x, self.businessDict,self.rng, self.tester)
            agentId +=1         
            self.agents.append(agent)
            self.unshuffledAgents.append(agent)
            
        self.rng.shuffle(self.agents) #shuffle so that we can randomly assign vaccine 
        
        
        for i in range(0,int(self.vaccinationPercentage*len(self.agents))):
            self.agents[i].setVaccinated()

        self.rng.shuffle(self.agents) #shuffle so that we can randomly assign a household 
        
        housePop = 0
        building = None
        home = None
        houseId = 0
        for agent in self.agents:
            #generate Home
            if housePop ==0:
                housePop = self.rng.integers(1,3)
                building = self.rng.choice(houses)
                if (building.type == "house"):
                    houses.remove(building)
                home = Home(building,houseId,self.rng)
                houseId += 1
                if "home" not in building.content.keys():                 
                    building.content["home"] = []   
                building.content["home"].append(home)
            if "agent" not in building.content.keys():                    
                building.content["agent"] = []   
            building.content["agent"].append(agent)      
            agent.setHome(home)
            home.addOccupant(agent)
            housePop -= 1
            building.node.addAgent(agent)
            
            
        self.rng.shuffle(self.agents) #shuffle so that we can randomly assign people who got initial infection 
        for i in range (0, infectedAgent):
            self.agents[i].infection = Infection(self.agents[i],self.agents[i],self.timeStamp.clone(),dormant = 0,recovery = self.rng.integers(72,14*24) *3600,location ="Initial")
            
        
    def splitAgentsForThreading(self):
        """
        [Method] splitAgentsForThreading
        Method to split agents into several array for threading purposes
        
        TODO = change name to mark it as private
        """
        chunksize = int(len(self.agents)/ self.threadNumber)
        self.agentChunks = [self.agents[chunksize*i:chunksize*(i+1)] for i in range(int(len(self.agents)/chunksize) + 1)]
        if(len(self.agentChunks[-1]) < chunksize):
            self.agentChunks[0].extend(self.agentChunks[-1])
            self.agentChunks.remove(self.agentChunks[-1])
            
            

    def step(self,stepSize = 3600):
        """
        [Method] step
        The step function. there are 5 main step:
            - pathfinding (triggered when the hour changes)
            - move the agents
            - check infection of the agents
            - finalize the infection 
            - summarize
        
        Parameter: 
            - stepSize = how long we wanted to step forward in seconds (60 means 60 seconds)
        """
        print(self.timeStamp)
        hour = self.timeStamp.getHour()
        self.calculating = True

        if (self.lastHour != hour):
            self.lastHour = hour
            start = time.time()
            if self.threadNumber>1:
                ###############################################################################################
                # Generate Threads
                # Do not refactor into other function
                # ref : https://stackoverflow.com/questions/49391569/python3-process-object-never-joins
                ###############################################################################################
                threads = []
                i = 1
                manager = multiprocessing.Manager()
                returnDicts = [] #if not working, probably this must be allocated locally
                activitiesDicts = [] #if not working, probably this must be allocated locally
                for chunkOfAgent in self.agentChunks:
                    returnDict = manager.dict()
                    activitiesDict = manager.dict()
                    returnDicts.append(returnDict)
                    activitiesDicts.append(activitiesDict)
                    thread = StepThread(f"Thread {i}",chunkOfAgent,self.timeStamp,returnDict,activitiesDict,self.businessDict,self.pathfindDict,self.nodeHashIdDict,self.rng.integers(0,100000))
                    threads.append(thread)
                    i += 1  
                ###############################################################################################
                # Generate Threads end
                ###############################################################################################

                for thread in threads:
                    thread.daemon = True
                    thread.setStateToStep(stepSize)
                    thread.start()
                time.sleep(30) # sleep for 20 second to help the threads starts their work
                # wait for all thread to finish running
                for i in range(0,len(threads)):
                    threads[i].join()
            else:
                chunkOfAgent = self.agentChunks[0]
            
                manager = multiprocessing.Manager()
                returnDicts = [] 
                activitiesDicts = [] 
                
                returnDict = manager.dict()
                activitiesDict = manager.dict()
                returnDicts.append(returnDict)
                activitiesDicts.append(activitiesDict)
            
                nothread = StepThread(f"Nothread",chunkOfAgent,self.timeStamp,returnDict,activitiesDict,self.businessDict,self.pathfindDict,self.nodeHashIdDict, self.rng.integers(0,100000))
                nothread.setStateToStep(stepSize)
                nothread.run()

                    
            for returnDict in returnDicts:
                for key in returnDict.keys():
                    sequence = reconstruct(self.osmMap.roadNodesDict, returnDict[key][0], returnDict[key][1])
                    self.unshuffledAgents[int(key)].activeSequence = sequence
                    self.addSequenceToFile(sequence)
            for activitiesDict in activitiesDicts:
                for key in activitiesDict.keys():
                    self.unshuffledAgents[int(key)].activities = activitiesDict[key]
            #flush()
            self.lastHour = hour
            
            self.threads = []
            print("Pathfinding finished in: %.2fs" % (time.time() - start))
                
        #print("Finished checking activity, proceeding to move agents")
        for x in self.agents:
            x.step(self.timeStamp,self.rng,stepSize)
            if (x.newVisitLog is not None):
                self.visitHistory.append(x.newVisitLog)
                x.newVisitLog = None
            if (x.newTestResult is not None):
                self.testResults.append(x.newTestResult)
                x.newTestResult = None
        #print("Finished moving agents, proceeding to check for infection")
        for agent in self.agents:
            self.infectionModel.infect(agent,stepSize,self.timeStamp)
            #x.checkInfection(self.stepCount,stepSize)
        #print("Finished infection checking, proceeding to finalize the infection")
        for x in self.agents:
            x.finalize(self.timeStamp,stepSize,self.rng)
        print("Finished finalizing the infection")
        self.timeStamp.step(stepSize)
        self.calculating = False
        self.summarize()
        self.printInfectionLocation()

        if self.reportCooldown < 1:
            print("Extracting data")
            self.extract()
            self.reportCooldown = self.reportInterval
        self.reportCooldown -= 1
    
    def printInfectionLocation(self):
        """
        [Method] printInfectionLocation
        method to print where the infection happened to command line 
        """
        summary = {}
        for agent in self.agents:
            if agent.infection is not None:
                if agent.infection.location not in summary: 
                    summary[agent.infection.location]=0
                summary[agent.infection.location] += 1

        print("\nknown infection location")
        for key in summary.keys():
            print(f"{key} = {summary[key]}")
        print("\n")
    
    
    
    def summarize(self):
        """
        [Method] summarize
        method to do staged data collection for current simulated time
        """
        result = {}
        result["CurrentStep"] = self.timeStamp.stepCount
        result["Day"] = self.timeStamp.getDay()
        result["Hour"] = self.timeStamp.getHour()
        result["Minute"] = self.timeStamp.getMinute()
        result["Susceptible"] = 0
        result["Infectious"] = 0
        result["Exposed"] = 0
        result["Recovered"] = 0
        result["Dead"] = 0
        for x in self.agents:
            result[x.infectionStatus] += 1
        for x in result.keys():
            if x in self.history.keys():
                self.history[x].append(result[x])
        self.historyTimeStamp.append(self.timeStamp.stepCount/3600)
        self.infectionHistory.append(result)
        
        return result
    
    def killStepThreads(self):
        """
        [Method] killStepThreads
        method to force terminate the StepThreads
        """
        for thread in self.threads:
            thread.terminate()
            
    def extract(self):
        """
        [Method] extract
        method to write the simulation result to files
        """
        # This function always open and close the files 
        # to guarantee that they are being rewriten from scratch

        # TODO: Remember where in the "infection history" we stopped saving the log, and continue later.
        summaryFilePath = join(self.reportPath,'infection_summary.csv')
        with open(summaryFilePath, 'w', newline='') as summaryFile:
            writer = csv.DictWriter(summaryFile, fieldnames=summaryFieldnames)
            writer.writeheader()
            for x in self.infectionHistory:
                writer.writerow(x)
            summaryFile.close()
        
        detailsFilePath = join(self.reportPath,'infection_details.csv')
        with open(detailsFilePath, 'w', newline='') as detailsFile:
            writer = csv.DictWriter(detailsFile, fieldnames=detailsFieldnames)
            writer.writeheader()
            for i in self.agents:
                if (i.infection is not None):
                    summary = i.infection.summarize()
                    writer.writerow(summary)
            detailsFile.close()
         
        # TODO Issue: Consider if we want to keep the history of the agents in the future (maybe this is too much data)
 
        agentsFilePath = join(self.reportPath,'agents.csv')
        with open(agentsFilePath, 'w', newline='') as agentsFile:
            agentFieldnames = getAgentKeys()
            writer = csv.DictWriter(agentsFile, fieldnames=agentFieldnames)
            writer.writeheader()
            for x in self.agents:
                writer.writerow(x.extract())
            agentsFile.close()
        
        visitFilePath = join(self.reportPath,'visit_log.csv')
        with open(visitFilePath, 'w', newline='') as detailsFile:
            writer = csv.DictWriter(detailsFile, fieldnames=getVisitKey())
            writer.writeheader()
            for i in self.visitHistory:
                summary = i.summarize()
                writer.writerow(summary)
            detailsFile.close()
        
        visitFilePath = join(self.reportPath,'PCR_results.csv')
        with open(visitFilePath, 'w', newline='') as detailsFile:
            writer = csv.DictWriter(detailsFile, fieldnames=getPCRResultKey())
            writer.writeheader()
            for i in self.testResults:
                summary = i.extract()
                writer.writerow(summary)
            detailsFile.close()

    def getAgentStatus(self):
        # Possible status: Normal, Symptomatics, Severe
        # Possible infectiousStatus: Susceptible, Exposed, Infectious, Recovered
        status = {"Normal":0, "Symptomatics": 0, "Severe": 0}
        seirStatus = {"Susceptible": 0, "Exposed": 0, "Infectious": 0, "Recovered": 0}

        for ag in self.agents:
            status[ag.status] += 1
            seirStatus[ag.infectionStatus] += 1
        return status, seirStatus