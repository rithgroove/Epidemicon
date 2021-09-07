import numpy as np
from .Coordinate import Coordinate
import numpy as np

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
        self.buildingSettings = []
        self.defaultBuildings = None
    
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
    
    def remapBuilding(self, buildConnFile = None, connectionDict = {}):
        """
        [Method] remapBuilding
        Method to give each building their entry points.
       
        Parameter:
            - buildConnFile = [FileIO] a file to cache the connections between the roads and buildings 
            - connectionDict = [Dict] a dictionary of the building entry points
                | Key = [wayID] str, 
                    | min_dist: [int] the distance from the building's centroid to the closest point on the road 
                    | entryCoordinate: [Coordinate] coordinate on the road that act as the connecting point
        """

        for building in self.buildings:
            if building.way.osmId in connectionDict:
                #if building have precalculated entry point, load the precalculated entry point.
                self.loadEntryPoint(building, connectionDict[building.way.osmId])
            else:
                #if not, recalculate the entry point of this building.
                self.calculateEntryPoint(building, buildConnFile)

    def loadEntryPoint(self, building, entryPoint):
        """
        [Method] loadEntryPoint
        Load the entry point of this building from the file
       
        Parameter:
            - building = [Building] The building
            - connectionDict = [Dict] a dictionary of the building entry points
                | Key = [wayID] str, 
                    | min_dist: [int] the distance from the building's centroid to the closest point on the road 
                    | entryCoordinate: [Coordinate] coordinate on the road that act as the connecting point
        to do : Move it to building class?
        """
        closest_coord = entryPoint["min_dist"]
        closest = self.roads[closest_coord]
        building.closestRoad = closest
        closest.addBuilding(building)
        building.entryPoint = entryPoint["entryCoordinate"]


    def calculateEntryPoint(self, building, file = None):
        """
        [Method] calculateEntryPoint
        calculate the building's entry point from the road
       
        Parameter:
            - building = [Building] The building
            - file = [FileIO] a file to write the connections between the roads and buildings 
        to do : Move it to building class?
        """
        road_min_dist = np.argmin([road.distanceToCoordinate(building.coordinate) for road in self.roads])
        closest = self.roads[road_min_dist]
        building.closestRoad = closest
        closest.addBuilding(building)
        building.entryPoint = closest.getClosestCoordinate(building.coordinate)
        
        if file != None:
            # write the calculated point to the file
            line = f"{building.way.osmId};{road_min_dist};{building.entryPoint.lat};{building.entryPoint.lon}\n"
            file.write(line)

    def addBuildingSettings(self,setting):
        """
        [Method] addBuildingSettings
        Add configuration for retagging this buildings
        
        Parameter:
            - setting = [Dict] the dictionary that defines the type of buildings in this Grid. 
                | type = the building type
                | number = the number of building of said type in this grid                
        """
        
                
        if (setting["number"] == "All"):
            self.defaultBuildings = setting
        else:
            setting["number"] = int(setting["number"])
            self.buildingSettings.append(setting)
        
    def retagBuildings(self):
        """
        [Method] retagBuildings
        Give the building without clear tags (for example building with tag "yes" or "+") a building type based on the settings
        
        See: [Method] Grid.addBuildingSettings
        
        """
        #collect all buildings that have the type "yes" and "+"
        nonTaggedBuildings = []        
        for building in self.buildings:
            if building.type == "yes" or building.type == "+":
                nonTaggedBuildings.append(building)
                
        #mark the building according to the csv (the one that we have the numbers)
        for setting in self.buildingSettings:
            for i in range(0,setting["number"]):
                if (len(nonTaggedBuildings) <= 0):
                    break #break if the config have more buildings than the actual buildings count
                building = nonTaggedBuildings.pop(0) #maybe randomize later?
                building.setType(setting["type"])
            if (len(nonTaggedBuildings) <= 0):
                break #break if the config have more buildings than the actual buildings count
                
        #mark the rest of the buildings as the default buildings (the one that marked as "All" in the CSV)
        if self.defaultBuildings is not None:
            for building in nonTaggedBuildings:
                building.setType(self.defaultBuildings["type"])

    def __str__(self):
        """
        [Method] __str__        
        return a string that summarized the grid
        """
        temp = f"[Grid]\n"
        temp = temp + f"\tstarting = (lat = {self.origin.lat}, lon = {self.origin.lon})\n"
        temp = temp + f"\tend = (lat = {self.end.lat}, lon = {self.end.lon})\n"
        temp = temp + f"\tnodes = {self.nodes.__len__()}\n"
        temp = temp + f"\tbuildings = {self.buildings.__len__()}\n"
        temp = temp + f"\troads = {self.roads.__len__()}\n"
        return temp