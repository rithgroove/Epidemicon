import geopy.distance as distance
from .MovementVector import MovementVector
from .MovementSequence import MovementSequence

class AStarNode():
    """
    [Class] AStarNode
    A class to represent the a star node
    
    Properties:
        - g             : [float] the exact cost of the path from the starting node to this node
        - h             : [float] the heuristic estimated cost from this node to the target node.
        - f             : [float] lowest cost in the neighbor of this node
        - position      : [Coordinate] the coordinate of this node
        - name          : name of this node
        - node          : [Node] the node object this object refers to
        - visited       : [Bool] is this node visited before?
        - prevNode      : [AStarNode] the previous node
    """
    def __init__(self,node,targetNode):
        """
        [Constructor]    
        Generate Unvisited AStarNode.
        
        Parameter:
            - node       : [Node] the OSM node this class represent
            - targetNode : [Node] the OSM node which is this class targeted goal
        """
        self.g = 0
        self.h = 0
        self.position = node.coordinate
        self.name = node.osmId
        self.node = node
        self.visited = False
        self.prevNode = None
        dft =  distance.distance(self.position.getLatLon(), targetNode.coordinate.getLatLon()).km * 1000
        self.h = dft
        self.f = self.g + self.h
        self.g = -1
        
    def calculateFrom(self,prevNode):
        """
        [Method] calculateFrom
        Calculate from a node we're currently exploring from. If the total distance is bigger, we ignore the prevNode
        
        Parameter:
            - prevNode : [Node] prevNode that we currently exploring from.
        """
        if (not self.visited):
            distanceToPrevious = 0
            distanceFromOrigin = 0
            distanceToPrevious = prevNode.g
            distanceFromOrigin = distance.distance(self.position.getLatLon(), prevNode.position.getLatLon()).km * 1000
            distanceFromOrigin += distanceToPrevious
            if (self.g > distanceFromOrigin or self.g == -1):
                self.g = distanceFromOrigin
                self.prevNode = prevNode
                self.f = self.g + self.h

def searchPath(osmMap, originNode, destinationNode, limit = None):
    """
    [Function] searchPath
    A function to searchPath from our origin to our destination.
        
    Parameter:
        - originNode      : [Node] prevNode that we currently exploring from.
        - destinationNode : [Node] prevNode that we currently exploring from.
        - limit           : [Float] Distance in meter to ignore nodes that is too far from the previous nodes (default = None)
        
    Return :
        - [Float] Distance in meters
        - [MovementSequence] the movementSequence
    """
    path = []
    quicksearch = {}
    workingList = []
    visited = []
    found = False
    finalNode = None
    distance = -1
    
    #insert starting node as the initial node
    startingNode = AStarNode(originNode,destinationNode)
    workingList.append(startingNode)
    
    #setup known blocked cells
    #for x in nzSim.blockedCells:
    #    x.setBlocked()
        
    #main loop
    while (workingList.__len__() != 0):        
        #get the first in the list
        workingNode = workingList.pop(0)
        workingNode.visited = True
        visited.append(workingNode)
        workingCell = workingNode.node
        sequence = None
        #start working if the limit is None or there is no path having lower distance than the designated limit
        if (limit is None or workingNode.f < limit):
            #loop through all of the path
            for x in workingCell.connections:
                #find if the a star node is created or not
                temp = quicksearch.get(x.osmId)
                #continue if condition apply
                if (temp is None or temp not in visited):
                    #if not created, create it
                    if temp is None:
                        temp = AStarNode(x,destinationNode)
                        quicksearch[temp.name] = temp
                    #calculate value
                    prevValue = temp.f
                    temp.calculateFrom(workingNode)
                    currentValue = temp.f
                    
                    #if destination reached
                    if (x == destinationNode):
                        #backtrack to create path
                        finalNode = temp
                        backtracking = finalNode
                        distance = finalNode.f
                        while backtracking != startingNode:
                            #create movement vector
                            movement = MovementVector(backtracking.prevNode.node, backtracking.node)
                            backtracking = backtracking.prevNode
                            path.insert(0,movement)
                        found = True
                        sequence = MovementSequence(path,distance)
                        break            
                        
                    #
                    #if (workingList.__len__() == 0):
                    #    workingList.append(temp)
                    #else:
                    
                    # messy method to find the right index to insert it based on value order
                    # remove to re-insert
                    if (temp in workingList):
                        workingList.remove(temp)
                    inserted = False

                    for i in range(0,workingList.__len__()):
                        #insert in the right index
                        if (workingList[i].f > currentValue):
                            workingList.insert(i,temp)
                            inserted = True
                            break
                    #if not inserted yet, it means it's the last index
                    if(not inserted):
                        workingList.append(temp)
        if (found):
            break
    return distance, sequence

   