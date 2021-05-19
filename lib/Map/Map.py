import xml.etree.ElementTree as ET
import os
import osmium
import numpy as np
import geopy.distance as distance
from .Node import  Node
from .Way import Way
from .Road import Road
from .Road import genName
from .Building import Building
from .Grid import Grid
from .Coordinate import Coordinate

class Map(osmium.SimpleHandler):
    """
    [Class] Map
    A class to represent the map
    
    Properties:
        - origin        : [Coordinate] map's origin coordinate
        - end           : [Coordinate] map's end coordinate
        - num_nodes     : Number of Nodes.
        - nodesDict     : Dictionary of all nodes. The key used are the Open Street Map ID.
        - nodes         : List of all nodes.
        
        - num_ways      : Number of Ways.
        - waysDict      : Dictionary of all nodes. The key used are the Open Street Map ID.
        - ways          : List of all ways.
        
        - num_roads     : Number of Roads.
        - roadNodesDict : 
        - roadNodes     : 
        - roadsDict     : List of all nodes that marked as road.
        - roads         : List of all roads.
        
        - num_buildings : Number of Buildings.
        - buildings     : List of all buildings.
        - naturals      : List of all naturals.
        - leisures      : List of all leisures.
        - amenities     : List of all amenities.
        
        - grids         : [(int,int)] Two dimensional array of grids
        
        - others        : List of other openstreetmap ways that yet to be categorized.
        - distanceLat   : height of 1 grid in latitude
        - distanceLon   : width of 1 grid in longitude
        - gridsize      : tuple of 2 integer that shows how many grids we have
    """
    def __init__(self,grid = (10,10)):
        """
        [Constructor]    
        Generate Empty Map.
        
        Parameter:
            - grid = grid size, default value = (10,10)
        """
        osmium.SimpleHandler.__init__(self)
        self.origin = Coordinate(0.0,0.0)
        self.end = Coordinate(0.0,0.0)
        
        self.num_nodes = 0
        self.nodesDict = {}
        self.nodes = []
        
        self.num_ways = 0
        self.waysDict = {}
        self.ways = []
        
        self.num_roads = 0
        self.roadNodesDict = {}
        self.roadNodes = []             
        self.roadsDict = {}
        self.roads = []             
        self.num_buildings = 0
        self.buildings = []
        
        self.naturals = []
        self.leisures = []
        self.amenities = []
        
        self.grids = [[0 for x in range(grid[1])] for y in range(grid[0])]
        self.others = []
        self.distanceLat = None
        self.distanceLon = None
        self.gridSize = grid
        
    def node(self, n):
        """
        [Method] node
        Do not use this method, this is an override method from osmium to generate nodes.
        """
        self.num_nodes += 1
        temp =  Node()
        temp.fill(n)
        self.nodesDict[f"n{n.id}"] = temp
        self.nodes.append(temp)
        
    def way(self, n):
        """
        [Method] way
        Do not use this method, this is an override method from osmium to generate ways.
        """
        self.num_ways += 1
        temp =  Way()
        temp.fill(n,self.nodesDict)
        self.waysDict[f"n{n.id}"] = temp
        self.ways.append(temp)
        
    def __str__(self):
        """
        [Method] __str__
        Generate the Map Statistic string and return it.
        
        Return: [string] String of summarized map Information.
        """
        tempstring = f"Epidemicon Map\n"
        tempstring = tempstring + f" number of nodes = {self.num_nodes}\n"
        tempstring = tempstring + f" number of ways = {self.num_ways}\n"
        tempstring = tempstring + f" number of roads = {self.roads.__len__()}\n"
        tempstring = tempstring + f" number of roads node = {self.roadNodes.__len__()}\n" 
        tempstring = tempstring + f" number of buildings = {self.buildings.__len__()}\n" 
        return tempstring
    
    def setBounds(self,filepath,grid=(10,10)):
        """
        [Method] __str__
        Setup the bounds using the file path
        
        Parameter:
            - filepath : path to the OSM file
        """
        tree = ET.parse(filepath)
        root = tree.getroot()
        for child in root:
            if (child.tag == 'bounds'):
                self.origin = Coordinate(float(child.attrib['minlat']),float(child.attrib['minlon']))
                self.end = Coordinate(float(child.attrib['maxlat']),float(child.attrib['maxlon']))
                break
        temp = self.end.getVectorDistance(self.origin)
        self.distanceLat = (temp.lat)/grid[1]
        self.distanceLon = (temp.lon)/grid[0]
        temp = Coordinate(self.origin.lat, self.origin.lon)
        for i in range(0,grid[0]):
            temp.lat = self.origin.lat
            for j in range(0,grid[1]):
                self.grids[j][i] = Grid(temp, self.distanceLat, self.distanceLon)  
                temp.translate(lon = self.distanceLon)
            temp.translate(lat = self.distanceLat)
                
    def constructMap(self):
        """
        [Method] constructMap
        Method to construct the Map. This method will separate which nodes are roads and which 
        
        """
        for x in self.ways:
            if 'building' in x.tags.keys():
                temp = Building(x)
                self.buildings.append(temp)
                if(self.distanceLat is not None and self.distanceLon is not None):
                    xAxis = int((temp.coordinate.lon-self.origin.lon)/self.distanceLon)
                    yAxis = int((temp.coordinate.lat-self.origin.lat)/self.distanceLat)
                    if xAxis >= self.gridSize[0]:
                        xAxis = self.gridSize[0]-1
                    if yAxis >= self.gridSize[1]:
                        yAxis = self.gridSize[1]-1
                    #print(f'{xAxis},{yAxis}')
                    self.grids[xAxis][yAxis].addBuilding(temp)
            elif 'natural' in x.tags.keys():
                self.naturals.append(x)
            elif 'leisure' in x.tags.keys():
                self.leisures.append(x)
            elif 'amenity' in x.tags.keys():
                self.amenities.append(x)
            elif 'highway' in x.tags.keys():
                self.processRoad(x)
            else :
                self.others.append(x)
                
    def processRoad(self,road):
        """
        [Method] processRoad
        Method to link the node based on the open street map ways
        
        Parameter:
            - road: Open Street Map Road.
        """
        startingNode = None
        for node in road.nodes:
            if (startingNode is not None):
                startingNode.addConnection(node)
                node.addConnection(startingNode)           
                roadObject = self.roadsDict.get(genName(startingNode,node)[0])
                if roadObject is None:
                    roadObject = Road(startingNode,node)
                    self.roadsDict[roadObject.name] = roadObject
                    self.roads.append(roadObject)                                    
                
            node.addWay(road)
            startingNode = node
            temp = self.roadNodesDict.get(f"{node.osmId}")
            if temp is None:
                self.roadNodesDict[node.osmId] = node
                self.roadNodes.append(node)
                
    def recalculateGrid(self):
        """
        [Method] recalculateGrid
        Method to recalculate building to the right grid
        """
        for i in range(0,self.gridSize[0]):
            for j in range(0,self.gridSize[1]):
                self.grids[j][i].remapBuilding()
        
    
def readFile(filepath,grid = (10,10)):
    """
    [Function] readFile
    Function to generate map fom osm File
    
    parameter:
        - filepath : [string] path to the OSM file
        - grid     : [(int,int)] grid size, default value = (10,10)
    """
    generatedMap = Map(grid)
    generatedMap.apply_file(filepath)
    generatedMap.setBounds(filepath)
    generatedMap.constructMap()
    return generatedMap