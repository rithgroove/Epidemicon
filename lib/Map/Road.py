import geopy.distance as distance

class Road:
    """
    [Class] Road
    A class to represent the Road.
    
    Properties:
        - name : road name.
        - start : starting node.
        - destination : [Coordinate] destination node.
        - distance : [Coordinate] road length
    """
    def __init__(self,origin, dest):
        """
        [Constructor]
        Initialize road.
        
        Parameter:
            - origin = [Coordinate] starting node
            - dest = [Coordinate] destination node
        """
        self.name,self.start,self.destination = genName(origin,dest)
        self.length = self.start.calculateDistance(dest)
        
    def getPath(self):
        """
        [Method] getPath
        Get a tuple of starting location and destination
                
        return: Tuple of 2 coordinate start,destination)
        """
        return (self.start, self.destination)        
    
    def getVector(self):
        """
        [Method] getVector
        Get the vector that represent the distance between staring point and the destination
                
        return: get vector that represent distance from two points (lat)
        """
        return (self.destination.lon - self.start.lon, self.destination.lat - self.start.lat)
    
    def __str__(self):
        """
        [Method] __str__        
        return a string that summarized the road
        """
        temp = f"staring = (lat = {self.start.coordinate.lat}, lon = {self.start.coordinate.lon})\n"
        temp = temp + f"destination = (lat = {self.destination.coordinate.lat}, lon = {self.destination.coordinate.lon})\n"
        temp = temp + f"distance = {self.length/1000}km" 
        return temp
    
def genName(node1, node2):
    """
    [Function] genName        
    a function return the name of the road. The name itself will be ordered by OSM_ID
    
    Parameter:
        - node1 = starting node
        - node2 = destination node
    """
    name = None
    start = None 
    destination = None
    if (node1.osmId < node2.osmId):
        name = f"{node1.osmId}-{node2.osmId}"
        start = node1 
        destination = node2 
    else:
        name = f"{node2.osmId}-{node1.osmId}"        
        start = node2
        destination = node1
    return (name, start, destination)
    