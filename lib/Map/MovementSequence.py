from .MovementVector import MovementVector
class MovementSequence:
    """
    [Class] MovementSequence
    A class to represent the movement sequence required to go from one node to another node.
    
    Properties:
        - sequence                 : [MovementVector] array of MovementVectors
        - origin                   : [Node] the starting node of this MovementSequence
        - destination              : [Node] the destination node of this MovementSequence
        - currentActiveVector      : [MovementVector] current active movement vector
        - totalDistance            : [Float] total distance in meters
        - passedThroughDistance    : [Float] distance we traveled in this movementVector
        - currentTraversedDistance : [Float] how far we traversed in this sequence
        - finished                 : [Bool] is the whole sequence traveled?
        - currentNode              : [Node] currentNode traversed
        - lastNode                 : [Node] last node traversed
    """
    
    def __init__(self,sequence,totalDistance):
        """
        [Constructor]    
        Generate Unused MovementSequence.
        
        Parameter:
            - sequence      : [MovementVector] array of MovementVectors
            - totalDistance : [Float] total distance in meters
        """
        self.sequence = sequence
        self.origin = sequence[0].startingNode
        self.destination = sequence[-1].destinationNode
        self.currentActiveVector = None
        self.totalDistance = totalDistance
        self.currentTraversedDistance = 0
        self.finished = False
        self.currentNode = sequence[0].startingNode
        self.lastNode = sequence[0].startingNode
        self.new = True
        
    def step(self,distances):
        """
        [Method] step    
        Travel a certain number of distances in this sequence's currentActiveVector. Leftover distances are returned
        
        Parameter:
            - distances : [Float] distance traveled in meters
            
        return :
            - [float] the leftover of the distance            
        """
        self.new = False
        # pop from array of sequence to the current active vector
        if (self.currentActiveVector is None or self.currentActiveVector.finished) and self.sequence.__len__()>0:
            self.currentActiveVector = self.sequence.pop(0)     
        leftOver = 0
        #if current active vector is finished (which means we're at the last vector) mark this sequence as finished
        if (self.currentActiveVector.finished):
            leftOver = distances
            self.finished = True
        else:
            leftOver = self.currentActiveVector.step(distances)            
            self.currentTraversedDistance += (distances-leftOver)                        
            if self.currentActiveVector.finished:
                self.lastNode = self.currentNode
                self.currentNode = self.currentActiveVector.destinationNode
        return leftOver
        
    def getVector(self,currentPosition):
        """
        [Method] getVector    
        Calculate the translation required from a coordinate to the calculated position in the current actives movement vector. 
        (Might need to change the name later)
        
        Parameter:
            - currentPosition : [Coordinate]current position
            
        return :
            - (lat,lon) the translation vector in latitude and longitude
            
        """
        return self.currentActiveVector.calculateTranslation(currentPosition)
    
    def getCurrentPosition(self):
        """
        [Method] getCurrentPosition  
        return the current position of the agent
            
        return :
            - [Coordinate] current location based on currentActiveVector.
            
        """
        return self.currentActiveVector.currentPosition
    
    def extract(self):
        seq = []
        for vector in self.sequence:
            seq.append(vector.extract())
        return (seq,self.totalDistance)
            
            
    def clone(self):
        """
        [Method] clone    
        Generate a fresh clone of this object
                    
        return :
            - [MovementSequence] unused copy of this movement vector       
        """
        temp = []
        for x in self.sequence:
            temp.append(x.clone())
        return MovementSequence(temp,self.totalDistance)

def reconstruct(nodesDictionary, sequences, totalDistance):
    sequence = []
    for x in sequences:
        sequence.append(MovementVector(nodesDictionary[x[0]],nodesDictionary[x[1]]))
    return MovementSequence(sequence,totalDistance)