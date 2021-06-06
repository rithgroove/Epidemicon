
class Home:
    """
    [Class] Home
    
    
    Properties:
        - building: [Building] the building the house is in
        - occupants :[List of Agent] the agents that live inside this home
        - agents : [List of Agent] the agents that is currently inside this home
    """
    def __init__(self,building):
        """
        [Constructor]
        Initialize an empty home

        Parameter:
            - building: [Building] the building the house is in
        """
        self.building = building
        self.occupants = []
    
    def addOccupants(self,occupants):
        """
        [Method] addOccupants
        Add more occupants

        Parameter:
            - occupants: [List of agents] the agents that live inside this home
        """
        self.occupants.extend(occupants)
    
    def addAgents(self,agent):
        """
        [Method] addOccupants
        Add more occupants

        Parameter:
            - occupants: [agents] the agent that comes inside this building
        """
        self.agents.append(agent)
    
    def removeAgents(self,agent):
        """
        [Method] addOccupants
        Add more occupants

        Parameter:
            - occupants: [agents] the agent that comes inside this building
        """
        self.agents.remove(agent)
        
    def coordinate(self):
        return self.building.coordinate
    
    def node(self):
        return self.building.node
    
    def __str__(self):
        """
        [Method] __str__        
        return a string that summarized the building
        """
        tempstring = self.building.__str__()
        tempstring = tempstring + f"\n\tcurrent agents count : {len(self.agents)}\n"
        tempstring = tempstring + f"\tnumber of occupant : {len(self.agents)}\n"
        tempstring = tempstring + f"Current Agents : \n"
        for agent in self.agents:
            tempstring = tempstring +"\n" + agent.__str__()
        tempstring = tempstring + "\n"
        return tempstring