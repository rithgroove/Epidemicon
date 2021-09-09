import geopy.distance as distance

class Coordinate():  
    
    """
    [Class] Coordinate
    A class to represent a coordinate. Also used as a vector representation.
    
    Properties:
        - lat : latitude.
        - lon : longitude.
    """
    
    def __init__(self,lat,lon):
        """
        [Constructor]
        Initialize an empty node.

        Parameter:
            - lat : [Double]latitude.
            - lon : [Double]longitude.
        """
        self.lat = lat
        self.lon = lon

    def getLatLon(self):
        """
        [Method] getLatLon
        return a tuple of lat and lon in that order. (usefull for printing strings)
        
        Return:[(Double,Double)](lat,lon)
        """
        return (self.lat,self.lon)
    
    def getLonLat(self):
        """
        [Method] getLatLon
        return a tuple of lat and lon in that order. (usefull for printing strings)
        
        Return:[(Double,Double)](lon,lat)
        """
        return (self.lon,self.lat)

    def translate(self,lat =0,lon = 0):
        """
        [Method] translate
        translate/move this coordinate

        Parameter:
            - lat : [Double] latitude translation.
            - lon : [Double] longitude translation.
        """
        self.lat += lat
        self.lon += lon
    
    def __str__(self):
        """
        [Method] __str__
        Generate the Map Statistic string and return it.
        
        Return: [string] String of summarized map Information.
        """
        tempstring = f"[Coordinate]\n (lat = {self.lat}, lon = {self.lon})"
        return tempstring
    
    def newCoordinateWithTranslation(self,lat =0,lon = 0):
        """
        [Method] newCoordinateWithTranlation
        create a new coordinate and apply a translation from this coordinate

        Parameter:
            - lat : [Double] latitude translation.
            - lon : [Double] longitude translation.
            
        return :
            - [Coordinate] a clone of this coordinate with the translation applied.
        """
        temp = Coordinate(self.lat+lat,self.lon+lon)
        return temp
    
    def newCoordinateWithScale(self,scale):
        """
        [Method] newCoordinateWithScale
        create a new coordinate which is the scale of this vector

        Parameter:
            - scale : [Double] scaling factor.
            
        return :
            - [Coordinate] a clone of this coordinate with the scaling applied.

        """
        temp = Coordinate(self.lat*scale,self.lon*scale)
        return temp
       
    def calculateDistance(self,targetCoordinate):
        """
        [Method] calculateDistance
        calculateDistance to other coordinate
        
        Parameter:
            - targetCoordinate : [Coordinate] target Coordinate.
            
        Return: [Double] Distance in Meter
        """
        return distance.distance(self.getLatLon(), targetCoordinate.getLatLon()).km * 1000
    
    def getVectorDistance(self,targetCoordinate):
        """
        [Method] getVectorDistance
        Get distance in vector format. (Will be returned in coordinate object for ease of use)
        
        Parameter:
            - targetCoordinate : [Coordinate] target Coordinate.
        
        Return: [Coordinate] distance in vector format
        """
        return Coordinate(self.lat - targetCoordinate.lat, self.lon - targetCoordinate.lon)
    
