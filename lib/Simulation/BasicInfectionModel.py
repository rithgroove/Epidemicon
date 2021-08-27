import random
import geopy
from enum import Enum
from .Infection import Infection
class InfectionType(Enum):
    AtBuilding = 1
    OnTheRoad = 2
    AtHome = 3
    OffMap = 4
    
class BasicInfectionModel:
    def __init__(self, sim, osmMap, flatInfectionRate = 0.2, roadInfectionRate = 0.68, offMapInfectionRate = 0.2):
        self.flatInfectionRate = flatInfectionRate
        self.roadInfectionRate = roadInfectionRate
        self.offMapInfectionRate = offMapInfectionRate
        self.sim = sim
        self.osmMap = osmMap
        
    def infect(self, agent, stepSize,currentStepNumber):
        if agent.infectionStatus == "Susceptible":
            if (agent.currentNode == agent.home.node()):
                #infect at home
                infectiousAgents = self._collectInfectiousAgent(agent, InfectionType.AtHome)
                self._buildingBasedInfection(agent, infectiousAgents, stepSize, currentStepNumber)
            elif agent.currentNode.isBuildingCentroid:
                if agent.currentNode.building == agent.mainJob.building and agent.mainJob.isOutsideCity():
                    #infect off map
                    self._infectOffMap(agent,stepSize,currentStepNumber)
                else:
                    #infect at a building
                    infectiousAgents = self._collectInfectiousAgent(agent, InfectionType.AtBuilding)
                    self._buildingBasedInfection(agent, infectiousAgents, stepSize, currentStepNumber)
            else:
                #infect on the road
                infectiousAgents = self._collectInfectiousAgent(agent, InfectionType.OnTheRoad)
                self._distanceBasedInfection(agent, infectiousAgents, stepSize, currentStepNumber)
        
                    
    def _buildingBasedInfection(self,agent, infectiousAgents, stepSize, currentStepNumber):
        for stranger in infectiousAgents:
            infectionProbability = self.flatInfectionRate/ (24 * 3600/ stepSize)
            if infectionProbability > 0 and random.uniform(0.0,1.0) < infectionProbability: # infect
                agent.infection = Infection(stranger, 
                                           agent,
                                           currentStepNumber, 
                                           dormant = random.randint(24,72) *3600, #maybe put it in config?
                                           recovery = random.randint(72,14*24) *3600, #maybe put it in config?
                                           location = agent.currentNode.building.type) 
                break 
        
    def _distanceBasedInfection(self,agent, infectiousAgents, stepSize, currentStepNumber):
        gradient = 0.05 - self.roadInfectionRate / 2.0
        for stranger in infectiousAgents:
            distance = stranger.currentLocation.calculateDistance(agent.currentLocation)                
            infectionProbability = ((gradient* distance) + self.roadInfectionRate)/(24 * 3600/ stepSize)
            if infectionProbability > 0 and random.uniform(0.0,1.0) < infectionProbability: # infect
                agent.infection = Infection(stranger, 
                                           agent,
                                           currentStepNumber, 
                                           dormant = random.randint(24,72) *3600, #maybe put it in config?
                                           recovery = random.randint(72,14*24) *3600, #maybe put it in config?
                                           location = "On the Road") 
                break 
        
        
    def _infectOffMap(self,agent, stepSize, currentStepNumber):
        infectionProbability = self.offMapInfectionRate/ (24 * 3600/ stepSize)
        if infectionProbability > 0 and random.uniform(0.0,1.0) < infectionProbability: # infect
            # off map infection
            self.infection = Infection(agent, 
                                       agent,
                                       currentStepNumber, 
                                       dormant = random.randint(24,72) *3600, #maybe put it in config?
                                       recovery = random.randint(72,14*24) *3600, #maybe put it in config?
                                       location = "Going out of simulated area")          
                
    def _collectInfectiousAgent(self, agent, infectionType):
        infectiousAgents = []

        # check the same node for at the building / on the road infection
        if infectionType ==  InfectionType.AtBuilding or infectionType ==  InfectionType.OnTheRoad:
            for stranger in agent.currentNode.agents:
                if (stranger.infectionStatus == "Infectious"):
                    infectiousAgents.append(stranger)

        # check for connecting node for the on the road infection
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
        