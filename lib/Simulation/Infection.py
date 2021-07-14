import random
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
    def __init__(self,origin,target,step,dormant = 2 *24 *3600, recovery = 3*24*3600,location = "Undefined"):
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
        self.step = step
        self.dormant = dormant
        self.recovery = recovery
        self.location = location
        
    def finalize(self,currentStepCount,stepLength):
        """
        [Method] finalize
        Method to change the status of the agent
        
        Parameter:
            - step : current simulator stepCount
        """
        if (currentStepCount - self.step < self.dormant):
            self.target.infectionStatus = "Exposed" 
        elif (currentStepCount - self.step < self.dormant+ self.recovery):
            self.target.infectionStatus = "Infectious"
            if self.target.status == "Normal" and random.randint(0,1000000)< ((30000 * self.target.risk)/ (24*3600/stepLength)):
                self.target.status = "Symptomatics"
            elif self.target.status == "Symptomatics" and random.randint(0,1000000) < ((10000 * self.target.risk)/ (24*3600/stepLength)):
                self.target.status = "Severe"
        elif (currentStepCount - self.step >= self.dormant+ self.recovery):
            self.target.infectionStatus = "Recovered"
            self.target.status = "Normal"

    
    def summarize(self):
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
        day,hour,minutes = step2Hour(self.step)
        result["exposedTimeStamp"] = self.step
        result["exposedDay"] = day
        result["exposedHour"] = hour       
        result["exposedMinutes"] = minutes
        result["incubationDuration"] = self.dormant
        
        # infectious
        day,hour,minutes = step2Hour(self.step+self.dormant)
        result["infectiousTimeStamp"] = self.step+self.dormant
        result["infectiousDay"] = day
        result["infectiousHour"] = hour
        result["infectiousMinutes"] = minutes
        result["recoveryDuration"] = self.recovery
        
        # recovered
        day,hour,minutes = step2Hour(self.step+self.dormant+self.recovery)
        result["recoveredTimeStamp"] = self.step+self.dormant+self.recovery
        result["recoveredDay"] = day
        result["recoveredHour"] = hour
        result["recoveredMinutes"] = minutes
        
        
        
        

            
def step2Hour(hour):
    hour = int(self.stepCount / 3600)% 24
    day = int(hour /24) % 7
    minutes = int(self.stepCount/60)%60
    return day,hour, minutes
