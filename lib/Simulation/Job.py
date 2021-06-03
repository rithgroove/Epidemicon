
class Job:
    """
    [Class] Job
    
    
    Properties:
        - home : [] the building the house is in
        - currentLocation : [Coordinate] the agents that live inside this home
        - infection_status : [string] SEIR (Susceptible, Exposed, Infectious, Recovered)
        - age :[int] Age
        - mainJob : [Job] job
    """
    def __init__(self,name,age,job):
        self.name = name
        self.work = age
        self.mainJob = job
        self.infection_status = "Susceptible"
        self.currentLocation = home.building.coordinate