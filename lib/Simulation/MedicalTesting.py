import random 
import numpy as np
from . PCRResult import PCRResult
class MedicalTesting:
    def __init__(self,rng,accuracy):
        self.accuracy = accuracy
        self.rng = rng
        
    def test(self,agent,timeStamp):        
        if (self.rng.uniform(0.0,1.0) < self.accuracy):
            # correct result
            agent.testResult = PCRResult(agent, (agent.infection is not None) ,timeStamp,24*3600) 
        else:
            # incorrect result
            agent.testResult = PCRResult(agent, not (agent.infection is not None) ,timeStamp,24*3600) 
        agent.newTestResult = agent.testResult
        agent.waitingResult = True
            