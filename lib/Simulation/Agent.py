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
    def __init__(self,agentId, osmMap,age,job):
        self.home = None
        self.currentLocation = None
        self.agentId = agentId
        self.age = age
        self.mainJob = job.generateJob()
        self.mainJob.setAgent(self)
        self.infectionStatus = "Susceptible"
        self.currentNode = None
        self.oval = None
        self.name = ""
        self.speed = 1.46
        self.activeSequence = None
        self.osmMap = osmMap
        self.transition = (0,0)
        self.distanceToDestination = 0
        self.infection = None
        self.hairCap = float(random.randint(12,30))
        self.hair = float(random.randint(4,self.hairCap))
        self.hunger = 1.0
        self.hungerReduction = 0.7
        self.eatingOutPref = float(random.randint(0,10))/10.0
        
    def setHome(self,home):
        self.home = home
        self.currentLocation = home.coordinate().newCoordinateWithTranslation()
        self.currentNode = home.node()
        
    def setMovementSequence(self, activeSequence):
        self.activeSequence = activeSequence
        
    def getSpeed(self):
        return self.speed
    
    def checkSchedule(self,day,hour,steps=1):
        if(self.activeSequence is None or self.activeSequence.finished):
            if self.mainJob.isWorking(day, hour) and self.currentNode != self.mainJob.building.node:                 
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.mainJob.building)
                else:

            elif not self.mainJob.isWorking(day, hour) and self.currentNode != self.home.node():                 
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.home.building)
            else:
                self.activeSequence = None        
        if (self.activeSequence is not None and self.activeSequence.new):
            #print(f"I agent {self.agentId} did find a sequence")
            return self.activeSequence.extract()
        return None
                #gohome    
                
    def step(self,day,hour,steps=1):
        self.hair += 0.44/(24*(3600/steps))
        self.hunger -= self.hungerReduction/(24*(3600/steps))
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
            
    def checkInfection(self,currentStepNumber,stepLength):
        if self.infectionStatus == "Susceptible":
            #print("checking for infection")
            #at node infection
            if (self.currentNode == self.home.node()):
                #this if means the agent is at home
                self.infectAtHome(currentStepNumber,stepLength)
            elif self.currentNode.isBuildingCentroid:
                if self.currentNode.building == self.mainJob.building and self.mainJob.isOutsideCity():
                    #this means they are working outside city
                    self.infectFromOutsideOfCity(currentStepNumber,stepLength)
                else:
                    #this means infection is at a building locally
                    self.infectAtBuilding(currentStepNumber,stepLength)
            else:
                self.infectOnTheRoad(currentStepNumber,stepLength)  

    def infectOnTheRoad(self,currentStepNumber,stepLength):
        for stranger in self.currentNode.agents:
            if (stranger.infectionStatus == "Infectious"):
                distance = stranger.currentLocation.calculateDistance(self.currentLocation)
                #infectionPercentage = (-23.28 * distance) + 20.0
                infectionPercentage = (-23.28 * distance) + 63.2
                #infectionPercentage = 20.0
                infectionPercentage /= (24 * 3600/ stepLength)
                if infectionPercentage > 0 and random.randint(0,int(10000)) < infectionPercentage*100:
                    self.infection = Infection(stranger,self,currentStepNumber, location = "On The Road")
                    #print("I got infected!")
                    break
        if self.infection is None:
            for node in self.currentNode.connections:
                for stranger in node.agents:
                    if (stranger.infectionStatus == "Infectious"):
                        distance = stranger.currentLocation.calculateDistance(self.currentLocation)
                        infectionPercentage = (-23.28 * distance) + 63.2
                        infectionPercentage /= (24 * 3600/ stepLength)
                        #print("I met an infected person!")
                        if infectionPercentage > 0 and (random.randint(0,int(10000)) < (infectionPercentage*100)):
                            self.infection = Infection(stranger,self,currentStepNumber, location = "On The Road")
                            #print("I got infected!")
                            break
        
        
    def infectFromOutsideOfCity(self,currentStepNumber,stepLength):
        if random.randint(0,int(10000)) < 200/(24*3600/stepLength) :
            self.infection = Infection(self,self,currentStepNumber,location = "Going out of city")
            
                                
    def infectAtBuilding(self,currentStepNumber,stepLength):
        for stranger in self.currentNode.agents:
            #if room mate is infectious and at home
            if (stranger.infectionStatus == "Infectious"):
                #infectionPercentage = (-23.28 * distance) + 20.0
                infectionPercentage = 20.0
                infectionPercentage /= (24 * 3600/ stepLength)
                if infectionPercentage > 0 and random.randint(0,int(10000)) < infectionPercentage*100:
                    self.infection = Infection(stranger,self,currentStepNumber,location = self.currentNode.building.type)
                    #print("I got infected!")
                    break
                            
    def infectAtHome(self,currentStepNumber,stepLength):
        for roomMate in self.home.occupants:
            #if room mate is infectious and at home
            if (roomMate.infectionStatus == "Infectious" and roomMate.currentNode == self.home.node()):
                #infectionPercentage = (-23.28 * distance) + 20.0
                infectionPercentage = 20.0
                infectionPercentage /= (24 * 3600/ stepLength)
                if infectionPercentage > 0 and random.randint(0,int(10000)) < infectionPercentage*100:
                    self.infection = Infection(roomMate,self,currentStepNumber,location = "Home")
                    #print("I got infected!")
                    break
                
      
    def finalize(self,currentStepNumber):
        if self.infection != None:
            self.infection.finalize(currentStepNumber)