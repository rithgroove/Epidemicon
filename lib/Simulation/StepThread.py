#import threading
import multiprocessing 
import time 
import random
from atpbar import atpbar,register_reporter, find_reporter

#class StepThread(threading.Thread):
class StepThread(multiprocessing.Process):
    def __init__(self, name, agents,stepCount,returnDict,activitiesDict):
        #threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)
        self.name = name
        self.agents = agents
        self.state = "step"
        self.stepCount = stepCount
        self.stepValue = 24*3600
        self.activitiesDict = activitiesDict
        self.returnDict = returnDict
        self.finished = False
        
    def setStateToStep(self,stepValue):
        self.state = "step"
        self.stepValue = stepValue
        
    def setStateToInfect(self,stepValue):
        self.state = "infect"
        self.stepValue = stepValue
        
    def setStateToFinalize(self,stepValue):
        self.state = "finalize"
        self.stepValue = stepValue
        
    def run(self):
        #voodoo line, do not remove, this helps to trigger the progress bar correctly
        print(' ', end='', flush=True)
        if self.state == "step":
            self.step()
        elif self.state == "infect":
            self.infect()
        else:
            self.finalize()
        self.finished = True

    def step(self):
        day, hour = self.currentHour()
        register_reporter(find_reporter())
        for i in atpbar(range(len(self.agents)), name= f"{self.name} Step Function"):
            result = self.agents[i].checkSchedule(day,hour,self.stepValue)
            self.activitiesDict[f"{self.agents[i].agentId}"] = self.agents[i].activities
            if result is not None:
                self.returnDict[f"{self.agents[i].agentId}"] = result
        
           
    def infect(self):
        for i in atpbar(range(len(self.agents)), name= f"{self.name} Infect Function"):
            self.agents[i].checkInfection(self.stepValue)

    def finalize(self):
        for i in atpbar(range(len(self.agents)), name= f"{self.name} Finalize Function"):
            self.agents[i].finalize(self.stepValue)
                     
    def currentHour(self):
        hour = int(self.stepCount / 3600)% 24
        day = int(self.stepCount / (24*3600)) % 7
        return day,hour
