from .Coordinate import Coordinate

class Node():    
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - osmId : Open Street Map ID.
        - coordinate : coordinate 
        - isRoad : Boolean to mark whether this Node is a part of a road.
        - connection : List of all connected node.
        - ways : A dictionary of Open Street Map Ways.
        - tags :  dictionary of the Map Feature of this object (check Open Street Map - Map Features).
    """
    
    def __init__(self):
        """
        [Constructor]
        Initialize an empty node.
        """
        self.osmId = ""
        self.coordinate = Coordinate(0.0,0.0)
        self.isRoad = False
        self.connections = []
        self.ways = {}
        self.tags = {}
        
    def fill(self, osmNode):
        """
        [Method]fill        
        Fill up several property of this object, such as:
            - osmId
            - coordinate
            - isRoad
            - tags
        
        Parameter:
            - osmNode = osmium library node.
        """
        self.osmId = f"{osmNode.id}"
        self.coordinate = Coordinate(osmNode.location.lat,osmNode.location.lon)
        for tag in osmNode.tags:
            self.tags[tag.k] = tag.v
        if 'highway' in self.tags.keys():
            isRoad = True
        
    def addWay(self,way):
        """
        [Method] addWay
        Add an Open Street Map Way into the ways property.
        
        Parameter:
            - way = Namazu Way (not osmium "Way", osmium "Way" is deleted after the loop).
        """
        self.ways[way.osmId] = way
        
        
    def addConnection(self,connection):
        """
        [Method] addConnection
        Add a node that is connected to this node.
        
        Parameter:
            - connection = Namazu Node.
        """
        self.connections.append(connection)
            
    def __str__(self):        
        """
        [Method] __str__
        Generate the summarized node information string  and return it.
        
        Return: [string] String of summarized map Information.
        """
        tempstring = f"id: {self.osmId}\nlat = {self.coordinate.lat} lon = {self.coordinate.lon} \nnumber of ways : {self.ways.__len__()}\nnumber of connections : {self.connections.__len__()}\nTags : \n"
        for key in self.tags.keys():
            tempstring = tempstring + f"\t{key} : {self.tags[key]}\n"
        tempstring = tempstring + "\n"
        return tempstring