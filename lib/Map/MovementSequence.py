class MovementSequence:
    
    def __init__(self,sequence,totalDistance):
        self.sequence = sequence
        self.origin = sequence[0].startingNode
        self.destination = sequence[-1].destinationNode
        self.currentActiveVector = None
        self.totalDistance = totalDistance
        self.currentTraversedDistance = 0
        self.finished = False
        self.currentNode = sequence[0].startingNode
        self.lastNode = sequence[0].startingNode
        #print(self.sequence.__len__())
        
    def step(self,distances):
        # pop from array of current active se
        if (self.currentActiveVector is None or self.currentActiveVector.finished) and self.sequence.__len__()>0:
            #print(self.sequence.__len__())
            self.currentActiveVector = self.sequence.pop(0)     
        leftOver = 0
        translation = (0.0,0.0)
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
        return self.currentActiveVector.calculateTranslation(currentPosition)
    
    def clone(self):
        temp = []
        for x in self.sequence:
            temp.append(x.clone())
        return MovementSequence(temp,self.totalDistance)
        