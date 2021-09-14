from lib.Map.MovementSequence import MovementSequence, reconstructByHashId
import xml.etree.ElementTree as ET
import osmium
import numpy as np
import geopy.distance as distance
from pathlib import Path
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
        - gridCellHeight   : height of 1 grid in latitude
        - gridCellWidth   : width of 1 grid in longitude
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
        self.gridCellHeight = None
        self.gridCellWidth = None
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
        boundDistance = self.end.getVectorDistance(self.origin)
        self.gridCellHeight = (boundDistance.lat) / self.gridSize[1]
        self.gridCellWidth = (boundDistance.lon) / self.gridSize[0]
        coord = Coordinate(self.origin.lat, self.origin.lon)
        for i in range(0,self.gridSize[0]):
            coord.lon = self.origin.lon
            for j in range(0,self.gridSize[1]):
                self.grids[j][i] = Grid(coord, self.gridCellHeight, self.gridCellWidth)  
                coord = coord.newCoordinateWithTranslation(lon = self.gridCellWidth)
            coord = coord.newCoordinateWithTranslation(lat = self.gridCellHeight)
            
    def mapNodesToGrid(self):
        """
        [Method] mapNodesToGrid
        Map the nodes to the grids. This function needs to be called after generateGrid()
        """
        if(self.gridCellHeight is not None and self.gridCellWidth is not None):
            for node in self.nodes:
                xAxis = int((node.coordinate.lon - self.origin.lon) / self.gridCellWidth)
                yAxis = int((node.coordinate.lat - self.origin.lat) / self.gridCellHeight)
                if xAxis >= self.gridSize[0]:
                    xAxis = self.gridSize[0]-1
                if yAxis >= self.gridSize[1]:
                    yAxis = self.gridSize[1]-1             
                if xAxis >= 0 and xAxis < self.gridSize[0] and yAxis >= 0 and yAxis < self.gridSize[1]:
                    grid =self.grids[xAxis][yAxis]             
                    grid.addNode(node)
                    node.grid = self.grids[xAxis][yAxis]          

                
    def constructMap(self):
        """
        [Method] constructMap
        Method to construct the Map. This method will separate which nodes are roads and which nodes are building, naturals, etc
        
        """
        for x in self.ways:
            if 'building' in x.tags.keys():
                build = Building(x)
                if(self.gridCellHeight is not None and self.gridCellWidth is not None):
                    if build.coordinate.lat < self.origin.lat or build.coordinate.lon < self.origin.lon or build.coordinate.lat > self.end.lat or build.coordinate.lon > self.end.lon: 
                        continue
                    self.addBuilding(build)

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

    def addBuilding(self, building):
        """
        [Method] addBuilding
        Add a building to this map
        
        Parameter:
            - building: [Building] The building
        """
        xAxis = int((building.coordinate.lon-self.origin.lon) / self.gridCellWidth)
        yAxis = int((building.coordinate.lat-self.origin.lat) / self.gridCellHeight)
        self.buildings.append(building)
        if building.type not in self.buildingsDict.keys():
            self.buildingsDict[building.type] =[]
        self.buildingsDict[building.type].append(building)
        self.buildingsMap[building.buildingId] = building
        grid = self.grids[xAxis][yAxis]               
        grid.addBuilding(building)

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
            
                
    def recalculateGrid(self, buildConnFileName):
        """
        [Method] recalculateGrid
        Method to recalculate building to the right grid and also map it to the road

        Parameter:
            - buildConnFileName = [str] the name of the file used to cache the connections between the roads and buildings
        """
        file = None
        connectionDict = {}
        if buildConnFileName != "":
            Path(buildConnFileName).touch()
            file = open(buildConnFileName, "r+")
            connectionDict = self.buildConnectionDict(file)
        
        for i in range(0,self.gridSize[1]):
            for j in range(0,self.gridSize[0]):
                self.grids[j][i].remapBuilding(file, connectionDict)
            
        for i in self.roads:
            generatedNodes = i.generateNodes()
            self.roadNodes.extend(generatedNodes)
            for newNodes in generatedNodes:
                self.roadNodesDict[newNodes.osmId] = newNodes
            self.roadNodes.extend(generatedNodes)

        if file != None:
            file.close()

    def buildConnectionDict(self, file):
        """
        [Method] buildConnectionDict
        Method that creates an dictionary in the format: [Dict[wayID: str, ("min_dist": int, "entryCoordinate": Coordinate)]]
        that maps the wayIDof the building to an entry coordinate and a minimum distance

        Parameter:
            - file = [FileIO] a file to cache the connections between the roads and buildings 

        Return: [Dict[wayID: str, ("min_dist": int, "entryCoordinate": Coordinate)]]
        """

        wayIdDict={}
        for line in file.readlines():
            if line[-1:] == "\n": # remove \n at the end of line if necessary
                line = line[:-1]
            try:
                wayID, min_dist, lat, lon = line.split(";")
                coord = Coordinate(float(lat), float(lon))
                wayIdDict[wayID] = {"min_dist": int(min_dist), "entryCoordinate": coord}
            except ValueError:
                # This exception occurs if the split does not return the correct number of arguments
                # This means that or the csv is invalid or the line is wrong, in any case the process continues
                continue
        return wayIdDict
        
    def findPath(self, agent, building, pathfindDict=None, nodeHashIdDict=None):
        """
        [Method] findPath
        A-star function to find the path from the agent location to the building 
        
        parameter:
            - agent : [Agent] agent (will be changed to node later to make sure the division between map and simulator)
            - building : [Building] the building 
            - pathfindDict = [dict] dictionary to check for already calculated paths
        """
        startNode = agent.currentNode
        finishNode = building.node
        # Checking if the path has aready been calculated in the pathfindDict
        if pathfindDict is not None and startNode.hashId in pathfindDict and finishNode.hashId in pathfindDict[startNode.hashId]:
            sequence = pathfindDict[startNode.hashId][finishNode.hashId]
            if type(sequence) != MovementSequence: # This means the sequence is in the format (sequenceIds: List[Tuple(nodeId, nodeId)], distance:float)
                sequence = reconstructByHashId(nodeHashIdDict, sequence[0], sequence[1])
                pathfindDict[startNode.hashId][finishNode.hashId] = sequence
            distance = sequence.totalDistance
        else:
            distance = 0
            sequence = startNode.getMovementSequence(finishNode)     
            if sequence is None:
                distance, sequence = searchPath(self,startNode,finishNode)
                if sequence is not None:
                    startNode.addMovementSequence(sequence.clone())
            else:
                distance = sequence.totalDistance
        
        return distance, sequence
        
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
        """
        [Method] generateRandomBuildingType
        Retags buildings that does not have tags based on the CSV config.
        
        Parameter:
            - buildingCSV = [String] path to the csv file
        """
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
                    #print(row)
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
            
    def getRandomBuilding(self,buildingType,rng):
        """
        [Method] getRandomBuilding
        Get a random building based on the type
        
        Parameter:
            - buildingType = [String] building type that we want (For example: restaurant)
            
        Return:
            [Building] the building
        """
        return rng.choice(self.buildingsDict[buildingType])
                    
def readFile(OSMfilePath, buildConnFile="",grid = (10,10),buildingCSV = None):
    """
    [Function] readFile
    Function to generate map fom osm File
    
    parameter:
        - OSMfilePath : [string] path to the OSM file
        - grid     : [(int,int)] grid size, default value = (10,10)
    """
    generatedMap = Map(grid)
    generatedMap.apply_file(OSMfilePath)
    generatedMap.setBounds(OSMfilePath)
    generatedMap.generateGrid()
    generatedMap.mapNodesToGrid()
    generatedMap.constructMap()
    generatedMap.recalculateGrid(buildConnFile)
    if buildingCSV is not None:
        generatedMap.generateRandomBuildingType(buildingCSV)
    return generatedMap
