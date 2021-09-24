#import random
from .TimeStamp import TimeStamp
class Infection:
    """
    [Class] Infection
        
    Properties:
        - origin: The virus carrier
        - target: The target
        - step: the step number when the infection was generated
        - dormant : how long the virus will stay dormant from the infection star
        - recovery : how long the person will recover from the infection after becaming infectious
    """
    def __init__(self,origin,target,timeStamp,dormant = 2 *24 *3600, recovery = 3*24*3600,location = "Undefined"):
        """
        [Constructor]

        Parameter:
            - origin : The virus carrier
            - target : The target
            - step: current simulator stepCount
            - dormant : how long the virus will stay dormant from the infection star (default = 2 days)
            - recovery : how much times required to transition between infectious to recovered (default = 3 days in seconds)
        """
        self.origin = origin
        self.target = target

        try :
            self.lat = target.currentLocation.lat
            self.lon = target.currentLocation.lon
            self.node = target.currentNode
        except:
            self.lat = 0.0
            self.lon = 0.0      
            self.node = None   
        self.timeStamp = timeStamp
        self.dormant = dormant
        self.recovery = recovery
        self.location = location
        self.timeStamp = timeStamp.clone()
        self.infectiousTimeStamp = timeStamp.clone()
        self.infectiousTimeStamp.step(dormant)
        self.recoveredTimeStamp = self.infectiousTimeStamp.clone()
        self.recoveredTimeStamp.step(recovery)
        self.symptomaticsTimeStamp = TimeStamp()
        self.severeTimeStamp = TimeStamp()
        
    def finalize(self,currentTimeStamp,stepLength,rng):
        """
        [Method] finalize
        Method to change the status of the agent
        
        Parameter:
            - step : current simulator stepCount
        """
        if (currentTimeStamp.stepCount - self.timeStamp.stepCount < self.dormant):
            self.target.infectionStatus = "Exposed" 
        elif (currentTimeStamp.stepCount - self.timeStamp.stepCount < self.dormant+ self.recovery):
            self.target.infectionStatus = "Infectious"
            if self.target.status == "Normal" and rng.integers(0,1000000)< ((200000 * self.target.risk)/ (24*3600/stepLength)):
                self.target.status = "Symptomatics"
                self.symptomaticsTimeStamp = currentTimeStamp.clone()
            elif self.target.status == "Symptomatics" and rng.integers(0,1000000) < ((50000 * self.target.risk)/ (24*3600/stepLength)):
                self.target.status = "Severe"
                self.severeTimeStamp = currentTimeStamp.clone()
        elif (currentTimeStamp.stepCount - self.timeStamp.stepCount >= self.dormant+ self.recovery):
            self.target.infectionStatus = "Recovered"
            self.target.status = "Normal"

    
    def summarize(self):
        """
        [Method] summarize
        Method to extract information of this infection instance into a dictionary

        return:
            -[Dictionary] = information about this infection instance

        TODO : change the function name to extract
        """    
        result = {}
        result["location"] = self.location
        result["lat"] = self.lat
        result["lon"] = self.lon
        if self.node is None:
            result["nodeId"] = "Not found"
        else:
            result["nodeId"] = self.node.osmId
            
        result["infectedAgentId"] = self.target.agentId
        result["infectedAgentProfession"] = self.target.mainJob.getName()
        result["originAgentId"] = self.origin.agentId
        result["originAgentProfession"] = self.origin.mainJob.getName()
        
        # exposed
        result["exposedTimeStamp"] = self.timeStamp.stepCount
        result["exposedDay"] = self.timeStamp.getDay()
        result["exposedHour"] = self.timeStamp.getHour()
        result["exposedMinute"] = self.timeStamp.getMinute()
        result["incubationDuration"] = self.dormant
        
        # infectious
        result["infectiousTimeStamp"] = self.infectiousTimeStamp.stepCount
        result["infectiousDay"] = self.infectiousTimeStamp.getDay()
        result["infectiousHour"] = self.infectiousTimeStamp.getHour()
        result["infectiousMinute"] = self.infectiousTimeStamp.getMinute()
        result["recoveryDuration"] = self.recovery
        
        # recovered
        result["recoveredTimeStamp"] = self.recoveredTimeStamp.stepCount
        result["recoveredDay"] = self.recoveredTimeStamp.getDay()
        result["recoveredHour"] = self.recoveredTimeStamp.getHour()
        result["recoveredMinute"] = self.recoveredTimeStamp.getMinute()
        
        result["symptomaticTimeStamp"] = self.symptomaticsTimeStamp.stepCount
        result["symptomaticDay"] = self.symptomaticsTimeStamp.getDay()
        result["symptomaticHour"] = self.symptomaticsTimeStamp.getHour()
        result["symptomaticMinute"] = self.symptomaticsTimeStamp.getMinute()
        
        result["severeTimeStamp"] = self.severeTimeStamp.stepCount
        result["severeDay"] = self.severeTimeStamp.getDay()
        result["severeHour"] = self.severeTimeStamp.getHour()
        result["severeMinute"] = self.severeTimeStamp.getMinute()
        
        return result
        