import itertools
from .Coordinate import Coordinate
class Building:
    """
    [Class] Building
    A class to represent the Building
    
    Properties:
        - way: List of nodes that defines the shape of the building.
        - coordinate : the coordinate of the building's centroid
    """
    idCounter = itertools.count().__next__
    def __init__(self, way):
        """
        [Constructor]
        Initialize the building building

        Parameter:
            - way: [Way] the building outline from Open Street Map
        """
        self.buildingId = self.idCounter()
        self.way = way
        lat,lon = 0,0
        for node in way.nodes[:-1]:
            lat += node.coordinate.lat
            lon += node.coordinate.lon
        lat = lat/(way.nodes.__len__()-1)
        lon = lon/(way.nodes.__len__()-1)
        self.coordinate = Coordinate(lat,lon)
        self.closestRoad = None
        self.entryPoint = None
        self.entryPointNode = None
        self.tags = way.tags
        self.setType(self.tags.get("building"))
        if self.type == "yes" and "amenity" in self.tags.keys():
            self.setType(self.tags.get("amenity"))
        self.node = None
        self.content = {}
        
    def __str__(self):
        """
        [Method] __str__        
        return a string that summarized the building
        """
        tempstring = f"[Building]\n"
        tempstring = tempstring + f"id: {self.way.osmId}\n"
        tempstring = tempstring + f"number of nodes : {self.way.nodes.__len__()}\n"
        tempstring = tempstring + f"Tags : \n"
        for key in self.tags.keys():
            tempstring = tempstring + f"\t{key} : {self.tags[key]}\n"
        tempstring = tempstring + "\n"
        return tempstring
    
    def getPosition(self):
        """
        [Method]getPosition
        get the latitude and longitude of the cell

        Return : (lat,lon)
        """
        return (self.lat,self.lon);
   
    def setType(self, buildingType):
        self.type = buildingType
        self.color = "#CCCCCC"
        houseType = ["residential","apartments","house"]
        if (self.type in houseType):
            self.color = "#99CC99"