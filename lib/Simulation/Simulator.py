import csv
from .JobClass import JobClass
from .Agent import Agent
from .Home import Home
from .Infection import Infection
import random
class Simulator:
    def __init__(self,jobCSVPath,osmMap,agentNum = 1000):
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
        self.stepCount = 3600*8
        self.generateAgents(agentNum)
        self.stepCount = 0
        self.history = {}
        self.timeStamp = []
            
    def generateAgents(self, count):
        total = 0
        self.osmMap
        houses = []
        houses.extend(self.osmMap.buildingsDict['residential'])
        houses.extend(self.osmMap.buildingsDict['house'])
        houses.extend(self.osmMap.buildingsDict['apartments'])
        for x in houses:
            if x.node is None:
                houses.remove(x)
        for x in self.jobClasses:
            total += x.populationProportion
        for x in self.jobClasses:
            temp = int(x.populationProportion*count/float(total))
            ageRange = x.maxAge - x.minAge
            for i in range(0,temp):              
                building = random.choice(houses)
                home = Home(building)
                if "home" not in building.content.keys():                    
                    building.content["home"] = []   
                building.content["home"].append(home)               
                agent = Agent(self.osmMap,home,x.minAge+random.randint(0,ageRange),x)
                if "agent" not in building.content.keys():                    
                    building.content["agent"] = []   
                building.content["agent"].append(agent)               
                self.agents.append(agent)
                building.node.addAgent(agent)
        for i in range (0,80):
            self.agents[i].infection = Infection(self.agents[i],self.agents[i],self.stepCount,dormant = 0)
    
                
    def step(self,steps = 3600):
        for x in self.agents:
            day, hour = self.currentHour()
            try:
                x.step(day,hour,steps)
            except:
                print("agent failed steps")
                x.translation = (0,0)
        self.stepCount += steps
        for x in self.agents:
            x.checkInfection(self.stepCount)
        for x in self.agents:
            x.finalize(self.stepCount)
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
            