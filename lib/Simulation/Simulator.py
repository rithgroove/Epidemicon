import csv
from .JobClass import JobClass
from .Agent import Agent
from .Home import Home

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
        self.generateAgents(agentNum)
        self.stepCount = 0
            
    def generateAgents(self, count):
        total = 0
        self.osmMap
        houses = []
        houses.extend(self.osmMap.buildingsDict['residential'])
        houses.extend(self.osmMap.buildingsDict['house'])
        houses.extend(self.osmMap.buildingsDict['apartments'])
        for x in self.jobClasses:
            total += x.populationProportion
        for x in self.jobClasses:
            temp = int(x.populationProportion*count/float(total))
            ageRange = x.maxAge - x.minAge
            for i in range(0,temp):
                agent = Agent(self.osmMap,Home(random.choice(houses)),x.minAge+random.randint(0,ageRange),x)
                self.agents.append(agent)
                
    def step(self,steps = 15):
        self.stepCount +=1
        for x in self.agents:
            try:
                x.step(steps)
            except:
                print("agent failed steps")