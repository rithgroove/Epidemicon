
class Agent:
    """
    [Class] Agent
    
    
    Properties:
        - home : [] the building the house is in
        - currentLocation : [Coordinate] the agents that live inside this home
        - infection_status : [string] SEIR (Susceptible, Exposed, Infectious, Recovered)
        - age :[int] Age
        - mainJob : [Job] job
    """
    def __init__(self,home,age,job):
        self.home = home
        self.age = age
        self.mainJob = job.generateJob()
        self.mainJob.setAgent(self)
        self.infection_status = "Susceptible"
        self.currentLocation = home.coordinate().newCoordinateWithTranslation()
        self.oval = None
        self.name = ""