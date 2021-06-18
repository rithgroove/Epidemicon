
class Virus:
    """
    [Class] Virus
    
    
    Properties:
        - host : [] the building the house is in
        - currentLocation : [Coordinate] the agents that live inside this home
        - status : Dormant, active, etc
        - exposed : [Bool] yes if the the virus is currently outside of the host body (used to make the building/ road infectious)
    """
    def __init__(self,osmMap):