import random 
import numpy as np
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
    def __init__(self,jobClass):
        self.jobClass =jobClass
        self.workhour =  random.randint(jobClass.minWorkhour,jobClass.maxWorkhour)
        self.building = random.choice(jobClass.buildings)
        self.workhour =  random.randint(jobClass.minStartHour,jobClass.maxStartHour)
        self.activityPerWeek =  random.randint(jobClass.minActivityPerWeek,jobClass.maxActivityPerWeek)
        self.startHour =  random.randint(jobClass.minStartHour,jobClass.maxStartHour)
        indexes = np.where(jobClass.workDays)[0]
        if len(indexes) < self.activityPerWeek+1:
            print("warning, activities per week is lower than the optional workdays")
            self.activityPerWeek = len(indexes)
        np.random.shuffle(indexes)
        self.workdays = 0
        #print(indexes)
        #print(self.activityPerWeek)
        for i in indexes[:(self.activityPerWeek-1)]:
            self.workdays  += (2**(6-i))
        self.agent = None
        
    def isOutsideCity(self):
        return self.jobClass.outsideCity
    
    def setAgent(self,agent):
        self.agent = agent
        
    def isWorking(self,day, hour):
        if self.workdays & (2**(6-day)) and (hour >= self.startHour and hour <= self.startHour+self.workhour) :
            return True
        return False
        