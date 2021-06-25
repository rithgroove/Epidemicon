import random
from .Infection import Infection 
class Agent:
    """
    [Class] Agent
    
    
    Properties:
        - home : [] the building the house is in
        - currentLocation : [Coordinate] the agents that live inside this home
        - infection_status : [string] SEIR (Susceptible, Exposed, Infectious, Recovered)
        - age :[int] Age
        - mainJob : [Job] job
    """
    def __init__(self,osmMap,home,age,job):
        self.home = home
        self.age = age
        self.mainJob = job.generateJob()
        self.mainJob.setAgent(self)
        self.infectionStatus = "Susceptible"
        self.currentLocation = home.coordinate().newCoordinateWithTranslation()
        self.currentNode = home.node()
        self.oval = None
        self.name = ""
        self.speed = 1.46
        self.activeSequence = None
        self.osmMap = osmMap
        self.transition = (0,0)
        self.distanceToDestination = 0
        self.infection = None
        
    def setMovementSequence(self, activeSequence):
        self.activeSequence = activeSequence
        
    def getSpeed(self):
        return self.speed
    
    def step(self,day,hour,steps=1):
        if(self.activeSequence is None or self.activeSequence.finished):
            if self.currentNode == self.home.node():
                #gotowork
                if self.mainJob.isWorking(day, hour) and self.currentNode != self.mainJob.building.node:                 
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.mainJob.building)
                else:
                    self.activeSequence = None
            else:
                if not self.mainJob.isWorking(day, hour) and self.currentNode != self.home.node():                 
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.home.building)
                #gohome
        if self.activeSequence is not None:
            #after recalculate
            leftOver = steps * self.getSpeed()
            
            while leftOver > 0 and not self.activeSequence.finished:
                leftOver = self.activeSequence.step(leftOver)
                self.currentNode.removeAgent(self)
                self.currentNode = self.activeSequence.currentNode
                self.currentNode.addAgent(self)
                #self.evaluate()
                #print(f"leftover = {leftOver}")
                
            self.transition = self.activeSequence.getVector(self.currentLocation)
            self.currentLocation.translate(lat = self.transition[0], lon = self.transition[1])
            
    def checkInfection(self,currentStepNumber):
        if self.infectionStatus == "Susceptible":
            print("checking for infection")
            for x in self.currentNode.agents:
                
                if (x.infectionStatus == "Infectious"):
                    distance = x.currentLocation.calculateDistance(self.currentLocation)
                    #infectionPercentage = (-23.28 * distance) + 63.2
                    infectionPercentage = (-23.28 * distance) + 10.0
                    print("I met an infected person!")
                    if infectionPercentage > 0 and random.randint(0,int(10000)) < infectionPercentage*100:
                        self.infection = Infection(x,self,currentStepNumber)
                        print("I got infected!")
                        break
            for node in self.currentNode.connections:
                for x in node.agents:
                    
                    if (x.infectionStatus == "Infectious"):
                        distance = x.currentLocation.calculateDistance(self.currentLocation)
                        infectionPercentage = (-23.28 * distance) + 63.2
                        print("I met an infected person!")
                        if infectionPercentage > 0 and (random.randint(0,int(10000)) < (infectionPercentage*100)):
                            self.infection = Infection(x,self,currentStepNumber)
                            print("I got infected!")
                            break
                            
    def finalize(self,currentStepNumber):
        if self.infection != None:
            self.infection.finalize(currentStepNumber)