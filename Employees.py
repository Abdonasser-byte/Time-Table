
from TimeTable import TimeTable


class Employees:
    def __init__(self, name, emp_id, available_days, emp_type):
        self._name = name
        self._id = emp_id
        self._available_days = available_days
        self._type = emp_type
        timetable=TimeTable()
        self._timetable=timetable

    def add_data_timetable(self, day, listOfHours, data):
        if day in self._available_days:
            self._timetable.add_entry(day, listOfHours, data)
            return True
        else:
            return False
    
    
    def get_timetable(self):
        return self._timetable

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_available_days(self):
        return self._available_days

    def get_type(self):
        return self._type

    def set_name(self, name):
        self._name = name

    def set_id(self, emp_id):
        self._id = emp_id

    def set_available_days(self, available_days):
        self._available_days = available_days

    def set_timetable(self, timetable):
        self._timetable = timetable

    def set_type(self, emp_type):
        self._type = emp_type

    def __str__(self):
        return (f"Employee Name: {self._name}, ID: {self._id}, Available Days: {self._available_days}, "
                f"Type: {self._type} , TimeTable:{self._timetable} ")
    

''''

employee = Employees("John Doe", "E123", ["Monday", "Wednesday", "Friday"], "Full-Time")

# Adding entries to the employee's timetable
employee.add_data_timetable("Monday", "8:30", "Meeting")
employee.add_data_timetable("Wednesday", "1:30", "Workshop")
employee.add_data_timetable("Friday", "10:30", "Conference")

# Printing the employee's details and timetable
print(employee)
'''