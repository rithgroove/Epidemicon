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
        self.hunger = float(random.randint(2,10))/10.0
        self.hungerReduction = 1.5
        self.eatingOutPref = float(random.randint(0,10))/10.0
        self.idle = 0
        self.energy = 100.0
        self.faveRetailer = self.osmMap.getRandomBuilding("retail")
        self.faveBarber = self.osmMap.getRandomBuilding("barbershop")
        self.risk = random.randint(1,3)
        self.status = "Normal"
        self.activities = "idle"
        
    def setHome(self,home):
        self.home = home
        self.currentLocation = home.coordinate().newCoordinateWithTranslation()
        self.currentNode = home.node()
        
    def setMovementSequence(self, activeSequence):
        self.activeSequence = activeSequence
        
    def getSpeed(self):
        return self.speed
    
    def checkSchedule(self,day,hour,steps=1):        
        if (self.activeSequence is None and self.activeSequence.finished):

            if self.status == "Symptomatics":
                if self.currentNode != self.home.node():       
                    #print("I'm sick, I need to go home")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.home.building)
                    self.activities = "going home"
                elif self.hunger <= 0.65:
                    #print("I'm sick, so I eat at home")
                    #self.home.consumeGroceries()
                    #hunger = 1.0
                    self.activities = "eat at home"
                elif self.home.groceries < len(self.home.occupants) * 2:
                    print("I'm sick, but fridge are empty. I need to go to retailer")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.faveRetailer)
                    self.activities = "do groceries"
                    #self.home.buyGroceries()
                    #self.idle = 4800
            elif self.status == "Severe":
                if not self.currentNode.isBuildingCentroid or self.currentNode.building.type != "hospital":
                    self.activities = "go to hospital"
                    #print("I'm sick, I need to go to hospital")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.osmMap.getRandomBuilding("hospital"))
                elif self.hunger <= 0.65:
                    #print("I'm sick, so I eat at hospital")
                    #hunger = 1.0
                    self.activities = "eat at hospital"
            elif self.mainJob.isWorking(day, hour):
                if self.currentNode != self.mainJob.building.node:     
                    self.activities = "go to work"            
                    #print(f"I'm {self.mainJob.getName()} Go to work at {self.mainJob.building.type}")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.mainJob.building)
            elif self.idle <= 0:
                if self.hunger <= 0.65:
                    whereToEatProbability = random.randint(0,10)
                    if (whereToEatProbability <= self.eatingOutPref):
                        print(f"agent id {self.agentId} is eating outside") 
                        self.activities = "go to restaurant"            
                        self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.osmMap.getRandomBuilding("restaurant"))
                        #self.idle = 4800
                        #hunger = 1.0
                    else:
                        #print("eat at home")
                        self.activities = "eat at home"
                        #self.home.consumeGroceries()
                        #hunger = 1.0
                        #self.idle = 4800
                elif self.hair > self.hairCap:
                    #print("going to barbershop")
                    self.activities = "go to barbershop"            

                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.faveBarber)
                    #self.hair = float(random.randint(0,int(self.hairCap/2)))
                    #self.idle = 4800
                elif self.home.groceries < len(self.home.occupants) * 2:
                    #print("go to retail")
                    self.activities = "do groceries"          
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.faveRetailer)
                    #self.home.buyGroceries()
                    #self.idle = 4800
                elif self.currentNode != self.home.node():       
                    #print("go home")
                    self.activities = "going home"  
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.home.building)
            
        if (self.activeSequence is not None and self.activeSequence.new):
            return self.activeSequence.extract()
        return None
                #gohome    
                
    def step(self,day,hour,steps=1):
        if (self.activities == "eat at home" and self.idle <= 0):
            self.home.consumeGroceries()
            hunger = 1.0
            self.idle = 2400
            self.activities = "idle"
        elif (self.activities == "eat at hospital" and self.idle <= 0):
            hunger = 1.0
            self.activities = "idle"
        elif (self.activities == "go to restaurant" and self.idle <= 0 and self.currentNode.isBuildingCentroid and self.currentNode.building.type == "restaurant"):
            hunger = 1.0
            self.idle = 2400
            self.activities = "idle"
        elif (self.activities == "go to barbershop" and self.idle <= 0 and self.currentNode.isBuildingCentroid and self.currentNode.building.type == "barbershop"):
            self.hair = float(random.randint(0,int(self.hairCap/2)))
            self.idle = 2400 #agents actually wait in the destination for 2 hour because the hourly checkschedule function
            self.activities = "idle"
        elif (self.activities == "do groceries" and self.idle <= 0 and self.currentNode.isBuildingCentroid and self.currentNode.building.type == "retail"):
            self.hair = float(random.randint(0,int(self.hairCap/2)))
            self.idle = 2400 #agents actually wait in the destination for 2 hour because the hourly checkschedule function
            self.activities = "idle"
        elif (self.activities == "do groceries" and self.idle <= 0 and self.currentNode.isBuildingCentroid and self.currentNode.building.type == "retail"):
            self.hair = float(random.randint(0,int(self.hairCap/2)))
            self.idle = 2400 #agents actually wait in the destination for 2 hour because the hourly checkschedule function
            self.activities = "idle"
            
            
        
        
        self.hair += 0.44/(24*(3600/steps))
        self.hunger -= self.hungerReduction/(24*(3600/steps))
        self.idle -= steps
        
        if self.activeSequence is not None and self.idle <= 0:
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
                    self.infection = Infection(stranger,self,currentStepNumber, dormant = random.randint(24,72) *3600,recovery = random.randint(72,14*24) *3600,  location = "On The Road")
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
                            self.infection = Infection(stranger,self,currentStepNumber, dormant = random.randint(24,72) *3600,recovery = random.randint(72,14*24) *3600, location = "On The Road")
                            #print("I got infected!")
                            break
        
        
    def infectFromOutsideOfCity(self,currentStepNumber,stepLength):
        if random.randint(0,int(10000)) < 200/(24*3600/stepLength) :
            self.infection = Infection(self,self,currentStepNumber, dormant = random.randint(24,72) *3600, recovery = random.randint(72,14*24) *3600, location = "Going out of city")
            
                                
    def infectAtBuilding(self,currentStepNumber,stepLength):
        for stranger in self.currentNode.agents:
            #if room mate is infectious and at home
            if (stranger.infectionStatus == "Infectious"):
                #infectionPercentage = (-23.28 * distance) + 20.0
                infectionPercentage = 20.0
                infectionPercentage /= (24 * 3600/ stepLength)
                if infectionPercentage > 0 and random.randint(0,int(10000)) < infectionPercentage*100:
                    self.infection = Infection(stranger,self,currentStepNumber, dormant = random.randint(24,72) *3600,recovery = random.randint(72,14*24) *3600, location = self.currentNode.building.type)
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
                    self.infection = Infection(roomMate,self,currentStepNumber, dormant = random.randint(24,72) *3600, recovery = random.randint(72,14*24) *3600, location = "Home")
                    #print("I got infected!")
                    break
                
      
    def finalize(self,currentStepNumber,stepLength):
        if self.infection != None:
            self.infection.finalize(currentStepNumber,stepLength)