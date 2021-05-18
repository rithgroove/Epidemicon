import geopy.distance as distance

class Coordinate():  
    
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - lat : latitude.
        - lon : longitude.
    """
    
    def __init__(self,lat,lon):
        """
        [Constructor]
        Initialize an empty node.

        Parameter:
            - lat : latitude.
            - lon : longitude.
        """
        self.lat = lat
        self.lon = lon

    def getLatLon(self):
        """
        [Method] getLatLon
        return a tuple of lat and lon in that order. (usefull for printing strings)
        
        Return:[(float,float)](lat,lon)
        """
        return (self.lat,self.lon)
    
    def getLonLat(self):
        """
        [Method] getLatLon
        return a tuple of lat and lon in that order. (usefull for printing strings)
        
        Return:[(float,float)](lon,lat)
        """
        return (self.lon,self.lat)
    
    
    def __str__(self):
        """
        [Method] __str__
        Generate the Map Statistic string and return it.
        
        Return: [string] String of summarized map Information.
        """
        tempstring = f"Coordinate (lat = {self.lat}, lon = {self.lon}"
        return tempstring