from Employees import Employees


class Teachers(Employees):
    def __init__(self, name, emp_id, available_days, emp_type):
        super().__init__(name, emp_id, available_days, emp_type)

    def __str__(self):
        return super().__str__() 
    
    def validation(self):
        return True
    
    def validationDelegate(self):
        timetable = self._timetable.getTimeTable()
        for day_schedule in timetable:
            busy_slots = [i for i, slot in enumerate(day_schedule) if slot != ""]
            if busy_slots:
                for i in range(len(busy_slots) - 1):
                    if busy_slots[i] + 1 != busy_slots[i + 1]:
                        return False
        return True
    
    def add_data_timetable(self, day, hour, data):
        if day in self._available_days:
            self.get_timetable().add_entry(day, hour, data)
            if not self.validation():
                self.get_timetable().remove_entry(day, hour)
                return False
            return True
        else:
            return False

''''

# Example usage
teacher_delegate = Teachers("Jane Smith", "T456", ["Monday", "Wednesday", "Friday", "Saturday"], "Delegate", "Engineering")
teacher_regular = Teachers("John Doe", "T789", ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"], "Full-Time", "Mathematics")

# Adding entries to the teacher's timetable
print(teacher_delegate.add_data_timetable("Monday", "8:30", "Math Class"))   # Should return True
print(teacher_delegate.add_data_timetable("Wednesday", "9:30", "Science Class"))  # Should return True
print(teacher_delegate.add_data_timetable("Friday", "10:30", "Chemistry Lab"))  # Should return True
print(teacher_delegate.add_data_timetable("Tuesday", "8:30", "Physics Lecture"))  # Should return True
print(teacher_delegate.add_data_timetable("Saturday", "8:30", "Physics Lecture"))  # Should return True
print(teacher_delegate.add_data_timetable("Saturday", "9:30", "Physics Lecture"))  # Should return True
print(teacher_delegate.add_data_timetable("Saturday", "11:30", "Physics Lecture"))  # Should return False due to non-consecutive validation

print(teacher_regular.add_data_timetable("Monday", "8:30", "Math Class"))  # Should return True
print(teacher_regular.add_data_timetable("Wednesday", "9:30", "Science Class"))  # Should return True
print(teacher_regular.add_data_timetable("Friday", "10:30", "Chemistry Lab"))  # Should return True
print(teacher_regular.add_data_timetable("Thursday", "1:30", "Physics Lecture"))  # Should return True
#print(teacher_regular.add_data_timetable("Thursday", "5:30", "Physics Lecture"))  # Should return false

# Printing the teacher's details and timetable
print(teacher_delegate.get_timetable())
print(teacher_regular)

'''