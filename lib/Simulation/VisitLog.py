class VisitLog:
    def __init__(self, agent, building, timeStamp):
        self.agent = agent
        self.infectionStatus = agent.status
        self.building = building 
        self.timeStamp = timeStamp.clone()
    
    def __str__(self):
        tempString = "[VisitLog]\n"
        tempString+= self.timeStamp.__str__()
        tempString+= f"\n" 
        tempString+= f"Agent      : {self.agent.agentId}\n" 
        tempString+= f"Profession : {self.agent.getProfession()}\n" 
        tempString+= f"Status     : {self.infectionStatus}\n"         
        tempString+= f"Building   : {self.building.type}\n"
        tempString+= f"Building Id: {self.building.buildingId}\n"
        tempString+= f"OSM Map Id : {self.building.way.osmId}\n"
        tempString+= f"lat,lon    : {self.building.coordinate.lat},{self.building.coordinate.lon}\n"
        return tempString
    
    def summarize(self):
        temp = {}
        temp["timeStamp"]  = self.timeStamp.stepCount
        temp["week"]  = self.timeStamp.getWeek()
        temp["day"]  = self.timeStamp.getDay()
        temp["hour"]  = self.timeStamp.getHour()
        temp["minute"]  = self.timeStamp.getMinute()
        temp["second"]  = self.timeStamp.getSecond()
        temp["agentId"] = self.agent.agentId
        temp["agentProfession"] = self.agent.getProfession()
        temp["infectionStatus"] = self.infectionStatus
        temp["homeId"] = self.agent.home.building.buildingId
        temp["homeBuildingType"] = self.building.type
        temp["workId"] = self.agent.mainJob.building.buildingId
        temp["workBuildingType"] = self.building.type
        temp["buildingId"] = self.building.buildingId
        temp["buildingType"] = self.building.type
        return temp
        
def getVisitKey():
    key = []
    key.append("timeStamp")
    key.append("week")
    key.append("day")
    key.append("hour")
    key.append("minute")
    key.append("second")
    key.append("agentId")
    key.append("agentProfession")
    key.append("infectionStatus")
    key.append("homeId")
    key.append("homeBuildingType")
    key.append("workId")
    key.append("workBuildingType")
    key.append("buildingId")
    key.append("buildingType")
    return key