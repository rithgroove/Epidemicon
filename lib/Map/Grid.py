import geopy.distance as distance
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
        self.origin = origin
        self.end = origin.newCoordinateWithTranlation(latDistance, lonDistance)
        self.latDistance = latDistance
        self.lonDistance = lonDistance
        self.nodes = []
        self.buildings = []
    
    def addBuilding(self,building):
        """
        [Method] addBuilding
        Add a building to the building list
        
        Parameter:
            - building = [Building] a building inside this grid
        """
        self.buildings.append(building)
    
    def remapBuilding(self):
        """
        [Method] remapBuilding
        find closest nodes inside this grid 
       
        to do : maybe even create a new nodes
        """
        for building in self.buildings:
            closest = None
            closestDistance = 1000000000000000
            for cell in self.cells:
                temp = distance.distance(building.getPosition(), cell.getPosition())
                if closestDistance > temp :
                    closestDistance = temp
                    closest = cell
            building.closestCell = closest
