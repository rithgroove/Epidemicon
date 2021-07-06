import xml.etree.ElementTree as ET
import os
import osmium
import numpy as np
import geopy.distance as distance
import csv
from .Node import  Node
from .Way import Way
from .Road import Road
from .Road import genName
from .Building import Building
from .Grid import Grid
from .Coordinate import Coordinate
from .PathFinder import searchPath
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
        self.buildingsDict = {}
        self.buildingsMap = {}
        
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
    
    def setBounds(self,filepath):
        """
        [Method] setBounds
        Re-read the filepath to setup the boundary
        
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
                
    def generateGrid(self):
        """
        [Method] generateGrid
        Generate the grids. This function needs to be called after setBounds()
        """
        temp = self.end.getVectorDistance(self.origin)
        #print(temp)
        self.distanceLat = (temp.lat)/self.gridSize[1]
        self.distanceLon = (temp.lon)/self.gridSize[0]
        print(f'{self.distanceLon},{self.distanceLat}')
        temp = Coordinate(self.origin.lat, self.origin.lon)
        for i in range(0,self.gridSize[0]):
            temp.lon = self.origin.lon
            for j in range(0,self.gridSize[1]):
                self.grids[j][i] = Grid(temp, self.distanceLat, self.distanceLon)  
                temp = temp.newCoordinateWithTranslation(lon = self.distanceLon)
            temp = temp.newCoordinateWithTranslation(lat = self.distanceLat)
            
    def mapNodesToGrid(self):
        """
        [Method] mapNodesToGrid
        Map the nodes to the grids. This function needs to be called after generateGrid()
        """
        for x in self.nodes:
            if(self.distanceLat is not None and self.distanceLon is not None):
                xAxis = int((x.coordinate.lon-self.origin.lon)/self.distanceLon)
                yAxis = int((x.coordinate.lat-self.origin.lat)/self.distanceLat)
                if xAxis >= self.gridSize[0]:
                    xAxis = self.gridSize[0]-1
                if yAxis >= self.gridSize[1]:
                    yAxis = self.gridSize[1]-1             
                if xAxis >= 0 and xAxis <self.gridSize[0] and yAxis >= 0 and yAxis <self.gridSize[1]:
                    grid =self.grids[xAxis][yAxis]
                    valid = True
                    if (x.coordinate.lat < grid.origin.lat or x.coordinate.lat > grid.end.lat):
                        valid = False
#                         print("fault in lat")
                    if (x.coordinate.lon < grid.origin.lon or x.coordinate.lon > grid.end.lon):
                        valid = False
#                         print("fault in lon")
                    if (valid):                 
                        grid.addNode(x)
                        x.grid = self.grids[xAxis][yAxis]
#                     else:
#                         print(f'######################################################')
#                         print("okay")
#                         print(f'{xAxis},{yAxis}')
#                         print(f'{self.distanceLon},{self.distanceLat}')
#                         print(self.origin)
#                         print(self.end)
#                         print(x)
#                         print(self.grids[xAxis][yAxis])
#                         print(f'######################################################')   
#                 else:
#                     print("dokay")
            
                
    def constructMap(self):
        """
        [Method] constructMap
        Method to construct the Map. This method will separate which nodes are roads and which nodes are building, naturals, etc
        
        """
        buildingId = 1
        for x in self.ways:
            if 'building' in x.tags.keys():
                temp = Building(f"b{buildingId}",x)
                buildingId += 1
                if(self.distanceLat is not None and self.distanceLon is not None):                   
                    if temp.coordinate.lat < self.origin.lat or temp.coordinate.lon < self.origin.lon or temp.coordinate.lat > self.end.lat or temp.coordinate.lon > self.end.lon: 
                        continue
                    xAxis = int((temp.coordinate.lon-self.origin.lon)/self.distanceLon)
                    yAxis = int((temp.coordinate.lat-self.origin.lat)/self.distanceLat)
                    #print(f'{xAxis},{yAxis}')               
                    if xAxis >= 0 and xAxis <self.gridSize[0] and yAxis >= 0 and yAxis <self.gridSize[1]:
                        self.buildings.append(temp)
                        if temp.type not in self.buildingsDict.keys():
                            self.buildingsDict[temp.type] =[]
                        self.buildingsDict[temp.type].append(temp)
                        self.buildingsMap[temp.buildingId] = temp
                        grid =self.grids[xAxis][yAxis]
                        x=temp
                        valid = True
                        if (x.coordinate.lat < grid.origin.lat or x.coordinate.lat > grid.end.lat):
                            valid = False
                        if (x.coordinate.lon < grid.origin.lon or x.coordinate.lon > grid.end.lon):
                            valid = False
                        if (valid):                 
                            grid.addBuilding(temp)
                            #x.grid = self.grids[xAxis][yAxis]
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
                    roadObject = Road(startingNode,node,road)
                    self.roadsDict[roadObject.name] = roadObject
                    self.roads.append(roadObject)  
                    if (roadObject.start.grid is not None):
                        roadObject.start.grid.addRoad(roadObject)
                    if (roadObject.destination.grid is not None):
                        roadObject.destination.grid.addRoad(roadObject)
                
            node.addWay(road)
            startingNode = node
            temp = self.roadNodesDict.get(f"{node.osmId}")
            if temp is None:
                self.roadNodesDict[node.osmId] = node
                self.roadNodes.append(node)
            
                
    def recalculateGrid(self):
        """
        [Method] recalculateGrid
        Method to recalculate building to the right grid and also map it to the road
        """
        for i in range(0,self.gridSize[1]):
            for j in range(0,self.gridSize[0]):
                self.grids[j][i].remapBuilding()
        for i in self.roads:
            generatedNodes = i.generateNodes()
            self.roadNodes.extend(generatedNodes)
            for newNodes in generatedNodes:
                self.roadNodesDict[newNodes.osmId] = newNodes
            
        
    def findPath(self,agent,building):
        """
        [Method] findPath
        A-star function to find the path from the agent location to the building 
        
        parameter:
            - agent : [Agent] agent (will be changed to node later to make sure the division between map and simulator)
            - building : [Building] the building 
        """
        try:
            distance = 0
            sequence = agent.currentNode.getMovementSequence(building.node)            
            if (sequence is None):
                #print("No previously calculated sequence is found")
                distance, sequence = searchPath(self,agent.currentNode,building.node)
                agent.currentNode.addMovementSequence(sequence.clone())           
            else:
                distance = sequence.totalDistance
            return distance, sequence
        except:
            return None, None
        
    def summarizeRoad(self):
        """
        [Method] summarizeRoad
        Print the summarized information of road types contained in this map
        """
        roadMap = {}
        for x in self.roads:
            if (x.type not in roadMap.keys()):
                roadMap[x.type] = 0
            roadMap[x.type] += 1
        print("Type of roads contained in this map")
        for x in roadMap.keys():
            print (f"{x} = {roadMap[x]}")
            
    def summarizeBuilding(self):
        """
        [Method] summarizeBuilding
        Print the summarized information of road types contained in this map
        """
        buildingMap = {}
        for x in self.buildings:
            if (x.type not in buildingMap.keys()):
                buildingMap[x.type] = 0
            buildingMap[x.type] += 1
        print("Type of buildings contained in this map")
        for x in buildingMap.keys():
            print (f"{x} = {buildingMap[x]}")
    
    def generateRandomBuildingType(self,buildingCSV):
        # load the CSV and put the result into the grids
        with open(buildingCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            keys = []
            for row in csv_reader:
                data = {}
                if len(keys) == 0:
                    keys = row
                elif len(row) != 0:         
                    print(row)
                    for i in range(0,len(keys)):
                        data[keys[i]]=row[i]
                    self.grids[int(data["x"])][int(data["y"])].addBuildingSettings(data)
                    
        # have the grids retags the buildings
        for i in range(0,self.gridSize[1]):
            for j in range(0,self.gridSize[0]):
                self.grids[j][i].retagBuildings()
                
        self.buildingsDict = {}
        for building in self.buildings:
            if (building.type not in self.buildingsDict.keys()):
                self.buildingsDict[building.type] = []
            self.buildingsDict[building.type].append(building)
                    
def readFile(filepath,grid = (10,10),buildingCSV = None):
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
    generatedMap.generateGrid()
    generatedMap.mapNodesToGrid()
    generatedMap.constructMap()
    generatedMap.recalculateGrid()
    if buildingCSV is not None:
        generatedMap.generateRandomBuildingType(buildingCSV)
    return generatedMap