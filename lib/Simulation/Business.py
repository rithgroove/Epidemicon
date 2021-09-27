import numpy as np

class Business:
    def __init__(self, building, businessData, rng) -> None:
        self.building = building

        min_workhour = int(businessData["min_workhour"])
        max_workhour = int(businessData["max_workhour"])
        min_start_hour = int(businessData["min_start_hour"])
        max_start_hour = int(businessData["max_start_hour"])
        min_activity_per_week = int(businessData["min_activity_per_week"])
        max_activity_per_week = int(businessData["max_activity_per_week"])
        open24hoursChance = float(businessData["open_24_hours_chance"])

        # TODO: change randint to a random that takes the result from a normal curve
        self.startHour = min_start_hour
        if (min_start_hour != max_start_hour):
            self.startHour =  rng.integers(min_start_hour, max_start_hour)
            
        workHours = min_workhour
        if (min_workhour != max_workhour):
            workHours =  rng.integers(min_workhour, max_workhour)
        self.finishHour = (self.startHour + workHours)%24

        if  rng.random() < open24hoursChance:
            self.startHour = 0
            self.finishHour = 0

        workdays =  [0, 1, 2, 3,4 , 5, 6]
        if businessData["day"] == "weekday":
            workdays = [0, 1, 2, 3, 4]
        elif businessData["day"] == "weekend":
            workdays = [5, 6]
            
        activityPerWeek = min_activity_per_week
        if (min_activity_per_week < max_activity_per_week):
            activityPerWeek =  rng.integers(min_activity_per_week, max_activity_per_week)            
        activityPerWeek = np.min([activityPerWeek, len(workdays)])
        self.workdays = rng.choice(workdays, activityPerWeek, replace=False)

        # These vars are used to set the lockdown and reset it to the original value when it ends
        self.isLockdown = False
        self.originalStartHour = self.startHour
        self.originalFinishHour = self.finishHour
        self.originalWorkdays = self.workdays

    def isOpen(self, day, hour):
        if day in self.workdays:
            # Have to cover the case where the working hours goes from a day to the next
            # could be done in one line but for readbility i divided in two
            if self.startHour <= self.finishHour and (self.startHour <= hour < self.finishHour):
                return True
            elif self.startHour >= self.finishHour and not(self.finishHour <= hour < self.startHour):
                return True
        return False


    def startLockdown(self, startHour, finishHour, workdays):
        self.startHour = startHour
        self.finishHour = finishHour
        # self.workdays = workdays
        self.isLockdown = True

    def finishLockdown(self):
        self.startHour = self.originalStartHour
        self.finishHour = self.originalFinishHour
        self.workdays = self.originalWorkdays
        self.isLockdown = False
