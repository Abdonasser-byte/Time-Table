import csv
from GenerateTimetable import GenerateTimeTable
from Levels import LEVELS
from CourseTeacherLink import CourseTeacherLink
from OutPut import OutPut
from ValidationHalls import ValidationHalls
from Read import ReadTopics
import os

import validateLabs
os.environ["ORACLEDB_THIN"] = "1"
import oracledb

username = 'CHIB'
password = 'CHIB'
host = '65.109.83.174'
port = 1551
sid = 'PSYSTEMSDB'

dsn = oracledb.makedsn(host, port, sid=sid)

try:
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn,
    )
    print("Successfully connected to Oracle Database using SID in Thin Mode")
except oracledb.Error as error:
    print("Error connecting to Oracle Database:", error)
    exit(1)


readtopics = ReadTopics(connection)

teachers = readtopics.ReadDoctors()

assistant = readtopics.getassistant()

all_halls = readtopics.RadHalls()

courses = readtopics.ReadCourses()

Labs = readtopics.ReadLabs()

Plan_Level, plan_level_sections_Level_id = readtopics.ReadStudyPlanLevel()

Plan_Courses ,plan_courses_dict = readtopics.ReadStudyPlanCourses(Plan_Level)

course_teacher_links = readtopics.getCourseEmployeeId()

course_assistance_link = readtopics.getSectionEmployeeId()

validation_halls = ValidationHalls(all_halls)

validation_labs = validateLabs.ValidationLabs(Labs)


sections = readtopics.getAvailableSection()

labs = readtopics.getAvailableLab()

final_course = []

Levels = []

course_hall = {}

Generator = GenerateTimeTable()

appended_course_ids = set()

courseTimeHall = {}

print("Size of Plan_Courses:", len(plan_courses_dict))
print("Size of all_halls:", len(all_halls))
print("Size of teachers:", len(teachers))
print("Size of courses:", len(courses))



for key,valus in plan_courses_dict.items() :
    Levels.append(LEVELS(key,valus))

def get_course_from_labs(course_id, labs):
    for lab in labs:
        if lab.get_course_id() == course_id:
            return lab  
    return None 

def get_course_from_sections(course_id, sections):
    for section in sections:
        if section.get_course_id() == course_id:
            return section  
    return None  


def get_entries_by_course_ids(course_ids, all_courses_generated):
    result = [entry for entry in all_courses_generated if entry[5] == course_ids]
    return result


coL = 0
coS = 0 
sum = 0
all_courses_generated = []
for key,valu in plan_courses_dict.items() :
    final_course.clear()
    for course in courses :
        for planx in valu :

            if (planx ==  course.get_course_id() ) and planx not in appended_course_ids and course.get_lecture_hours() > 0:
                final_course.append(course )
                section = get_course_from_sections(course.get_course_id() , sections)
                lab = get_course_from_labs(course.get_course_id() ,labs)
                if  section != None:
                    final_course.append(section )
                if  lab != None:
                    final_course.append(lab )
                appended_course_ids.add(planx)

    level= None
    idx = 0
    for lev in Levels :
        if(lev.get_id()==key):
            level=lev
            break
        idx += 1
    
    timetable= Generator.create_timetable(final_course, teachers, validation_halls, course_teacher_links,level,courseTimeHall,validation_labs , course_assistance_link , assistant)
    Levels[idx]=level
    if timetable or timetable != None:
        #  sum += len(final_course)
         for entry in timetable:
            #  print(entry)
             all_courses_generated.append(entry)
            #  print(f"Course {entry[0]} assigned to Teacher {entry[1]} in Hall {entry[2]} on {entry[3]} at {entry[4]}")
        #  print("we  end from here" , len(final_course) , " " , len(timetable) , " " , len(valu) , key)
    else:
         coL+= 1
         print("No valid timetable found")





idx= 0 
file_path = r'D:\time_table.csv'

for key,valu in plan_courses_dict.items() :
    allCourses = []
    for course in valu:
        list = get_entries_by_course_ids(course,all_courses_generated)
        for item in list :
            allCourses.append(item)
    write = OutPut()
    write.write_timetable_to_csv(Levels[idx]._timetable, file_path, allCourses , key,connection)
    idx += 1
# print( len(courseTimeHall)  , " "  , len(teachers) , " " , len(appended_course_ids) , " " , len(sections) , coL  , coS , sum , "\n" ,plan_courses_dict_generated) 


connection.close()