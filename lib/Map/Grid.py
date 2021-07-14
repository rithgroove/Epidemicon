import numpy as np
from .Coordinate import Coordinate

class Grid():  
    """
    [Class] Grid
    A class to represent the Grid
    
    Properties:
        - origin : The origin coordinate of this grid.
        - end : The end coordinate of this grid.
        - lonDistance : x distance (in longitude)
        - latDistance : y distance (in latitude)
        - nodes : list of nodes inside this grids
        - buildings : list of buildings inside this grids
        - roads : list of roads inside this grids
    """
    
    def __init__(self,origin,latDistance,lonDistance):
        """
        [Constructor]
        Initialize an new grid.
        
        Parameter:
            - origin : [Coordinate] origin coordinate
            - latDistance : [Double] distance in latitude
            - lonDistance : [Double] distance in longitude
        """
        self.origin = origin.newCoordinateWithTranslation(0, 0)
        self.end = origin.newCoordinateWithTranslation(latDistance, lonDistance)
        self.latDistance = latDistance
        self.lonDistance = lonDistance
        self.nodes = []
        self.buildings = []
        self.roads = []
    
    def addBuilding(self,building):
        """
        [Method] addBuilding
        Add a building to the building list
        
        Parameter:
            - building = [Building] a building inside this grid
        """
        self.buildings.append(building)
    
    def addNode(self, node):
        """
        [Method] addNodes
        Add a node to the nodes list
        
        Parameter:
            - node = [Node] a node inside this grid
        """
        self.nodes.append(node)
    
    def addRoad(self, road):
        """
        [Method] addRoads
        Add a road to the roads list
        
        Parameter:
            - road = [Road] a node inside this grid
        """
        self.roads.append(road)
    
    def remapBuilding(self, buildConnFileName = ""):
        """
        [Method] remapBuilding
        find closest nodes inside this grid 
       
        to do : maybe even create a new nodes
        """

        file = None
        connectionDict = {}

        if buildConnFileName != "":
            file = open(buildConnFileName, "r+")
            connectionDict = self.buildConnectionDict(file)
            
        for building in self.buildings:
            if building.way.osmId in connectionDict:
                self.loadEntryPoint(building, connectionDict[building.way.osmId])
            else:
                self.calculateEntryPoint(building, file)

    def buildConnectionDict(self, file):
        dict={}
        for line in file.readlines():
            if line[-1:] == "\n": # remove \n at the end of line if necessary
                line = line[:-1]
            try:
                wayID, min_dist, lat, lon = line.split(";")
                coord = Coordinate(float(lat), float(lon))
                dict[wayID] = {"min_dist": int(min_dist), "entryCoordinate": coord}
            except:
                continue
        return dict

    def loadEntryPoint(self, building, entryPoint):
        closest_coord = entryPoint["min_dist"]
        closest = self.roads[closest_coord]
        building.closestRoad = closest
        closest.addBuilding(building)
        building.entryPoint = entryPoint["entryCoordinate"]


    def calculateEntryPoint(self, building, file = None):
        road_min_dist = np.argmin([road.distanceToCoordinate(building.coordinate) for road in self.roads])
        closest = self.roads[road_min_dist]
        building.closestRoad = closest
        closest.addBuilding(building)
        building.entryPoint = closest.getClosestCoordinate(building.coordinate)
        if file != None:
            line = f"{building.way.osmId};{road_min_dist};{building.entryPoint.lat};{building.entryPoint.lon}\n"
            file.write(line)

    def __str__(self):
        """
        [Method] __str__        
        return a string that summarized the grid
        """
        temp = f"Grid\n"
        temp = temp + f"\tstarting = (lat = {self.origin.lat}, lon = {self.origin.lon})\n"
        temp = temp + f"\tend = (lat = {self.end.lat}, lon = {self.end.lon})\n"
        temp = temp + f"\tnodes = {self.nodes.__len__()}\n"
        temp = temp + f"\tbuildings = {self.buildings.__len__()}\n"
        temp = temp + f"\troads = {self.roads.__len__()}\n"
        return temp