import geopy.distance as distance
from .Coordinate import Coordinate
class Building:
    """
    [Class] Map
    A class to represent the map
    
    Properties:
        - way: List of nodes that defines the shape of the building.
        - coordinate : the coordinate of the building's centroid
    """
    def __init__(self,way):
        self.way = way
        lat,lon = 0,0
        for i in range(0,way.nodes.__len__()-1):
            lat += way.nodes[i].lat
            lon += way.nodes[i].lon
        lat = self.lat/(way.nodes.__len__()-1)
        lon = self.lon/(way.nodes.__len__()-1)
        self.coordinate = Coordinate(lat,lon)
        #self.closestCell = None
    
    def getVector(self):
        return (self.destination.lat - self.start.lat, self.destination.lon - self.start.lon)
    
    def __str__(self):
        """
        [Method] __str__        
        return a string that summarized the road
        """
        temp = f"({self.start.lat},{self.start.lon}) to ({self.destination.lat},{self.destination.lon}) - {self.length}"
        return temp
    
    def getPosition(self):
            """
            [Method]getPosition
            get the latitude and longitude of the cell

            Return : (lat,lon)
            """
            return (self.lat,self.lon);