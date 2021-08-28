import random 
import numpy as np
class MedicalTesting:
    def __init__(self,accuracy):
        self.accuracy = accuracy
        
    def test(self,agent):
        if (random.uniform(0.0,1.0) < self.accuracy):
            return (agent.infection is not None)
        else 
            return not (agent.infection is not None)
            