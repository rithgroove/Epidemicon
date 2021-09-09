
class TimeStamp:
    
    def __init__(self, stepCount = 0):
        self.stepCount = stepCount
        
    def getHour(self):
        return int(int(self.stepCount/3600) %24)
    
    def getDay(self):
        return int((self.stepCount/(24*3600)))
    
    def getDayOfWeek(self):
        return int(int(self.stepCount/(24*3600))%7)
    
    def getSecond(self):
        return self.stepCount%60
    
    def getDayOfWeekStr(self):
        temp = self.getDayOfWeek()
        if (temp == 0):
            return "Mon"
        if (temp == 1):
            return "Tue"
        if (temp == 2):
            return "Wed"
        if (temp == 3):
            return "Thu"
        if (temp == 4):
            return "Fri"
        if (temp == 5):
            return "Sat"
        if (temp == 6):
            return "Sun"
      
    def getMinutes(self):
        return int(int(self.stepCount/60) % 60)

    def getWeek(self):
        return int(self.stepCount/(24*3600))
        
    def clone(self):
        return TimeStamp(self.stepCount)
    
    def step(self,stepSize):
        self.stepCount += stepSize
    
    def __str__(self):        
        week = self.getWeek()
        tempString = "{}, Week = {} Day = {}\n".format(self.getDayOfWeekStr(), self.getWeek(), self.getDay())
        tempString += "Current Time = {:02d}:{:02d}:{:02d}".format(self.getHour(),self.getMinutes(),self.getSecond())
        return tempString