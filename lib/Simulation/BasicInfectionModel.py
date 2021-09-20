#import random
import geopy
from enum import Enum
from .Infection import Infection
class InfectionType(Enum):
    """
    [Class] InfectionType 
    
    an Enum class that have 4 different enumeeration
    
    Enums:
        - AtBuilding
        - OnTheRoad
        - AtHome
        - OffMap
    """
    AtBuilding = 1
    OnTheRoad = 2
    AtHome = 3
    OffMap = 4
    
class BasicInfectionModel:
    """
    [Class] BasicInfectionModel
    Simple infection model that covers : infection at home, at building, on the road, and outside of simulation area.
    Each properties with infectionRate is a float with value between 0.0 - 1.0 per day infection chance.
    
    Properties:
        - sim = [Simulator] the simulator
        - osmMap = [Map] the map used in our simulation
        - flatInfectionRate = [float] a value from 0.0 to 1.0 per day and used in calculating infection in building and home
        - roadInfectionRate = [float] maximum infection rate if the agent is standing next to infected agent on the road
        - offMapInfectionRate = [float] infection rate if the agent leaves the simulation area
    """
    def __init__(self, sim, osmMap, flatInfectionRate = 0.1, roadInfectionRate = 0.68, offMapInfectionRate = 0.1):
        """
        [Constructor] 
        Constructor for this class

        Parameter:
            - sim = [Simulator] the simulator
            - osmMap = [Map] the map used in our simulation
            - flatInfectionRate = [float] infection chance and used in calculating infection in building and home
            - roadInfectionRate = [float] maximum infection rate if the agent is standing next to infected agent on the road
            - offMapInfectionRate = [float] infection rate if the agent leaves the simulation area
        """
        self.flatInfectionRate = flatInfectionRate
        self.roadInfectionRate = roadInfectionRate
        self.offMapInfectionRate = offMapInfectionRate
        self.sim = sim
        self.osmMap = osmMap
        
    def setRNG(self,rng):
        self.rng = rng

    def infect(self, agent, stepSize, timeStamp):
        """
        [Method] infect 

        function to infect the agents

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - stepSize = [int] the step length
            - timeStamp = [TimeStamp] current timestamp
        """
        if agent.infectionStatus == "Susceptible":
            if (agent.currentNode == agent.home.node()):
                #infect at home
                infectiousAgents = self._collectInfectiousAgent(agent, InfectionType.AtHome)
                self._buildingBasedInfection(agent, infectiousAgents, stepSize, timeStamp)
            elif agent.currentNode.isBuildingCentroid:
                if agent.currentNode.building == agent.mainJob.building and agent.mainJob.isOutsideCity():
                    #infect off map
                    self._infectOffMap(agent,stepSize,timeStamp)
                else:
                    #infect at a building
                    infectiousAgents = self._collectInfectiousAgent(agent, InfectionType.AtBuilding)
                    self._buildingBasedInfection(agent, infectiousAgents, stepSize, timeStamp)
            else:
                #infect on the road
                infectiousAgents = self._collectInfectiousAgent(agent, InfectionType.OnTheRoad)
                self._distanceBasedInfection(agent, infectiousAgents, stepSize, timeStamp)
        
                    
    def _buildingBasedInfection(self,agent, infectiousAgents, stepSize, timeStamp):
        """
        [Method] _buildingBasedInfection 

        private method to check for infection from agent in the same building/ in the same household in case of home

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - infectiousAgents = [array] array of infected Agents that is within proximity of the agent
            - stepSize = [int] the step length
            - timeStamp = [TimeStamp] current timestamp
        """
        for stranger in infectiousAgents:
            infectionProbability = self.flatInfectionRate/ (24 * 3600/ stepSize)
            if infectionProbability > 0 and self.rng.uniform(0.0,1.0) < infectionProbability: # infect
                agent.infection = Infection(stranger, 
                                           agent,
                                           timeStamp, 
                                           dormant = self.rng.integers(24,72) *3600, #maybe put it in config?
                                           recovery = self.rng.integers(72,14*24) *3600, #maybe put it in config?
                                           location = agent.currentNode.building.type) 
                break 
        
    def _distanceBasedInfection(self,agent, infectiousAgents, stepSize, timeStamp):
        """
        [Method] _distanceBasedInfection 

        private method to check infection based on distance. Used for on the road infection.

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - infectiousAgents = [array] array of infected Agents that is within proximity of the agent
            - stepSize = [int] the step length
            - timeStamp = [TimeStamp] current timestamp
        """
        gradient = 0.01 - self.roadInfectionRate / 1.5
        for stranger in infectiousAgents:
            distance = stranger.currentLocation.calculateDistance(agent.currentLocation)                
            infectionProbability = ((gradient* distance) + self.roadInfectionRate)/(24 * 3600/ stepSize)
            if infectionProbability > 0 and self.rng.uniform(0.0,1.0) < infectionProbability: # infect
                agent.infection = Infection(stranger, 
                                           agent,
                                           timeStamp, 
                                           dormant = self.rng.integers(24,72) *3600, #maybe put it in config?
                                           recovery = self.rng.integers(72,14*24) *3600, #maybe put it in config?
                                           location = "On the Road") 
                break 
        
        
    def _infectOffMap(self,agent, stepSize, timeStamp):
        """
        [Method] _infectOffMap 

        private method to check infection for agents that leaving the simulated area.

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - stepSize = [int] the step length
            - timeStamp = [TimeStamp] current timestamp
        """
        infectionProbability = self.offMapInfectionRate/ (24 * 3600/ stepSize)
        if infectionProbability > 0 and self.rng.uniform(0.0,1.0) < infectionProbability: # infect
            # off map infection
            agent.infection = Infection(agent, 
                                       agent,
                                       timeStamp, 
                                       dormant = self.rng.integers(24,72) *3600, #maybe put it in config?
                                       recovery = self.rng.integers(72,14*24) *3600, #maybe put it in config?
                                       location = "Going out of simulated area")          
                
    def _collectInfectiousAgent(self, agent, infectionType):
        """
        [Method] _collectInfectiousAgent 

        private method to collect infectious agents depending of the infection type.

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - infectionType = [InfectionType] the type of infection
            
        Return:
            - [array] list of infectious agents based on the infection type.
        """
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
        