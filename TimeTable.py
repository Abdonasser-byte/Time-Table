class TimeTable:
    def __init__(self):
        self.hours = ["8:30", "9:30", "10:30", "11:30", "12:30", 
                      "1:30", "2:30", "3:30", "4:30", "5:30", "6:30"]
        self.days = ["Friday", "Saturday", "Sunday" ,"Monday", "Tuesday", "Wednesday", "Thursday" ]
        self.table = [["" for _ in self.hours] for _ in self.days]
    
    def getTimeTable (self):
        return self.table

    def __str__(self):
        timetable_str = "Time Table:\n"
        timetable_str += "            \t   " + " | ".join(self.hours)  + "\n"
        for day, schedule in zip(self.days, self.table):
            formatted_schedule = ["-" if slot == "" else slot for slot in schedule]
            timetable_str += f"{day:8} " + " | ".join(formatted_schedule) + "\n"
        return timetable_str

    def add_entry(self, day, hours, entry):
        day_index = self.days.index(day)
        
        if (self.isEmpty(day,hours)) == False :
             return False
        
        for hour in hours:
                hour_index = self.hours.index(hour)
                self.table[day_index][hour_index] = entry
        
        return True

    
    def isEmpty(self,day,hours):
        day_index = self.days.index(day)
        for hour in hours:
                hour_index = self.hours.index(hour)
                if self.table[day_index][hour_index]:
                    return False
        return True

    def remove_entry(self, day, hours):
        day_index = self.days.index(day)
        for hour in hours:
            hour_index = self.hours.index(hour)
            self.table[day_index][hour_index] = ""



