#import random 
import numpy as np
class Job:
    """
    [Class] Job
    Class to represent a job instance for a single agent
    
    Properties:
        - jobClass : [JobClass] this job class
        - workhour: [int] how long the job takes place 
        - startHour: [int] what hour does this job begin
        - building : [Building] the place where the agent works
        - activityPerWeek :[int] how many workdays per week
        - workdays: [int] 8 bit integer that uses bit 1 as monday, 2 (b10) as tuesday, 4 (b100) as wednesday, etc
        - agent : [Agent] the agent this job belongs to
    """
    def __init__(self,jobClass,rng):
        self.jobClass =jobClass
        self.workhour =  jobClass.minWorkhour        
        if (jobClass.minWorkhour != jobClass.maxWorkhour):
            self.workhour =  rng.integers(jobClass.minWorkhour, jobClass.maxWorkhour)
        
        self.building = rng.choice(jobClass.buildings)

        self.startHour =  jobClass.minStartHour     
        if (jobClass.minStartHour != jobClass.maxStartHour):
            self.startHour =  rng.integers(jobClass.minStartHour,jobClass.maxStartHour)        
        
        
        
        self.activityPerWeek = jobClass.minActivityPerWeek
        if (jobClass.minActivityPerWeek != jobClass.maxActivityPerWeek):
            self.activityPerWeek =  rng.integers(jobClass.minActivityPerWeek,jobClass.maxActivityPerWeek)
        
        
        
       
        
        
        
        indexes = np.where(jobClass.workDays)[0]
        if len(indexes) < self.activityPerWeek+1:
            self.activityPerWeek = len(indexes)
        rng.shuffle(indexes)
        self.workdays = 0
        for i in indexes[:(self.activityPerWeek-1)]:
            self.workdays  += (2**(6-i))
        self.agent = None
        
    def getName(self):
        """
        [Method] getName        
        get the job name
        """
        return self.jobClass.name
    
    def isOutsideCity(self):
        """
        [Method] isOutsideCity        
        return True if the job is outside of simulated area
        """
        return self.jobClass.outsideCity
    
    def setAgent(self,agent):
        """
        [Method] setAgent        
        set the agent of this job instance assigned to
        """
        self.agent = agent
        
    def isWorking(self,day, hour):
        """
        [Method] isWorking        
        return True if the input is a working day. s
        """
        if self.workdays & (2**(6-day)) and (hour >= self.startHour and hour <= self.startHour+self.workhour) :
            return True
        return False