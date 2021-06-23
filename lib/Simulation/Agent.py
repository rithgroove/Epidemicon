
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
        self.infection_status = "Susceptible"
        self.currentLocation = home.coordinate().newCoordinateWithTranslation()
        self.currentNode = home.node()
        self.oval = None
        self.name = ""
        self.speed = 1.46
        self.activeSequence = None
        self.osmMap = osmMap
        self.transition = (0,0)
        self.distanceToDestination = 0
        
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
            
    def checkInfection(self):
        if self.infection_status == "Susceptible":
            otherAgents = []
            for node in self.currentNode.connections:

    def infect(simulator):
        for x in simulator.agent:
            node = x.currentNode
            otherAgents = []
            for node in node.connections:
                for other agents = node.agents:
                    #check if agent position is within a certain number of meter
                    include to the other agents

        
    def finalize(self):
        if self.infection != None:
            self.infection.finalize