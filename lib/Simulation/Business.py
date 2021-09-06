import random
import numpy as np

class Business:
    def __init__(self, building, businessData) -> None:
        self.building = building

        min_workhour = int(businessData["min_workhour"])
        max_workhour = int(businessData["max_workhour"])
        min_start_hour = int(businessData["min_start_hour"])
        max_start_hour = int(businessData["max_start_hour"])
        min_activity_per_week = int(businessData["min_activity_per_week"])
        max_activity_per_week = int(businessData["max_activity_per_week"])

        self.workhour =  random.randint (min_workhour, max_workhour)
        self.startHour =  random.randint (min_start_hour, max_start_hour)

        workdays =  [0, 1, 2, 3,4 , 5, 6]
        if businessData["day"] == "weekday":
            workdays = [0, 1, 2, 3, 4]
        elif businessData["day"] == "weekend":
            workdays = [5, 6]
        activityPerWeek =  random.randint (min_activity_per_week, max_activity_per_week)
        activityPerWeek = np.min([activityPerWeek, len(workdays)])
        self.workdays = np.random.choice(workdays, activityPerWeek)

    def isOpen(self, day, hour):
        if day in self.workdays and (self.startHour <= hour <= self.startHour+self.workhour) :
            return True
        return False