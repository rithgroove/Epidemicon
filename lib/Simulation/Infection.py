
class Infection:
    """
    [Class] Infection
        
    Properties:
        - Origin: The virus carrier
        - Target: The target
        - Step: the step number when the infection was generated
        - Dormant : 2 days
        - recovery : 14 days (2 weeks)
    """
    def __init__(self,origin,target,step,dormant = 2 *24 *3600, recovery = 14*24*3600):
        self.origin = origin
        self.target = target
        self.step = step
        self.dormant = dormant
        self.recovery = recovery
        
    def finalize(self,step):
        if (step - self.step < self.dormant):
            self.target.infectionStatus = "Exposed" 
        elif (step - self.step < self.dormant+ self.recovery):
            self.target.infectionStatus = "Infectious"
        elif (step - self.step >= self.dormant+ self.recovery):
            self.target.infectionStatus = "Recovered"

