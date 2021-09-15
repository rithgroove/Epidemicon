

class PCRResult:
	def __init__(self,agent, result,timeStamp, waitDuration):
		self.agent = agent
		self.realCondition = self.agent.infectionStatus
		self.result = result
		if (agent.infection is not None and result):
			self.status = "Positive"
		elif (agent.infection is None and not result):
			self.status = "Negative"
		elif (agent.infection is None and not result):
			self.status = "False Positive"
		else:
			self.status = "False Negative"
		self.timeStamp = timeStamp.clone()
		self.finishedTimeStamp = timeStamp.clone()
		self.finishedTimeStamp.step(waitDuration)

	def finalize(self,timeStamp):
		if (self.finishedTimeStamp.isAfter(timeStamp)):
			self.agent.PCRResult = None
			self.agent.testedPositive = self.result
			minDay = timeStamp.getDay() -2 
			if minDay < 0:
				minDay = 0 
			buildingVisited = []
			for day in range(minDay,timeStamp.getDay()+1):
				if (day in self.agent.visitHistory.keys()):
					history = self.agent.visitHistory[day]
					for visit in history:
						if visit.building not in buildingVisited:
							buildingVisited.append(visit.building)
			for building in buildingVisited:
				for day in range(minDay,timeStamp.getDay()+1):
					if (day in building.visitHistory.keys()):
						history = building.visitHistory[day]
						for visit in history:
							print("people start to get anxious")
							visit.agent.setAnxious(True)

	def extract(self):
		result = {}
		result["agentId"] = self.agent.agentId
		result["agentProfession"] = self.agent.getProfession()
		result["realCondition"] = self.realCondition
		result["testResult"] = self.result
		result["status"] = self.status
		result["testedTimestamp"] = self.timeStamp.stepCount
		result["testedDay"] = self.timeStamp.getDay()
		result["testedHour"] = self.timeStamp.getHour()
		result["testedMinutes"] = self.timeStamp.getMinute()
		result["resultTimestamp"] = self.finishedTimeStamp.stepCount
		result["resultDay"] = self.finishedTimeStamp.getDay()
		result["resultHour"] = self.finishedTimeStamp.getHour()
		result["resultMinutes"] = self.finishedTimeStamp.getMinute()
		return result

def getPCRResultKey():
	temp = []
	temp.append("agentId")
	temp.append("agentProfession")
	temp.append("realCondition")
	temp.append("testResult")
	temp.append("status")
	temp.append("testedTimestamp")
	temp.append("testedDay")
	temp.append("testedHour")
	temp.append("testedMinutes")
	temp.append("resultTimestamp")
	temp.append("resultDay")
	temp.append("resultHour")
	temp.append("resultMinutes")
	return temp
