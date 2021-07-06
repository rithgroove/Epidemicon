import csv
import random
import multiprocessing
from atpbar import flush
from .JobClass import JobClass
from .Agent import Agent
from .Home import Home
from .Infection import Infection
from .StepThread import StepThread
from lib.Map.MovementSequence import reconstruct
class Simulator:
    def __init__(self,jobCSVPath,osmMap,agentNum = 1000,threadNumber = 4):
        self.jobClasses = []
        self.osmMap = osmMap
        with open(jobCSVPath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            keys = []
            for row in csv_reader:
                data = {}
                if len(keys) == 0:
                    keys = row
                elif len(row) != 0:         
                    print(row)
                    for i in range(0,len(keys)):
                        data[keys[i]]=row[i]
                    temp =JobClass(data)
                    temp.buildings = osmMap.buildingsDict.get(temp.place)
                    self.jobClasses.append(temp)
            print(f'Processed {line_count} lines.')
        self.agents = []
        self.unshuffledAgents = []
        #self.stepCount = 3600*8
        self.stepCount = 0
        self.history = {}
        self.timeStamp = []
        self.threadNumber = threadNumber
        self.generateAgents(agentNum)
        self.splitAgentsForThreading()
        self.returnDict = None
        self.lastHour = -1
        
    def generateAgents(self, count):
        total = 0
        self.osmMap
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
                #time.sleep(0.5)
                #
                building = random.choice(houses)
                home = Home(building)
                if "home" not in building.content.keys():                    
                    building.content["home"] = []   
                building.content["home"].append(home)               
                agent = Agent(agentId, self.osmMap,home,x.minAge+random.randint(0,ageRange),x)
                agentId +=1
                if "agent" not in building.content.keys():                    
                    building.content["agent"] = []   
                building.content["agent"].append(agent)               
                self.agents.append(agent)
                self.unshuffledAgents.append(agent)
                building.node.addAgent(agent)
        random.shuffle(self.agents)
        for i in range (0,80):
            self.agents[i].infection = Infection(self.agents[i],self.agents[i],self.stepCount,dormant = 0)
            
    def splitAgentsForThreading(self):
        chunksize = int(len(self.agents)/ self.threadNumber)
        self.agentChunks = [self.agents[chunksize*i:chunksize*(i+1)] for i in range(int(len(self.agents)/chunksize) + 1)]
        if(len(self.agentChunks[-1]) < chunksize):
            self.agentChunks[0].extend(self.agentChunks[-1])
            self.agentChunks.remove(self.agentChunks[-1])
            
    def generateThread(self):
        self.queues = []
        self.threads = []
        i = 1
        manager = multiprocessing.Manager()
        self.returnDict = manager.dict()
        for chunkOfAgent in self.agentChunks:
            thread = StepThread(f"Thread {i}",chunkOfAgent,self.stepCount,self.returnDict)
            self.threads.append(thread)
            i += 1  
            
#     def step(self,steps = 3600):
#         for x in self.agents:
#             day, hour = self.currentHour()
#             try:
#                 x.step(day,hour,steps)
#             except:
#                 print("agent failed steps")
#                 x.translation = (0,0)
#         for x in self.agents:
#             x.checkInfection(self.stepCount)
#         for x in self.agents:
#             x.finalize(self.stepCount)
#         self.stepCount += steps
#         self.summarize()

    def step(self,steps = 3600):
        day, hour = self.currentHour()
        if (self.lastHour != hour):
            print("Activity Checking")
            self.generateThread()
            for thread in self.threads:
                thread.setStateToStep(steps)
                thread.start()
            #wait for all thread to finish running
            for thread in self.threads:
                thread.join()
            #reconstruct movement sequence
            for key in self.returnDict.keys():
                self.unshuffledAgents[int(key)].activeSequence = reconstruct(self.osmMap.roadNodesDict, self.returnDict[key][0], self.returnDict[key][1])
            flush()
            self.lastHour = hour

        print("Finished checking activity, proceeding to move agents")
        for x in self.agents:
            x.step(day,hour,steps)
        print("Finished moving agents, proceeding to check for infection")
        for x in self.agents:
            x.checkInfection(self.stepCount)
        print("Finished infection checking, proceeding to finalize the infection")
        for x in self.agents:
            x.finalize(self.stepCount)
        print("Finished finalizing the infection")
        self.stepCount += steps
        self.summarize()
        
    def currentHour(self):
        hour = int(self.stepCount / 3600)% 24
        day = int(hour /24) % 7
        return day,hour
    
    def summarize(self):
        result = {}
        result["Susceptible"] = 0
        result["Infectious"] = 0
        result["Exposed"] = 0
        result["Recovered"] = 0
        for x in self.agents:
            result[x.infectionStatus] += 1
        for x in result.keys():
            if x not in self.history.keys():
                self.history[x] = []
            self.history[x].append(result[x])
        self.timeStamp.append(self.stepCount/3600)
        return result
