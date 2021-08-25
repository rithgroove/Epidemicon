import random
import geopy
from enum import Enum
class InfectionType(Enum):
    SameNode = 1
    ConnectingNode = 2
    SameAndConnectingNode = 3
    HouseHold = 4
    OffMap = 8
    
class Infect:
    def __init__(self, flatInfectionRate = 20.0, roadInfectionRate = 68.0, offMapInfectionRate = 20.0):
        self.flatInfectionRate = flatInfectionRate
        self.roadInfectionRate = roadInfectionRate
        self.offMapInfectionRate = offMapInfectionRate
        
    def infectAgents(self,agent, infectionType = InfectionType.SameNode, useDistance = False, stepLength, currentStepNumber): 
        infectionPercentage = self.offMapInfectionRate/ (24 * 3600/ stepLength)
        if infectionType < 8:
            infectiousAgents = self._collectInfectiousAgent(agent, infectionType)
            gradient = 5 - self.roadInfectionRate / 2
            for stranger in infectiousAgents:
                #flat infection rate
                infectionPercentage = self.flatInfectionRate/ (24 * 3600/ stepLength)
                if usedistance:
                    #if use distance go here
                    distance = stranger.currentLocation.calculateDistance(self.currentLocation)                
                    # daily infection chance
                    infectionPercentage = (gradient* distance) + self.roadInfectionRate
                    # reduce it to step-length based Infection chance
                    infectionPercentage /= (24 * 3600/ stepLength)
                # randomized
                if infectionPercentage > 0 and random.uniform(0.0,100.0) < infectionPercentage:
                    agent.infection = Infection(stranger, 
                                               agent,
                                               currentStepNumber, 
                                               dormant = random.randint(24,72) *3600,
                                               recovery = random.randint(72,14*24) *3600, 
                                               location = self.currentNode.building.type)                                    
        else if infectionPercentage > 0 and random.uniform(0.0,100.0) < infectionPercentage:
            self.infection = Infection(agent, 
                                       agent,
                                       currentStepNumber, 
                                       dormant = random.randint(24,72) *3600,
                                       recovery = random.randint(72,14*24) *3600, 
                                       location = self.currentNode.building.type)             
            
        
    def _collectInfectiousAgent(self, agent, infectionType):
        infectiousAgents = []

        # check for SameNode and SameAndConnectingNode
        if infectionType % 2 == 1:  
            for stranger in agent.currentNode.agents:
                if (stranger.infectionStatus == "Infectious"):
                    infectiousAgents.append(stranger)

        # check for ConnectingNode and SameAndConnectingNode
        if infectionType & 2 != 0
            for connectingNode in agent.currentNode.connections:
                for stranger in connectingNode.agents:
                    if (stranger.infectionStatus == "Infectious"):
                        infectiousAgents.append(stranger)

        # check for infection within household only
        if infectionType == 4:
            for roomMate in agent.home.occupants:
                #if room mate is infectious and at home
                if (roomMate.infectionStatus == "Infectious" and roomMate.currentNode == self.home.node()):
                    infectiousAgents.append(roomMate)

        return infectiousAgents
        