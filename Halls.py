from TimeTable import TimeTable


class Halls:
    def __init__(self, hall_id,name, code, normal_capacity, exam_capacity):
        self._hall_id = hall_id
        self._hall_name = name
        self._code = code
        self._normal_capacity = normal_capacity
        self._exam_capacity = exam_capacity
        self._timetable = TimeTable()

    # Getters
    def is_hall_available(self, day, hours):
        timetable = self._timetable.getTimeTable()
        day_index = self._timetable.days.index(day)
    
        
        for hour in hours:
            hour_index = self._timetable.hours.index(hour)
            if timetable[day_index][hour_index] != "":
                return False
        
        return True

    def get_timetable(self):
        return self._timetable

    def get_name(self):
        return self._hall_name
    
    def add_data_timetable(self, day, hours, data):
        if isinstance(hours, str):
            hours = [hours]
        self._timetable.add_entry(day, hours, data)
    
    def remove_data_timetable(self, day, hours):
        if isinstance(hours, str):
            hours = [hours]
        self._timetable.remove_entry(day, hours)

    def get_hall_id(self):
        return self._hall_id
    
    def get_code(self):
        return self._code

   
    def get_normal_capacity(self):
        return self._normal_capacity

    def get_exam_capacity(self):
        return self._exam_capacity

    # Setters
    def set_hall_id(self, hall_id):
        self._hall_id = hall_id

    def set_timetable(self, timetable):
        self._timetable = timetable

    def set_code(self, code):
        self._code = code



    def set_normal_capacity(self, normal_capacity):
        self._normal_capacity = normal_capacity

    def set_exam_capacity(self, exam_capacity):
        self._exam_capacity = exam_capacity


# # Assuming Halls and TimeTable classes are already defined and imported

# # Create a Hall instance
# hall1 = Halls(hall_id=101, name="Hall A", code="HA101", normal_capacity=100, exam_capacity=50)

# # Add some entries to the timetable for Hall A (using the `add_data_timetable` method)
# hall1.add_data_timetable("Monday", ["8:30", "9:30"], "Meeting with Department A")
# hall1.add_data_timetable("Monday", ["10:30"], "Lecture on AI")
# hall1.add_data_timetable("Tuesday", ["9:30"], "Project Meeting")
# hall1.add_data_timetable("Tuesday", ["1:30", "2:30"], "Exam Preparation")

# # Now let's check if the hall is available at specific times

# # Check if Hall A is available on Monday from 8:30 to 9:30 (should return False because those slots are occupied)
# result1 = hall1.is_hall_available("Monday", ["8:30", "9:30"])
# print("Is Hall A available on Monday from 8:30 to 9:30?", result1)  # Expected: False (because it's already booked)

# # Check if Hall A is available on Tuesday from 10:30 to 11:30 (should return True because these slots are not booked)
# result2 = hall1.is_hall_available("Tuesday", ["10:30", "11:30"])
# print("Is Hall A available on Tuesday from 10:30 to 11:30?", result2)  # Expected: True (no entries)

# # Check if Hall A is available on Monday from 9:30 to 10:30 (should return False because 9:30 is occupied)
# result3 = hall1.is_hall_available("Monday", ["9:30", "10:30"])
# print("Is Hall A available on Monday from 9:30 to 10:30?", result3)  # Expected: False (because 9:30 is booked)

# # Check if Hall A is available on Wednesday from 8:30 to 9:30 (should return True because no data has been added for Wednesday)
# result4 = hall1.is_hall_available("Wednesday", ["8:30", "9:30"])
# print("Is Hall A available on Wednesday from 8:30 to 9:30?", result4)  # Expected: True (no bookings for Wednesday)

# # Check if Hall A is available on Tuesday from 1:30 to 2:30 (should return False because these slots are occupied for Exam Preparation)
# result5 = hall1.is_hall_available("Tuesday", ["1:30", "2:30"])
# print("Is Hall A available on Tuesday from 1:30 to 2:30?", result5)  # Expected: False (occupied for Exam Preparation)
