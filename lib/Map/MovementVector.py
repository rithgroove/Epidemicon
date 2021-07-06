import geopy.distance as gdistance
class MovementVector:
    """
    [Class] MovementVector
    A class to represent the a star node
    
    Properties:
        - startingNode          : [Node] the starting node of this movementVector
        - destinationNode       : [Node] the destination node of this movementVector
        - starting              : [Coordinate] the starting coordinate of this movementVector
        - destination           : [Coordinate] the destination coordinate of this movementVector
        - distance              : [Float] distance in meters
        - passedThroughDistance : [Float] distance we traveled in this movementVector
        - totalTranslation      : [(Float,Float)] current translation in latitude longitude from the starting node
        - currentPosition       : [Coordinate] current position
        - finished              : [Bool] is the whole vector traveled?
        - progress              : [Float] passedThroughDistance divided by totalTranslation
    """
    def __init__(self,startingNode, destinationNode ):
        """
        [Constructor]    
        Generate Unused MovementVector.
        
        Parameter:
            - startingNode    : [Node] the starting node of this movementVector
            - destinationNode : [Node] the destination node of this movementVector
        """
        self.startingNode = startingNode
        self.destinationNode = destinationNode
        self.starting = startingNode.coordinate.getLatLon()
        self.destination = destinationNode.coordinate.getLatLon()
        self.distance = gdistance.distance(self.starting,self.destination).km*1000
        if(self.distance == 0):
            print(startingNode)
            print(destinationNode)
        self.passedThroughDistance = 0
        self.totalTranslation = (self.destination[0]-self.starting[0],self.destination[1]-self.starting[1])
        self.currentPosition = self.starting
        self.finished = False
        self.progress = 0.0
        
    def calculateTranslation(self, currentPosition):
        """
        [Method] calculateTranslation    
        Calculate the translation required from a coordinate to the calculated position in this movement vector. 
        
        Parameter:
            - currentPosition : [Coordinate]current position
            
        return :
            - (lat,lon) the translation vector in latitude and longitude
            
        """
        return (self.currentPosition[0] - currentPosition.lat, self.currentPosition[1] - currentPosition.lon)
        
    def step(self,distances):
        """
        [Method] step    
        Travel a certain number of distances in this vector, if the distance is higher than our remaining distance in this vector, the leftover will be returned.
        
        Parameter:
            - distances : [Float] distance traveled in meters
            
        return :
            - [float] the leftover of the distance            
        """
        # calculate is there any left over translation
        leftOver = distances - (self.distance - self.passedThroughDistance)
        # if leftover somehow less than 0 se to 0
        if leftOver < 0:
            leftOver = 0
        #after 
        self.passedThroughDistance += distances
        if self.passedThroughDistance >= self.distance:
            self.passedThroughDistance = self.distance     
            self.finished = True
        self.progress = float(self.passedThroughDistance)/float(self.distance)
        if (self.progress >= 1):
            self.progress = 1
            self.currentPosition =  self.destination
        else:
            #print("progressing")
            lat = self.starting[0] +(self.progress * self.totalTranslation[0])
            lon = self.starting[1] +(self.progress * self.totalTranslation[1])
            self.currentPosition = (lat, lon)
        return leftOver
    
    def extract(self):
        return (self.startingNode.osmId, self.destinationNode.osmId)
    
    def clone(self):
        """
        [Method] clone    
        Generate a fresh clone of this object
                    
        return :
            - [MovementVector] copy of this movement vector       
        """
        return MovementVector(self.startingNode,self.destinationNode)
            