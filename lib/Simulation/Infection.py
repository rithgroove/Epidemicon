
class Infection:
    """
    [Class] Infection
        
    Properties:
        - Origin: The virus carrier
        - Target: The target
        - Step: the step number when the infection was generated
    """
    def __init__(self,origin,target,step,dormant ,recovery):
        self.origin = origin
        self.target = target
        self.step = step
        self.dormant = dormant
        self.recovery = recovery
        
    def finalize(self,step):
        if (step - self.step < dormant):
            self.target.infection_status = "Exposed" 
        elif (step - self.step < dormant+ recovery):
            self.target.infection_status = "Infectious"
        elif (step - self.step >= dormant+ recovery):
            self.target.infection_status = "Recovered"