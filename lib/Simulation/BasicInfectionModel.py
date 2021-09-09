import random
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
    def __init__(self, sim, osmMap, flatInfectionRate = 0.2, roadInfectionRate = 0.68, offMapInfectionRate = 0.2):
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
        
    def infect(self, agent, stepSize,currentStepNumber):
        """
        [Method] infect 

        function to infect the agents

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - stepSize = [int] the step length
            - currentStepNumber = [int] current step number
        """
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
        """
        [Method] _buildingBasedInfection 

        private method to check for infection from agent in the same building/ in the same household in case of home

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - infectiousAgents = [array] array of infected Agents that is within proximity of the agent
            - stepSize = [int] the step length
            - currentStepNumber = [int] current step number
        """
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
        """
        [Method] _distanceBasedInfection 

        private method to check infection based on distance. Used for on the road infection.

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - infectiousAgents = [array] array of infected Agents that is within proximity of the agent
            - stepSize = [int] the step length
            - currentStepNumber = [int] current step number
        """
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
        """
        [Method] _infectOffMap 

        private method to check infection for agents that leaving the simulated area.

        Parameter:
            - agent = [Agent] susceptible agent that is going to be checked for infection
            - stepSize = [int] the step length
            - currentStepNumber = [int] current step number
        """
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
        