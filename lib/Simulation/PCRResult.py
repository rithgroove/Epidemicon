

class PCRResult:
	def __init__(self,agent, result,timeStamp, waitDuration):
		self.agent = agent
		self.realCondition = self.agent.infectionStatus
		self.result = result
		if (agent.infection is not None and result):
			self.status = "Positive"
		elif (agent.infection is None and not result):
			self.status = "Negative"
		elif (agent.infection is not None and result):
			self.status = "False Positive"
		else:
			self.status = "False Negative"
		self.healthStatus = agent.status
		self.timeStamp = timeStamp.clone()
		self.finishedTimeStamp = timeStamp.clone()
		self.finishedTimeStamp.step(waitDuration)

	def finalize(self,timeStamp):
		if (self.finishedTimeStamp.isAfter(timeStamp)):
			self.agent.testResult = None
			self.agent.testedPositive = self.result
			if (self.result):
				minDay = timeStamp.getDay() -2 
				if minDay < 0:
					minDay = 0 
				buildingVisited = []
				buildingVisited.append(self.agent.home.building) #inform people that live in the same building
				if not self.agents.mainJob.isOutsideCity():
					buildingVisited.append(self.agent.mainJob.building) #inform people that work in the workplace
				for building in buildingVisited:
					for day in range(minDay,timeStamp.getDay()+1):
						if (day in building.visitHistory.keys()):
							history = building.visitHistory[day]
							for visit in history:
								visit.agent.setAnxious(True)

	def extract(self):
		result = {}
		result["agentId"] = self.agent.agentId
		result["agentProfession"] = self.agent.getProfession()
		result["realCondition"] = self.realCondition
		result["testResult"] = self.result
		result["status"] = self.status
		result["healthStatus"] = self.healthStatus
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
	temp.append("healthStatus")
	temp.append("testedTimestamp")
	temp.append("testedDay")
	temp.append("testedHour")
	temp.append("testedMinutes")
	temp.append("resultTimestamp")
	temp.append("resultDay")
	temp.append("resultHour")
	temp.append("resultMinutes")
	return temp
