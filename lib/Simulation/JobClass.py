from .Job import Job
import random
import numpy as np
class JobClass:
    """
    [Class] JobClass
    
    Properties:
        - name : [String] Job name
        - minWorkHour : [int] minimum possible workhour the agent can work for a day
        - maxWorkHour : [int] maximum possible workhour the agent can work for a day
        - place : [string] the type of building this job takes place
        - minAge : [int] minimum age of the agent that have this profession 
        - minAge : [int] maximum age of the agent that have this profession 
        - populationProportion : [int] the proportion of agents with this job in the simulated area
        - minStartHour : [int] minimum possible start hour for the job
        - maxStartHour : [int] maximum possible start hour for the job
        - workDays : [array] array of boolean to represent each day from monday to sunday
        - minActivityPerWeek : [int] minimum number of workdays per week
        - maxActivityPerWeek : [int] maximum number of workdays per week
        - outsideCity : [boolean] maximum number of workdays per week
        - generatedJobs : [array] all the job this job class generated
    """
    def __init__(self,csvDict):
        self.name = csvDict["name"]
        self.minWorkhour = int(csvDict["min_workhour"])
        self.maxWorkhour = int(csvDict["max_workhour"])
        self.place = csvDict["place"]
        self.minAge = int(csvDict["min_age"])
        self.maxAge = int(csvDict["max_age"])
        self.populationProportion = int(csvDict["population_proportion"])
        self.minStartHour = int(csvDict["min_start_hour"])
        self.maxStartHour = int(csvDict["max_start_hour"])
        self.day = csvDict["day"]
        self.workDays = [False,False,False,False,False,False,False]
        self.buildings = []
        if csvDict["day"] == "weekday":
            self.workDays = [True,True,True,True,True,False,False]
        elif csvDict["day"] == "everyday":
            self.workDays = [True,True,True,True,True,True,True]
        elif csvDict["day"] == "weekend":
            self.workDays = [False,False,False,False,False,True,True]
        else:
            i = self.day.split(",")
            for x in i:
                if x.lower() == "mon":
                    self.workDays[0] = True
                elif x.lower() == "tue":
                    self.workDays[1] = True
                elif x.lower() == "wed":
                    self.workDays[2] = True
                elif x.lower() == "thu":
                    self.workDays[3] = True
                elif x.lower() == "fri":
                    self.workDays[4] = True
                elif x.lower() == "sat":
                    self.workDays[5] = True
                elif x.lower() == "sun":
                    self.workDays[6] = True
        self.workDays = np.array(self.workDays)
        self.minActivityPerWeek = int(csvDict["min_activity_per_week"])
        self.maxActivityPerWeek = int(csvDict["max_activity_per_week"])
        self.outsideCity = csvDict["outside_city"] == "yes"
        self.generatedJobs = []
        #self.randomInfectionRate = float(csvDict["random_infection_rate"])
        
    def addBuilding(self,building):
        """
        [Method] addBuilding        
        add a building where this job might happen.
        """
        self.buildings.append(building)
        
    def __str__(self):
        """
        [Method] __str__        
        return a string that summarized the job class
        """
        tempstring = f"[Job Class]\n"
        tempstring = tempstring + f"name : {self.name}\n"
        tempstring = tempstring + f"work place : {self.place}\n"
        tempstring = tempstring + f"working hour: {self.minWorkhour} - {self.maxWorkhour} hours\n"
        tempstring = tempstring + f"operational hour: {self.minStartHour}:00 - {self.maxStartHour}:00\n"
        tempstring = tempstring + f"working days: {self.minActivityPerWeek} - {self.maxActivityPerWeek} days per week\n"
        tempstring = tempstring + f"age range: {self.minAge} - {self.maxAge} years old\n"
        tempstring = tempstring + f"workdays : {self.day}\n"
        if (self.outsideCity):
            tempstring = tempstring + f"location : inside city\n"
        else:
            tempstring = tempstring + f"location : outside city\n"
            
        tempstring = tempstring + f"workdays : {self.day}\n"
        #tempstring = tempstring + f"random infection rate : {self.randomInfectionRate}\n"
        return tempstring
    
    def generateJob(self):
        """
        [Method] generateJob        
        generate a job instance based on this class
        """
        temp = Job(self)
        self.generatedJobs.append(temp)
        return temp

