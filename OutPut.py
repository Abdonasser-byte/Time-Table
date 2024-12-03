

import codecs
import csv
import arabic_reshaper
from bidi.algorithm import get_display


class OutPut:

    def is_course_scheduled(self,entries, day, hour):
        for entry in entries:
            course_name, teacher_id, hall_code, entry_day, list_of_hours, course_id, teacher_name = entry
        
            if entry_day == day and hour in list_of_hours:
                return entry 

        return None

    def format_hours(self,hour_list):
        if len(hour_list) == 1:
            return hour_list[0]
        
        return f"{hour_list[0]} - {hour_list[-1]}"


    def write_timetable_to_csv(self, timetable, filepath,  allCourses , key,connection):
        days = timetable.days
        hours = timetable.hours
        hours = [""] + timetable.hours        
        file_path = rf"{filepath}_Name_Level_{key}.csv"
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(hours)
            for day in days:
                row = [day + "\nCourse Code\n" + "Course Name\n" + "Teacher Name\n" + "Hall Id\n"]
                for hour in timetable.hours:
                    var = self.is_course_scheduled(allCourses , day,hour)
                    if var != None:
                        course_name, teacher_id, hall_code, entry_day, list_of_hours, course_id, teacher_name = var
                        insert_sql = """
                        INSERT INTO course_schedule (plan_level_sec_id, course_id, teacher_id, hall_id, entry_day, list_of_hours)
                        VALUES (:plan_level_sec, :course_id, :teacher_id, :hall_id, :entry_day, :list_of_hours)
                        """
                        cursor = connection.cursor()
                        cursor.execute(insert_sql, {
                            'plan_level_sec': int(key),
                            'course_id': int(course_id),
                            'teacher_id': int(teacher_id),
                            'hall_id': int(hall_code),
                            'entry_day': str(entry_day),
                            'list_of_hours': str(self.format_hours(list_of_hours))
                            })
                        
                        row.append(f"Course Name: {course_name} \n Course Id: {course_id} \nTeacher Name: {teacher_name} \nHall: {hall_code}")
                    else :
                        row.append("")
                writer.writerow(row)
        
