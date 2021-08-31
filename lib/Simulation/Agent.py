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
    def __init__(self,agentId, osmMap,age,job,gender = None):
        self.home = None
        
        if (gender is None):
            self.gender = random.choice(["M","F"])
        else:
            self.gender = gender
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
        self.hungerReduction = 1.0
        self.hungerCap = float(random.randint(40,65))/100.0
        self.eatingOutPref = float(random.randint(0,70))/10.0
        self.idle = 0
        self.energy = 100.0
        self.faveRetailer = self.osmMap.getRandomBuilding("retail")
        self.faveBarber = self.osmMap.getRandomBuilding("barbershop")
        self.risk = random.randint(1,3)
        self.status = "Normal"
        self.activities = "idle"
        self.vaccinated = False
        
    def setVaccinated(self, vaccinated = True):
    """
    [Method] setVaccinated
    set the vaccination status of the agent 
    
    Parameter:
        - vaccinated = [Bool] the vaccination status. Default value = True
    """
        self.vaccinated = vaccinated
        
    def setHome(self,home):
    """
    [Method] setHome
    set the home where this agent live
    
    Parameter:
        - home = [Home] the home object
    """
        self.home = home
        self.currentLocation = home.coordinate().newCoordinateWithTranslation()
        self.currentNode = home.node()
        
    def setMovementSequence(self, activeSequence):
    """
    [Method] setMovementSequence
    set the movement sequence for this agent
    
    Parameter =
        - home = [MovementSequence] the sequence calculated by pathfinding function
    """
        self.activeSequence = activeSequence
        
    def getSpeed(self):
    """
    [Method] getSpeed
    get the agent speed
    
    return:
        - [float] the agent's speed
        
    TODO: differentate speed if the agent use car / bus
    """
        return self.speed
    
    def checkSchedule(self,day,hour,steps=1):    
    """
    [Method] checkSchedule
    Check what kind of activity the agent will do at current point. If there's an activity, we will generate a movement sequence, if not return None. This also set the type of activity the agents will do. 
    
    parameter:
        - day = [int] current simulated day (0-7) 0 = Monday, 7 = Sunday
        - hour = [int] current simulated hour
        - steps = [int] step length in seconds
    
    return:
        - [MovementSequence] the movement sequence for the activity the agent will do
        
    Important: This method is being used by the StepThread.py which is a subclass of multiprocessing class. Hence why the method returns the movement sequence instead of just simply setting the sequence to the agents. In short, this method is not called by main thread but by subthread. 
    """    
        if (self.activeSequence is None or self.activeSequence.finished):

            if self.status == "Symptomatics":
                if self.currentNode != self.home.node():       
                    #print("I'm sick, I need to go home")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.home.building)
                    self.activities = "going home"
                elif self.hunger <= self.hungerCap:
                    #print("I'm sick, so I eat at home")
                    #self.home.consumeGroceries()
                    #hunger = 1.0
                    self.activities = "eat at home"
                elif self.home.groceries < len(self.home.occupants) * 2:
                    #print("I'm sick, but fridge are empty. I need to go to retailer")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.faveRetailer)
                    self.activities = "do groceries"
                    #self.home.buyGroceries()
                    #self.idle = 4800
            elif self.status == "Severe":
                if not self.currentNode.isBuildingCentroid or self.currentNode.building.type != "hospital":
                    self.activities = "go to hospital"
                    #print("I'm sick, I need to go to hospital")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.osmMap.getRandomBuilding("hospital"))
                elif self.hunger <= self.hungerCap:
                    #print("I'm sick, so I eat at hospital")
                    #hunger = 1.0
                    self.activities = "eat at hospital"
            elif self.mainJob.isWorking(day, hour):
                if self.currentNode != self.mainJob.building.node:     
                    self.activities = "go to work"            
                    #print(f"I'm {self.mainJob.getName()} Go to work at {self.mainJob.building.type}")
                    self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.mainJob.building)
            elif self.idle <= 0:
                if self.hunger <= self.hungerCap:
                    whereToEatProbability = random.randint(0,100)/100.0
                    if (whereToEatProbability <= self.eatingOutPref):
                        #print(f"agent id {self.agentId} is eating outside") 
                        self.activities = "go to restaurant"            
                        self.distanceToDestination,self.activeSequence = self.osmMap.findPath(self,self.osmMap.getRandomBuilding("restaurant"))
                        #self.idle = 4800
                        #hunger = 1.0
                    else:
                        #print("eat at home")
                        #need fixing if agents are not at home
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
    """
    [Method] step
    The actual step function used to trigger the movement sequence and move the agent position in the map.
    
    parameter:
        - day = [int] current simulated day (0-7) 0 = Monday, 7 = Sunday
        - hour = [int] current simulated hour
        - steps = [int] step length in seconds
    """    
        if (self.activities == "eat at home" and self.idle <= 0):
            self.home.consumeGroceries()
            #print(f"eat at home, agentId = {self.agentId} hunger = {self.hunger}, hungerCap = {self.hungerCap}")
            self.hunger = 1.0
            self.idle = 2400
            self.activities = "idle"
        elif (self.activities == "eat at hospital" and self.idle <= 0):
            self.hunger = 1.0
            self.activities = "idle"
        elif (self.activities == "go to restaurant" and self.idle <= 0 and self.currentNode.isBuildingCentroid and self.currentNode.building.type == "restaurant"):
            #print(f"eat outside, agentId = {self.agentId} hunger = {self.hunger}, hungerCap = {self.hungerCap}")
            self.hunger = 1.0
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
            self.home.buyGroceries()
        
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
            self.transition = self.activeSequence.getVector(self.currentLocation)
            self.currentLocation.translate(lat = self.transition[0], lon = self.transition[1])
      
    def finalize(self,currentStepNumber,stepLength):
    """
    [Method] finalize
    Method to update the agent SEIR and health status
    
    parameter:
        - currentStepNumber = [int] current step number in seconds
        - stepLength = [int] step length in seconds
    """    
        if self.infection != None:
            self.infection.finalize(currentStepNumber,stepLength)
            
    def extract(self):
    """
    [Method] extract
    Method to extract information of this agent into a dictionary
    
    return:
        -[Dictionary] = current information of the agent.
    """    
        temp = {}
        temp["agent_id"]=self.agentId
        temp["gender"] = self.gender
        temp["age"]=self.age
        temp["last_lat"] = self.currentLocation.lat
        temp["last_lon"] = self.currentLocation.lon
        if self.currentNode.isBuildingCentroid:
            temp["last_known_location"] = self.currentNode.building.type
        else:
            temp["last_known_location"] = "On the road"
        temp["last_node_id"] = self.currentNode.osmId
        
        temp["home_id"] = self.home.homeId
        temp["home_type"] = self.home.building.type
        temp["home_building_id"] = self.home.building.buildingId
        temp["home_lat"] = self.home.node().coordinate.lat
        temp["home_lon"] = self.home.node().coordinate.lon
        
        temp["profession"] = self.mainJob.jobClass.name
        temp["work_place"] = self.mainJob.building.buildingId
        temp["work_place_type"] =  self.mainJob.building.type
        temp["work_place_building_id"] =  self.mainJob.building.buildingId
        temp["work_place_lat"] =  self.mainJob.building.coordinate.lat
        temp["work_place_lon"] =  self.mainJob.building.coordinate.lon
        
        temp["last_infection_status"] = self.infectionStatus
        temp["last_health_status"] = self.status
        temp["last_activities"] = self.activities
        temp["eating_out_preference"] = self.eatingOutPref
        
        if (self.vaccinated):
            temp["vaccinated"] = "True"
        else:
            temp["vaccinated"] = "False"
        
        return temp
    
def getAgentKeys():
    """
    [Function] getAgentKeys
    Function to get all key for the Agent.extract() method.
    
    return:
        -[Array] = All the key for the Agent.extract() method
    """    
    temp = []
    temp.append("agent_id")
    temp.append("gender")
    temp.append("age")
    temp.append("last_lat")
    temp.append("last_lon")
    temp.append("last_known_location")
    temp.append("last_node_id")
    temp.append("home_id")
    temp.append("home_type")
    temp.append("home_building_id")
    temp.append("home_lat")
    temp.append("home_lon")
    temp.append("profession")
    temp.append("work_place")
    temp.append("work_place_type")
    temp.append("work_place_building_id")
    temp.append("work_place_lat")
    temp.append("work_place_lon")
    temp.append("last_infection_status")
    temp.append("last_health_status")
    temp.append("last_activities")
    temp.append("eating_out_preference")
    temp.append("vaccinated")
    return temp
