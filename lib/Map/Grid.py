import geopy.distance as distance

class Grid():  
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - minlat : minimum latitude.
        - minlon : minimum longitude.
        - maxlat : maximum latitute.
        - maxlon : maximum longitude.
        - nodes : 
    """
    
    def __init__(self,minlat,minlon,latDistance,lonDistance):
        """
        [Constructor]
        Initialize an new grid.
        """
        self.minlat = minlat
        self.minlon = minlon
        self.maxlat = minlat+latDistance
        self.maxlon = minlon+lonDistance
        self.latDistance = latDistance
        self.lonDistance = lonDistance
        self.nodes = []
        self.cells = []
        self.buildings = []
        
    def addCell(self,cell):
        self.cells.append(cell)
    
    def addBuilding(self,building):
        self.buildings.append(building)
    
    def remapBuilding(self):
        for building in self.buildings:
            closest = None
            closestDistance = 1000000000000000
            for cell in self.cells:
                temp = distance.distance(building.getPosition(), cell.getPosition())
                if closestDistance > temp :
                    closestDistance = temp
                    closest = cell
            building.closestCell = closest
