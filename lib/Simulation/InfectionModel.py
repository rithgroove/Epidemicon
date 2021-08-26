import random
import geopy
from enum import Enum
from .Infection import Infection
class InfectionType(Enum):
    AtBuilding = 1
    OnTheRoad = 2
    AtHome = 3
    OffMap = 4
    
class InfectionModel:
    def __init__(self, sim, osmMap, flatInfectionRate = 20.0, roadInfectionRate = 68.0, offMapInfectionRate = 20.0):
        self.flatInfectionRate = flatInfectionRate
        self.roadInfectionRate = roadInfectionRate
        self.offMapInfectionRate = offMapInfectionRate
        self.sim = sim
        self.osmMap = osmMap
        
    def infect(self, agent, stepSize,currentStepNumber):
        if agent.infectionStatus == "Susceptible":
            if (agent.currentNode == agent.home.node()):
                #infect at home
                self._infectAgent(agent,stepSize,currentStepNumber,infectionType = InfectionType.AtHome)
            elif agent.currentNode.isBuildingCentroid:
                if agent.currentNode.building == agent.mainJob.building and agent.mainJob.isOutsideCity():
                    #infect off map
                    self._infectAgent(agent,stepSize,currentStepNumber,infectionType = InfectionType.OffMap)
                else:
                    #infect at a building
                    self._infectAgent(agent,stepSize,currentStepNumber,infectionType = InfectionType.AtBuilding)
            else:
                #infect on the road
                self._infectAgent(agent,stepSize,currentStepNumber,infectionType = InfectionType.OnTheRoad)
        
        
    def _infectAgent(self,agent, stepSize, currentStepNumber, infectionType): 
        infectionPercentage = self.offMapInfectionRate/ (24 * 3600/ stepSize)
        if infectionType !=  InfectionType.OffMap:
            infectiousAgents = self._collectInfectiousAgent(agent, infectionType)
            for stranger in infectiousAgents:
                # Setup default flat infection rate
                infectionPercentage = self.flatInfectionRate/ (24 * 3600/ stepSize)
                
                if infectionType == InfectionType.OnTheRoad: 
                    # if on the road, change infection rate based on distance for the on the road infection
                    gradient = 5 - self.roadInfectionRate / 2
                    distance = stranger.currentLocation.calculateDistance(agent.currentLocation)                
                    infectionPercentage = ((gradient* distance) + self.roadInfectionRate)/(24 * 3600/ stepSize)
                    
                if infectionPercentage > 0 and random.uniform(0.0,100.0) < infectionPercentage: # infect
                    # non off map infection
                    location = "On the Road"
                    if (agent.currentNode.isBuildingCentroid):
                        location = agent.currentNode.building.type
                    agent.infection = Infection(stranger, 
                                               agent,
                                               currentStepNumber, 
                                               dormant = random.randint(24,72) *3600, #maybe put it in config?
                                               recovery = random.randint(72,14*24) *3600, #maybe put it in config?
                                               location = location) 
                    
        elif infectionPercentage > 0 and random.uniform(0.0,100.0) < infectionPercentage: # infect
            # off map infection
            self.infection = Infection(agent, 
                                       agent,
                                       currentStepNumber, 
                                       dormant = random.randint(24,72) *3600, #maybe put it in config?
                                       recovery = random.randint(72,14*24) *3600, #maybe put it in config?
                                       location = "Going out of simulated area")             
            
        
    def _collectInfectiousAgent(self, agent, infectionType):
        infectiousAgents = []

        # check for SameNode and SameAndConnectingNode
        if infectionType ==  InfectionType.AtBuilding or infectionType ==  InfectionType.OnTheRoad:
            for stranger in agent.currentNode.agents:
                if (stranger.infectionStatus == "Infectious"):
                    infectiousAgents.append(stranger)

        # check for ConnectingNode and SameAndConnectingNode
        if infectionType ==  InfectionType.OnTheRoad:
            for connectingNode in agent.currentNode.connections:
                for stranger in connectingNode.agents:
                    if (stranger.infectionStatus == "Infectious"):
                        infectiousAgents.append(stranger)

        # check for infection within household only
        if infectionType ==  InfectionType.AtHome:
            for roomMate in agent.home.occupants:
                #if room mate is infectious and at home
                if (roomMate.infectionStatus == "Infectious" and roomMate.currentNode == agent.home.node()):
                    infectiousAgents.append(roomMate)

        return infectiousAgents
        