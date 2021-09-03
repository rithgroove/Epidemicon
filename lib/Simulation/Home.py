import random
class Home:
    """
    [Class] Home
    
    
    Properties:
        - building: [Building] the building the house is in
        - occupants :[List of Agent] the agents that live inside this home
        - agents : [List of Agent] the agents that is currently inside this home
    """
    def __init__(self,building,homeId):
        """
        [Constructor]
        Initialize an empty home

        Parameter:
            - building: [Building] the building the house is in
        """
        self.homeId = homeId
        self.building = building
        self.occupants = []
        self.agents = []
        self.groceries = random.randint(6,15)
    
    def addOccupant(self,occupant):
        """
        [Method] addOccupants
        Add an occupant

        Parameter:
            - occupants: [Agents the agent that live inside this home
        """
        self.occupants.append(occupant)
    
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
        """
        [Method] coordinate        
        return the building coordinate
        """
        return self.building.coordinate
    
    def node(self):
        """
        [Method] node        
        return the building node
        """
        return self.building.node
    
    def buyGroceries(self):
        """
        [Method] buyGroceries        
        method to add stock of food at home. 
        """
        self.groceries += len(self.occupants) * 6
    
    def consumeGroceries(self):
        """
        [Method] consumeGroceries        
        method to consume 1 portion of the groceries stock.
        """
        self.groceries -= 1
        
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