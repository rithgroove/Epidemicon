class Way():
    """
    [Class] Way
    A class to represent the Open Street Map Way.
       
    Properties:
        - osmId : Open Street Map ID.
        - nodes : List of Nodes included in this way.
        - tags : A dictionary of the Map Feature of this object (check Open Street Map - Map Features).
    """
    
    def __init__(self):
        """
        [Constructor]
        Initialize an empty way.
        """
        self.osmId = ""
        self.nodes = []    
        self.tags = {}
        
    def fill(self, osmWay, nodes):
        """
        [Method] fill
        Fill up several property of this object, such as:
            - osmId
            - nodes
            - tags
        
        Parameter:
            - osmWay = osmium way node.
            - nodes = list to fill our version of Nodes.
        """
        self.osmId = f"{osmWay.id}"

        for node in osmWay.nodes:
            temp = nodes[f"n{node.ref}"]
            if (temp is not None):
                self.nodes.append(temp)
                temp.addWay(self)
            else:
                print("\n\nNode not Found\n\n")
            
        for tag in osmWay.tags:
            self.tags[tag.k] = tag.v
            
    def __str__(self):
        """
        [Method] __str__
        Generate the summarized way information string and return it.
        
        Return: [string] String of summarizedway information.
        """
        tempstring = f"id: {self.osmId}\n"
        tempstring = tempstring + f"number of nodes : {self.nodes.__len__()}\n"
        tempstring = tempstring + f"Tags : \n"
        for key in self.tags.keys():
            tempstring = tempstring + f"\t{key} : {self.tags[key]}\n"
        tempstring = tempstring + "\n"
        return tempstring