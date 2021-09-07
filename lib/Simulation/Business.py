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

        # TODO: change randint to a random that takes the result from a normal curve
        self.startHour =  random.randint (min_start_hour, max_start_hour)
        workHours =  random.randint (min_workhour, max_workhour)
        self.finishHour = (self.startHour + workHours)%24

        workdays =  [0, 1, 2, 3,4 , 5, 6]
        if businessData["day"] == "weekday":
            workdays = [0, 1, 2, 3, 4]
        elif businessData["day"] == "weekend":
            workdays = [5, 6]
        activityPerWeek =  random.randint (min_activity_per_week, max_activity_per_week)
        activityPerWeek = np.min([activityPerWeek, len(workdays)])
        self.workdays = random.sample(workdays, activityPerWeek)

    def isOpen(self, day, hour):
        if day in self.workdays:
            # Have to cover the case where the working hours goes from a day to the next
            # could be done in one line but for readbility i divided in two
            if self.startHour <= self.finishHour and (self.startHour <= hour < self.finishHour):
                return True
            elif self.startHour >= self.finishHour and not(self.finishHour < hour <= self.startHour):
                return True
        return False