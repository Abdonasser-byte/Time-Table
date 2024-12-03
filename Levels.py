from Courses import Course
from TimeTable import TimeTable  # Assuming TimeTable class is imported correctly

class LEVELS:
    def __init__(self, level_id, course):
        self._id = level_id
        self._course = course
        self._timetable = TimeTable()  # Initialize an instance of TimeTable

    # Setter methods
    def set_id(self, level_id):
        self._id = level_id

    def set_course(self, course):
        self._course = course

    def set_timetable(self, timetable):
        self._timetable = timetable

    def is_day_empty(self, day):
        day_index = self.days.index(day)
        return all(slot == "" for slot in self.table[day_index])
    
    def validate_empty_days(self):
        empty_days_count = sum(1 for day in self.timetable.days if self.timetable.is_day_empty(day))
        return empty_days_count>=2

    # Getter methods
    def get_id(self):
        return self._id

    def get_course(self):
        return self._course


    def get_timetable(self):
        return self._timetable


# Example usage

