#import threading
import multiprocessing 

#class StepThread(threading.Thread):
class StepThread(multiprocessing.Process):
    """
    [Class] StepThread
    Class for doing pathfinding in multithreading like process.
    
    Properties:
        - name = [string] name of this thread
        - agents = [array] array of agents
        - stepCount = [int] current step count which represent how many simulated seconds from the beggining of the simulation
        - stepValue = [int] how many step forward do we want to 
        - timeStamp = [array]  the timestamp of the history proporties
        - threadNumber = [int] how many thread this simulator allowed to create when doing pathfinding
        - activitiesDict = [dict] dictionary to store the activity type of the agent during this hour. key = agent's id
        - returnDict = [dict] dictionary to store the extracted movement sequence of the agent. key = agent's id
        
    Deprecated Properties:
        - state = [string] current state (Deprecated, will be removed soon)
        - finished = [boolean] flag if the process is finished or not 
        
    TO DO: remove unused pipeline
    """
    def __init__(self, name, agents,timeStamp,returnDict,activitiesDict):
        """
        [Constructor] 
        Constructor for StepThread class

        Parameters:
            - name = [string] name of this thread
            - agents = [array] array of agents
            - stepCount = [int] current step count
            - returnDict = [dict] dictionary to store the extracted movement sequence of the agent. key = agent's id
            - activitiesDict = [dict] dictionary to store the activity type of the agent during this hour. key = agent's id
        """
        #threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)
        self.name = name
        self.agents = agents
        self.state = "step"
        self.timeStamp = timeStamp
        self.stepValue = 24*3600
        self.activitiesDict = activitiesDict
        self.returnDict = returnDict
        self.finished = False
        
    def setStateToStep(self,stepValue):
        """
        [Method] setStateToStep 
        mark that the stepthread is going to do pathfinding 

        Parameters:
            - stepValue : [int] How many seconds we want to step forward
        """
        self.state = "step"
        self.stepValue = stepValue
        
    def setStateToInfect(self,stepValue):
        """
        [Method] setStateToInfect 
        DEPRECATED
        """
        self.state = "infect"
        self.stepValue = stepValue
        
    def setStateToFinalize(self,stepValue):
        """
        [Method] setStateToFinalize 
        DEPRECATED
        """
        self.state = "finalize"
        self.stepValue = stepValue
        
    def run(self):
        """
        [Method] run 
        main function that the MultiProcess class will run
        
        TO DO: remove unused pipeline
        """
        if self.state == "step":
            self.step()
        elif self.state == "infect":
            self.infect()
        else:
            self.finalize()
        self.finished = True
        print(f'{self.name} finished')

    def step(self):
        """
        [Method] step 
        pathfind function
        
        TO DO: merge with run
        """
        #day, hour = self.currentHour()
        for i in range(0,len(self.agents)):
            result = self.agents[i].checkSchedule(self.timeStamp,self.stepValue)
            self.activitiesDict[f"{self.agents[i].agentId}"] = self.agents[i].activities
            if result is not None:
                self.returnDict[f"{self.agents[i].agentId}"] = result
        
#     def infect(self):
#         """
#         [Method] infect 
#         DEPRECATED
#         """
#         for i in atpbar(range(len(self.agents)), name= f"{self.name} Infect Function"):
#             self.agents[i].checkInfection(self.stepValue)

#     def finalize(self):
#         """
#         [Method] finalize 
#         DEPRECATED
#         """
#         for i in atpbar(range(len(self.agents)), name= f"{self.name} Finalize Function"):
#             self.agents[i].finalize(self.stepValue)
                     
#     def currentHour(self):
#         """
#         [Method] currentHour
#         method to return the current tiem
        
#         return: 
#             - day = [int] current simulated day (0-6) 0 = Monday, 6 = Sunday
#             - hour = [int] current simulated hour
#         """
#         hour = int(self.stepCount / 3600)% 24
#         day = int(self.stepCount / (24*3600)) % 7
#         return day,hour
