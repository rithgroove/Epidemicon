
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
        self.step = step
        self.dormant = dormant
        self.recovery = recovery
        self.location = location
        
    def finalize(self,step):
        """
        [Method] finalize
        Method to change the status of the agent
        
        Parameter:
            - step : current simulator stepCount
        """
        if (step - self.step < self.dormant):
            self.target.infectionStatus = "Exposed" 
        elif (step - self.step < self.dormant+ self.recovery):
            self.target.infectionStatus = "Infectious"
        elif (step - self.step >= self.dormant+ self.recovery):
            self.target.infectionStatus = "Recovered"

