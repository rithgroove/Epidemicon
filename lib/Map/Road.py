import geopy.distance as distance
import math
from .Coordinate import Coordinate
from .Node import Node
class Road:
    """
    [Class] Road
    A class to represent the Road.
    
    Properties:
        - name : road name.
        - start : [Node] starting node.
        - destination : [Node] destination node.
        - distance : road length
        - buildings : buildings in this road
    """
    def __init__(self,origin, dest, way = None):
        """
        [Constructor]
        Initialize road.
        
        Parameter:
            - origin = [Node] starting node
            - dest = [Node] destination node
        """       
        self.name,self.start,self.destination = genName(origin,dest)
        self.length = self.start.calculateDistance(dest)
        self.buildings = []
        self.type = "Other"
        self.width = 4
        self.oneWay = False
        self.color = "#333333"
        self.lanes = 1 
        #types = ["tertiary","secondary","primary","residential", "trunk", "trunk_link", "primary_link", "secondary_link", "service","path"]
        types = ["footway","pedestrian","track","steps"]
        if way is not None:
            if "highway" in way.tags.keys():
                self.type = way.tags["highway"]
                if self.type in types:
                    self.width = 4
                    self.color = "#777777"
            if "lanes" in way.tags.keys():
                #self.width = float(way.tags["lanes"]) * 4
                self.lanes = way.tags["lanes"]
            if "oneway" in way.tags.keys():
                self.oneWay = way.tags["oneway"] == "yes"
                
                
    def getPath(self):
        """
        [Method] getPath
        Get a tuple of starting location and destination
                
        return: Tuple of 2 coordinate start,destination)
        """
        return (self.start, self.destination)        
        
    def getPathForRendering(self):
        """
        [Method] getPath
        Get a tuple of starting location and destination
                
        return: Tuple of 2 coordinate start,destination)
        """
        return (self.start.coordinate.lon,self.start.coordinate.lat, self.destination.coordinate.lon, self.destination.coordinate.lat)        
    
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
    
    def distanceToCoordinate(self, coordinate):
        a =  max(self.start.coordinate.calculateDistance(coordinate),self.destination.coordinate.calculateDistance(coordinate))
        b =  min(self.start.coordinate.calculateDistance(coordinate),self.destination.coordinate.calculateDistance(coordinate))
        c = self.start.coordinate.calculateDistance(self.destination.coordinate)
        s = (a+b+c)/2
        area =s*(s-a)*(s-b)*(s-c)
        if (area < 0):
            print("error, Heron's formula is not working due to very small angle")
            return 1000000000000000
            #print(self.start)
            #print(self.destination)
            #print(coordinate)
            #print(f"a={a}")
            #print(f"b={b}")
            #print(f"c={c}")
            #print(f"s={s}")
            #print(f"area={area}")
        area = math.sqrt(area)
        height = 2*area/c
        sinq = height/a
        q = math.asin(sinq)
        e = a * math.cos(q)
        if (e > c or q > math.pi):
            height = min(a,b)
        return height
    
    def getClosestCoordinate(self, coordinate):
        """
        [Method] getClosestCoordinate
        Method to get the closest coordinate in this road
        
        Parameter:
            - coordinate: the coordinate that we wanted to find the closest coordinate within road.
        """
        height = self.distanceToCoordinate(coordinate)
        a =  max(self.start.coordinate.calculateDistance(coordinate),self.destination.coordinate.calculateDistance(coordinate))
        b =  min(self.start.coordinate.calculateDistance(coordinate),self.destination.coordinate.calculateDistance(coordinate))
        c = self.start.coordinate.calculateDistance(self.destination.coordinate)
        
        sinq = height/a
        if (sinq > 1):
            return None
        q = math.asin(sinq)
        e = a * math.cos(q)
        if (e > c or q > math.pi):
            if (a<b):
                #print("return start")
                return self.start.coordinate
            else:
                #print("return destination")
                return self.destination.coordinate
        if self.start.coordinate.calculateDistance(coordinate) < self.destination.coordinate.calculateDistance(coordinate): 
            distanceVector = self.start.coordinate.getVectorDistance(self.destination.coordinate)  
            distanceVector = distanceVector.newCoordinateWithScale(e/c)
            return Coordinate(self.destination.coordinate.lat + distanceVector.lat, self.destination.coordinate.lon + distanceVector.lon)
        distanceVector = self.destination.coordinate.getVectorDistance(self.start.coordinate)  
        distanceVector = distanceVector.newCoordinateWithScale(e/c)
        return Coordinate(self.start.coordinate.lat + distanceVector.lat, self.start.coordinate.lon + distanceVector.lon)
        
    def addBuilding(self,building):
        """
        [Method] addBuilding
        Add a building to the building list
        
        Parameter:
            - building = [Building] a building inside this grid
        """
        self.buildings.append(building)
        
        
    def generateNodes(self):
        """
        [Method] generatesNodes
        Do not call this function, this function is to generate nodes that connects the buildings and roads
        """
        newNodes = []
        if (len(self.buildings) > 0):
            temp = []
            for x in self.buildings:
                #calculate entry point distance from start
                temp.append((x,self.start.coordinate.calculateDistance(x.entryPoint)))
            temp.sort(key=lambda x:x[1])
            nodes = []
            origin = self.start
            workingNode = None
            #print(temp)
            for x in temp:
                building = x[0]
                #generate entry node 
                if self.start.coordinate.calculateDistance(building.entryPoint) == 0:
                    workingNode = self.start
                elif self.destination.coordinate.calculateDistance(building.entryPoint) == 0:
                    workingNode = self.destination
                elif workingNode is None or workingNode.coordinate.calculateDistance(building.entryPoint) != 0:
                    workingNode  = Node()
                    workingNode.setAsBuildingConnector(building.entryPoint)
                    workingNode.osmId = f"{origin.osmId}-{building.buildingId}"
                    origin.addConnection(workingNode)
                    workingNode.addConnection(origin)
                #generate building Node
                buildingNode= Node()
                buildingNode.setAsBuildingConnector(building.coordinate)
                workingNode.addConnection(buildingNode)
                buildingNode.addConnection(workingNode)
                buildingNode.osmId = x[0].buildingId
                building.node = buildingNode
                building.entryPointNode = workingNode
                if workingNode not in newNodes:
                    newNodes.append(workingNode)
                newNodes.append(buildingNode)
                origin = workingNode
            workingNode.addConnection(self.destination)
            self.destination.addConnection(workingNode)
            self.start.removeConnection(self.destination)
            self.destination.removeConnection(self.start)
        #print(f"We have generated {len(newNodes)} number of new nodes")
        return newNodes
        
        
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
    