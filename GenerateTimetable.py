import math


class GenerateTimeTable :


    def is_course_scheduled(entries, day, hour):
        for entry in entries:
            course_name, teacher_id, hall_code, entry_day, list_of_hours, course_id, teacher_name = entry
        
            if entry_day == day and hour in list_of_hours:
                return True  # Found a match

        return False


    def create_timetable(self,courses, teachers, validation_halls, course_teacher_links,level,courseTimeHall,validation_labs, course_assistance_link , assistant):
        timetable = []
        valid_hours = ["8:30", "9:30", "10:30", "11:30", "12:30", 
                    "1:30", "2:30", "3:30", "4:30", "5:30", "6:30"]
        
        def is_valid(course, teacher, hall, day, hour,level):
            if not hall.is_hall_available(day, hour):
                print("false form hall ava ")
                return False
            if not teacher.add_data_timetable(day, hour, course.get_course_code()):
                print("false form hall add_data_timetable ")
                return False
            
            if not level._timetable.isEmpty( day, hour):
                return False

            if hall.get_normal_capacity() < course.get_number_of_students(): 
                return True
            return True

        def generate_consecutive_hours( start_time, consecutive_count):
            if start_time not in valid_hours:
                return []
            start_index = valid_hours.index(start_time)
        
            consecutive_hours = []

            if int(start_index+int(consecutive_count)) >= len(valid_hours):
                return []
            for i in range(start_index,int(start_index+int(consecutive_count))) :
                consecutive_hours.append(valid_hours[i])
            if len(consecutive_hours) < consecutive_count:
                return []

            return consecutive_hours


        def assign_course(index):
            if index == len(courses):
                return True
            course = courses[index]
            linked_teacher_id = None
            teacher = None
            if(course.get_type() == 0 ):
                linked_teacher_id = next(link._teacher_id for link in course_teacher_links if link._course_id == course.get_course_id())
                teacher = next(t for t in teachers if t._id == linked_teacher_id)
            
            if(course.get_type() != 0 ):
                linked_teacher_id = next(link._teacher_id for link in course_assistance_link if link._course_id == course.get_course_id())
                teacher = next(t for t in assistant if t._id == linked_teacher_id)

            for day in teacher.get_available_days():
                for hour in validation_halls.halls[0]._timetable.hours:
                    listOfHour =generate_consecutive_hours(hour,max( math.ceil(course.get_lecture_hours()),1) )
                    hall = None
                    if(course.get_type()!=2):
                        hall = validation_halls.find_valid_hall(course.get_number_of_students(), day, listOfHour)
                    if(course.get_type()==2):
                        hall = validation_labs.find_valid_lab(3, day, listOfHour)
                    
                    if(hall == None or len(listOfHour) == 0):
                        continue
                    if(is_valid(course,teacher,hall,day,listOfHour,level) == False):
                        continue
                    hall.add_data_timetable(day, listOfHour, course.get_course_code())
                    teacher.add_data_timetable(day, listOfHour, course.get_course_code())
                    timetable.append((course.get_course_name(), teacher.get_id(), hall.get_hall_id(), day, listOfHour , course.get_course_id() , teacher.get_name()))
                    level._timetable.add_entry(day, listOfHour, course.get_course_code())

                    if assign_course(index + 1):
                        courseTimeHall[str(course.get_course_code()) + str(course.get_course_name()) + str(course.get_course_id())] = [ hall.get_hall_id()]
                        return True
                    
                    hall.remove_data_timetable(day, listOfHour)
                    teacher.get_timetable().remove_entry(day, listOfHour)
                    timetable.pop()
                    level._timetable.remove_entry(day, [hour])
                    validation_halls.reset_valid_hall(hall)
                    # return None
            return False

        if assign_course(0):
            return timetable
        else:
            return None