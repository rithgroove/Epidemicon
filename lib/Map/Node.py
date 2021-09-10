from .Coordinate import Coordinate

class Node():    
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - osmId             : Open Street Map ID.
        - coordinate        : coordinate 
        - isRoad            : Boolean to mark whether this Node is a part of a road.
        - connection        : List of all connected node.
        - ways              : A dictionary of Open Street Map Ways.
        - tags              : A dictionary of the Map Feature of this object (check Open Street Map - Map Features).
        - grid              : [Grid] The grid this node is in
        - movementSequences : [MovementSequence] Dictionary of previously generated movementSequences destination id is the key
        - agents            : [Agents] agents in this node (might replace it later with something)
    """
    
    def __init__(self):
        """
        [Constructor]
        Initialize an empty node.
        """
        self.osmId = ""
        self.hashId = 0
        self.coordinate = Coordinate(0.0,0.0)
        self.isRoad = False
        self.connections = []
        self.ways = {}
        self.tags = {}
        self.grid = None
        self.movementSequences = {}
        self.agents = []
        self.isBuildingCentroid = False
        self.building = None
        
    def fill(self, osmNode):
        """
        [Method]fill        
        Fill up several property of this object, such as:
            - osmId
            - coordinate
            - isRoad
            - tags
        
        Parameter:
            - osmNode = List of osmium library node.
        """
        self.osmId = f"{osmNode.id}"
        self.coordinate = Coordinate(osmNode.location.lat,osmNode.location.lon)
        for tag in osmNode.tags:
            self.tags[tag.k] = tag.v
        if 'highway' in self.tags.keys():
            self.isRoad = True
        self.generateHashId()
            
    def setAsBuildingConnector(self, coordinate, generatedId =""):
        """
        [Method]fill        
        Fill up several property of this object, such as:
            - osmId
            - lat
            - lon
            - isRoad
            - tags
        
        Parameter:
            - osmNode = osmium library node.
        """
        self.osmId = f"{generatedId}"
        self.coordinate = coordinate
        self.isRoad = True
        self.generateHashId()

    def generateHashId(self):
        x, y = self.coordinate.getLatLon()
        x *= 1000
        y *= 1000
        self.hashId = hash((x,y))
        
    def addWay(self,way):
        """
        [Method] addWay
        Add an Open Street Map Way into the ways property.
        
        Parameter:
            - way = [Way] the way (not osmium "Way", osmium "Way" is deleted after the loop).
        """
        self.ways[way.osmId] = way
        
        
    def addConnection(self,connection):
        """
        [Method] addConnection
        Add a node that is connected to this node.
        
        Parameter:
            - connection = [Node] The node (not osmium "Node", osmium "Node" is deleted after the loop).
        """
        self.connections.append(connection)
        
    def removeConnection(self,connection):
        """
        [Method] removeConnection
        Remove a node that is connected to this node.
        
        Parameter:
            - connection = [Node] The node (not osmium "Node", osmium "Node" is deleted after the loop).
        """
        self.connections.remove(connection)
        
        
    def addAgent(self,agent):
        """
        [Method] addAgent
        Add an agent that is in this node (Agent are not part of this module). This is created to help the simulation model.
        
        Parameter:
            - agent = [Object] Any agent
        """
        self.agents.append(agent)
        
    def removeAgent(self,agent):
        """
        [Method] removeConnection
        Remove an agent that is in this node (Agent are not part of this module). This is created to help the simulation model.
        
        Parameter:
            - connection = [Node] The node (not osmium "Node", osmium "Node" is deleted after the loop).
        """
        self.agents.remove(agent)
            
    def __str__(self):        
        """
        [Method] __str__
        Generate the summarized node information string  and return it.
        
        Return: [string] String of summarized map Information.
        """
        tempstring = f"id: {self.osmId}\n"
        tempstring = tempstring + f"lat = {self.coordinate.lat} lon = {self.coordinate.lon}\n"
        tempstring = tempstring + f"number of ways : {self.ways.__len__()}\n"
        tempstring = tempstring + f"number of connections : {self.connections.__len__()}\n"
        tempstring = tempstring + f"Tags : \n"        
        for key in self.tags.keys():
            tempstring = tempstring + f"\t{key} : {self.tags[key]}\n"
        tempstring = tempstring + "\n"
        return tempstring
    
    def calculateDistance(self,targetNode):
        """
        [Method] calculateDistance
        calculateDistance to other nodes
        
        Return: [Double] Distance in KM
        """
        return self.coordinate.calculateDistance(targetNode.coordinate)
        
    def addMovementSequence(self,sequence):
        """
        [Method] addMovementSequence
        save a calculated sequence to our node
        
        Parameter:
            - sequence : [MovementSequence] the movement sequence
        """
        #print(sequence.destination.osmId)
        self.movementSequences[sequence.destination.osmId]  = sequence
        
    def getMovementSequence(self,targetNode):
        """
        [Method] getMovementSequence
        get the previously generated movementSequence (return none if not found)
        
        Parameter:
            - targetNode: the destinationNode
            
        return: [MovementSequence] a clone of the previously generated movement sequence or None 
        """
        #print(targetNode.osmId)
        if (targetNode.osmId in self.movementSequences.keys()):
            return self.movementSequences[targetNode.osmId].clone()
        return None

    def setBuilding(self,building):
        self.building = building
        self.isBuildingCentroid = True