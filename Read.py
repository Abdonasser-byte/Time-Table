import random
import pandas as pd
import os
import CourseTeacherLink
from ExcelReader import ExcelReader
from Courses import Course
from Halls import Halls
import LabHalls
from Teachers import Teachers


class ReadTopics:

    def __init__(self, connection):
        reader = ExcelReader()
        self._reader = reader
        self.connection = connection

    def generate_available_days(self, availability):
        days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        available_days = [day for day, is_available in zip(days, availability) if is_available]
        return available_days
    
    def findDaysArabic (self,row_Data): 
        days = []
        if(row_Data["السبت"] == "محدد") or 1 == 1:
            days.append(1)
        else :
            days.append(0)
        if(row_Data['الأحد'] == "محدد")or 1 == 1 :
            days.append(1)
        else :
            days.append(0)
        if(row_Data['الإثنين'] == "محدد") or 1 == 1 :
            days.append(1)
        else :
            days.append(0)
        if(row_Data['الثلاثاء'] == "محدد") or 1 == 1 :
            days.append(1)
        else :
            days.append(0)
        if(row_Data['الأربعاء'] == "محدد") or 1 == 1:
            days.append(1)
        else :
            days.append(0)
        if(row_Data['الخميس'] == "محدد")or 1 == 1 :
            days.append(1)
        else :
            days.append(0)
        return days
    
    def ReadDoctors (self) :
        cursor = self.connection.cursor()
        query = """
            SELECT CAD.EMPLOYEE_ID,
            E.EMPLOYEE_NAME
            FROM COURSES_ACTIVITY_DETAILS CAD
            LEFT JOIN EMPLOYEES E
            ON CAD.EMPLOYEE_ID = E.EMPLOYEE_ID
            WHERE CAD.ACTIVITY_TYPE = 'LECTURE'
            GROUP BY CAD.EMPLOYEE_ID , E.EMPLOYEE_NAME
        """
        cursor.execute(query)
        teachers = []
        for row in cursor:
            id = row[0]
            name = row[1]
            
            teachers.append(Teachers(name=name, emp_id=id, available_days=self.generate_available_days([1, 1, 1, 1, 1, 1]), emp_type="Full-time"))


        cursor.close()
        return teachers

        
        
        x =ReadTopics(self.connection)
        file_path = r'D:\staffdates.xls' 
        teachers = []
        columns  = [0,4]
        df = pd.read_excel(file_path, usecols=columns, engine='xlrd')
        df.columns = ['USER_ID', 'DAY_NAME_MONTH_DISPLAY']

        df['DAY_NAME_MONTH_DISPLAY'] = df['DAY_NAME_MONTH_DISPLAY'].str[4:].str.strip()

        grouped = df.groupby('USER_ID')['DAY_NAME_MONTH_DISPLAY'].apply(list).reset_index()

        for _, row in grouped.iterrows():
            # print(f"[{row['USER_ID']}]")
            # print(row['DAY_NAME_MONTH_DISPLAY'])
            teachers.append(Teachers(name=row['USER_ID'], emp_id=row['USER_ID'], available_days=row['DAY_NAME_MONTH_DISPLAY'], emp_type="Full-time", major="Enginnering"))
        return teachers
    
    def RadHalls (self):

        cursor = self.connection.cursor()
        query = """
            SELECT HALL_ID, HALL_NAME, HALL_TYPE_CODE , NORMAL_CAPACITY , EXAM_CAPACITY FROM HAlLS WHERE HAll_TYPE_CODE = 'TEACHING'
        """
        cursor.execute(query)
        halls = []
        for row in cursor:
            hall_id = row[0]
            name = row[1] + " Hall"
            hall_type_code = row[2]
            normal_capacity = row[3]
            exam_capacity = row[4]


            # Create an instance of Halls
            hall = Halls(
                hall_id=hall_id,
                name=name,
                code=hall_type_code,
                normal_capacity=normal_capacity,
                exam_capacity=exam_capacity
            )
            halls.append(hall)
        cursor.close()
        return halls

        file_path = r'D:\Halls.xlsx' 
        halls = []
        columns  = [0,1,2,3,4,5]
        data_dict = self._reader.get_columns_from_xlsx(file_path, columns)
        num_rows = len(next(iter(data_dict.values())))
        for row_index in range(num_rows):
            row_data = {col_name: data_list[row_index] for col_name, data_list in data_dict.items()}
            if(row_data['type'] != "قاعة تدريس"):
                continue
            halls.append(Halls(hall_id=row_data['code'], name=row_data['code'],code=row_data['code'], description="Average Hall", normal_capacity=row_data['number_studernt_lecture']+row_data['increaselecture'], exam_capacity=row_data['number_student_exam']+row_data['increaseexam']))
        return halls
    
    def ReadCourses(self) :
        cursor = self.connection.cursor()
        query = """
        SELECT C.COURSE_ID, C.COURSE_CODE, C.COURSE_NAME_EN, C.COURSE_NAME_AR, C.DEFAULT_LECTURE_HOURS, C.DEFAULT_LAB_HOURS, C.SECTION_ID , COUNT(SSC.ACTUAL_COURSE_ID) AS STUDENT_COUNT
        FROM  COURSES C
        INNER JOIN STUDY_PLANS_COURSES E ON C.COURSE_ID = E.COURSE_ID
        INNER JOIN STUDY_PLAN_LEVEL_SEC S ON S.PLAN_LEVEL_SEC_ID = E.PLAN_LEVEL_SPEC_ID
        INNER JOIN COURSES_ACTIVITY_DETAILS A ON A.COURSE_ID = c.COURSE_ID
        LEFT JOIN  STUDENTS_SEMESTERS_COURSES SSC  ON C.COURSE_ID = SSC.ACTUAL_COURSE_ID   AND SSC.SEMESTER_ID = 77
        WHERE S.PLAN_ID >= 133 AND MOD(S.LEVEL_ID, 2) = 0 AND A.ACTIVITY_TYPE = 'LECTURE'
        GROUP BY C.COURSE_ID,  C.COURSE_CODE, C.COURSE_NAME_EN, C.COURSE_NAME_AR, C.DEFAULT_LECTURE_HOURS, C.DEFAULT_LAB_HOURS,C.SECTION_ID
        """
        cursor.execute(query)
        courses = []
        for row in cursor:
            course = Course(
                course_id=row[0],
                course_code=row[1],
                course_name=row[2],
                course_name_AR=row[3],
                lecture_hours=row[4],
                lab_hours=row[5],
                section_id=row[6],
                number_of_students= 29
            )
            courses.append(course)
        cursor.close()
        return courses

    def ReadStudyPlanLevel (self) :
        
        Plan_Level = []
        plan_level_sections_Level_id = {}

        cursor = self.connection.cursor()
        query = """
            SELECT
                PLAN_LEVEL_SEC_ID,
                PLAN_ID,
                SECTION_ID,
                LEVEL_ID
            FROM
                STUDY_PLAN_LEVEL_SEC
        """
        cursor.execute(query)
        for row in cursor:
            row_data = {
                'PLAN_LEVEL_SEC_ID': row[0],
                'PLAN_ID': int(row[1]),
                'SECTION_ID': row[2],
                'LEVEL_ID': int(row[3])
            }
            plan_level_sections_Level_id[row_data['PLAN_LEVEL_SEC_ID']] = [row_data['LEVEL_ID']]
            if row_data['PLAN_ID'] >= 133 and row_data['PLAN_ID'] <= 142  :
                Plan_Level.append(row_data)
        cursor.close()
        return Plan_Level, plan_level_sections_Level_id


        # Plan_Level = []
        # reader = ExcelReader()
        # file_path = r'D:\STUDY_PLAN_LEVEL_SEC.csv' 
        # columns = [0, 1, 2, 3]
        # data_Plan_Course = reader.get_columns_from_excel(file_path, columns)
        # num_rows = len(next(iter(data_Plan_Course.values())))

        # plan_level_sections_Level_id = {}

        # for row_index in range(num_rows):
        #     row_data = {col_name: data_list[row_index] for col_name, data_list in data_Plan_Course.items()}
        #     plan_level_sections_Level_id[row_data['PLAN_LEVEL_SEC_ID']] = [row_data['LEVEL_ID']]
        #     if(row_data['PLAN_ID']==141 and row_data['LEVEL_ID'] %2 ==1) :
        #         Plan_Level.append(row_data)
        # return Plan_Level , plan_level_sections_Level_id

    def ReadStudyPlanCourses (self,Plan_Level):

        cursor = self.connection.cursor()
        query = """
            SELECT E.PLAN_LEVEL_SPEC_ID, A.COURSE_ID
        FROM STUDY_PLAN_LEVEL_SEC S
        INNER JOIN STUDY_PLANS_COURSES E ON S.PLAN_LEVEL_SEC_ID = E.PLAN_LEVEL_SPEC_ID
        INNER JOIN COURSES_ACTIVITY_DETAILS A ON A.COURSE_ID = E.COURSE_ID
        WHERE S.PLAN_ID >= 133 AND MOD(S.LEVEL_ID, 2) = 0
        group BY E.PLAN_LEVEL_SPEC_ID, A.COURSE_ID
        """
        cursor.execute(query)
        Plan_Courses = []
        plan_courses_dict = {}

        plan_level_sec_ids = set(plan['PLAN_LEVEL_SEC_ID'] for plan in Plan_Level)
        for row in cursor:
            plan_level_spec_id = row[0]
            course_id = row[1]
            if plan_level_spec_id in plan_level_sec_ids:
                if plan_level_spec_id not in plan_courses_dict:
                    plan_courses_dict[plan_level_spec_id] = []
                plan_courses_dict[plan_level_spec_id].append(course_id)
        cursor.close()

        # Extract the list of courses
        Plan_Courses = list(plan_courses_dict.values())
        return Plan_Courses, plan_courses_dict



        # file_path = r'D:\STUDY_PLANS_COURSES.csv' 
        # columns = [ 1, 2]
        # reader = ExcelReader()
        # data_Plan_Course = reader.get_columns_from_excel(file_path, columns)
        # num_rows = len(next(iter(data_Plan_Course.values())))
        # Plan_Courses = []
        # plan_courses_dict = {}


        # for row_index in range(num_rows):
        #     row_data = {col_name: data_list[row_index] for col_name, data_list in data_Plan_Course.items()}
        #     if any(plan['PLAN_LEVEL_SEC_ID'] ==  row_data['PLAN_LEVEL_SPEC_ID'] for plan in Plan_Level) :
        #         plan_level_sec_id = row_data['PLAN_LEVEL_SPEC_ID']
        #         if plan_level_sec_id not in plan_courses_dict:
        #             plan_courses_dict[plan_level_sec_id] = []
        #         plan_courses_dict[plan_level_sec_id].append(row_data['COURSE_ID'])
        
        # for key,valu in plan_courses_dict.items() :
        #     Plan_Courses.append(valu)

        # return Plan_Courses , plan_courses_dict
    
    def ReadLabs(self):

        cursor = self.connection.cursor()
        query = """
            SELECT HALL_ID, HALL_NAME, HALL_TYPE_CODE , NORMAL_CAPACITY , EXAM_CAPACITY FROM HAlLS WHERE HAll_TYPE_CODE = 'LABORATORY'
        """
        cursor.execute(query)
        LabHallslist = []
        for row in cursor:
            hall_id = row[0] 
            name = row[1] 
            hall_type_code = row[2]
            normal_capacity = row[3]
            exam_capacity = row[4]


            labHall = Halls(
                hall_id=hall_id,
                name=name + " Lab",
                code=hall_type_code,
                normal_capacity=normal_capacity,
                exam_capacity=exam_capacity
            )
            LabHallslist.append(labHall)
        cursor.close()
        return LabHallslist


        # file_path = r'D:\SECTIONS.csv' 
        # columns = [0, 1]
        # reader = ExcelReader()
        # Sections = {}
        # Sections_names = reader.get_columns_from_excel(file_path, columns)
        # num_rows = len(next(iter(Sections_names.values())))
        # for row_index in range(num_rows):
        #     row_data = {col_name: data_list[row_index] for col_name, data_list in Sections_names.items()}
        #     Sections[row_data['SECTION_ID']]=row_data['SECTION_NAME_EN']
        # return Sections

    def getCourseEmployeeId(self):
        cursor = self.connection.cursor()
        query = """
        SELECT  A.COURSE_ID, A.EMPLOYEE_ID
        FROM COURSES C
        INNER JOIN COURSES_ACTIVITY_DETAILS A ON A.COURSE_ID = C.COURSE_ID
         WHERE A.ACTIVITY_TYPE = 'LECTURE'
        """


        cursor.execute(query)
        courseTeacher = []
        for row in cursor:
            COURSE_ID = row[0]
            EMPLOYEE_ID = row[1]


            # Create an instance of Halls
            courseteacher = CourseTeacherLink.CourseTeacherLink(
                course_id=COURSE_ID,
                teacher_id=EMPLOYEE_ID,
            )
            courseTeacher.append(courseteacher)
        cursor.close()
        return courseTeacher

        cursor.execute(query)
        result = cursor.fetchone()  # Fetch a single row
        cursor.close()
    
        if result:
            return result[0]  
        else:
             return 0 

    def getAvailableSection(self):
        cursor = self.connection.cursor()
        query = """
        SELECT C.COURSE_ID, C.COURSE_CODE, C.COURSE_NAME_EN, C.COURSE_NAME_AR, C.DEFAULT_LECTURE_HOURS, C.DEFAULT_LAB_HOURS, C.SECTION_ID , COUNT(SSC.ACTUAL_COURSE_ID) AS STUDENT_COUNT
        FROM  COURSES C
        INNER JOIN STUDY_PLANS_COURSES E ON C.COURSE_ID = E.COURSE_ID
        INNER JOIN STUDY_PLAN_LEVEL_SEC S ON S.PLAN_LEVEL_SEC_ID = E.PLAN_LEVEL_SPEC_ID
        INNER JOIN COURSES_ACTIVITY_DETAILS A ON A.COURSE_ID = c.COURSE_ID
        LEFT JOIN  STUDENTS_SEMESTERS_COURSES SSC  ON C.COURSE_ID = SSC.ACTUAL_COURSE_ID   AND SSC.SEMESTER_ID = 77
        WHERE S.PLAN_ID >= 133 AND MOD(S.LEVEL_ID, 2) = 0 AND A.ACTIVITY_TYPE = 'SECTION'
        GROUP BY C.COURSE_ID,  C.COURSE_CODE, C.COURSE_NAME_EN, C.COURSE_NAME_AR, C.DEFAULT_LECTURE_HOURS, C.DEFAULT_LAB_HOURS,C.SECTION_ID
        """
        cursor.execute(query)
        courses = []
        for row in cursor:
            course = Course(
                course_id=row[0],
                course_code=row[1],
                course_name=row[2] + " Section",
                course_name_AR=row[3],
                lecture_hours=row[4],
                lab_hours=row[5],
                section_id=row[6],
                number_of_students= 29,
                type=1
            )
            courses.append(course)
        cursor.close()
        return courses

    def getAvailableLab(self):
        cursor = self.connection.cursor()
        query = """
        SELECT C.COURSE_ID, C.COURSE_CODE, C.COURSE_NAME_EN, C.COURSE_NAME_AR, C.DEFAULT_LECTURE_HOURS, C.DEFAULT_LAB_HOURS, C.SECTION_ID , COUNT(SSC.ACTUAL_COURSE_ID) AS STUDENT_COUNT
        FROM  COURSES C
        INNER JOIN STUDY_PLANS_COURSES E ON C.COURSE_ID = E.COURSE_ID
        INNER JOIN STUDY_PLAN_LEVEL_SEC S ON S.PLAN_LEVEL_SEC_ID = E.PLAN_LEVEL_SPEC_ID
        INNER JOIN COURSES_ACTIVITY_DETAILS A ON A.COURSE_ID = c.COURSE_ID
        LEFT JOIN  STUDENTS_SEMESTERS_COURSES SSC  ON C.COURSE_ID = SSC.ACTUAL_COURSE_ID   AND SSC.SEMESTER_ID = 77
        WHERE S.PLAN_ID >= 133 AND MOD(S.LEVEL_ID, 2) = 0 AND A.ACTIVITY_TYPE = 'LABORATORY'
        GROUP BY C.COURSE_ID,  C.COURSE_CODE, C.COURSE_NAME_EN, C.COURSE_NAME_AR, C.DEFAULT_LECTURE_HOURS, C.DEFAULT_LAB_HOURS,C.SECTION_ID
        """
        cursor.execute(query)
        courses = []
        for row in cursor:
            course = Course(
                course_id=row[0],
                course_code=row[1] ,
                course_name=row[2] + " Lab",
                course_name_AR=row[3],
                lecture_hours=row[4],
                lab_hours=row[5],
                section_id=row[6],
                number_of_students= 29,
                type=2 
            )
            courses.append(course)
        cursor.close()
        return courses

    def getassistant(self):
        cursor = self.connection.cursor()
        query = """
            SELECT CAD.EMPLOYEE_ID,
            E.EMPLOYEE_NAME
            FROM COURSES_ACTIVITY_DETAILS CAD
            LEFT JOIN EMPLOYEES E
            ON CAD.EMPLOYEE_ID = E.EMPLOYEE_ID
            WHERE CAD.ACTIVITY_TYPE <> 'LECTURE'
            GROUP BY CAD.EMPLOYEE_ID , E.EMPLOYEE_NAME
        """
        cursor.execute(query)
        teachers = []
        for row in cursor:
            id = row[0]
            name = row[1]
            
            teachers.append(Teachers(name=name, emp_id=id, available_days=self.generate_available_days([1, 1, 1, 1, 1, 1]), emp_type="Full-time"))


        cursor.close()
        return teachers


    def getSectionEmployeeId(self):
        cursor = self.connection.cursor()
        query = """
        SELECT  A.COURSE_ID, A.EMPLOYEE_ID
        FROM COURSES C
        INNER JOIN COURSES_ACTIVITY_DETAILS A ON A.COURSE_ID = C.COURSE_ID
         WHERE A.ACTIVITY_TYPE <> 'LECTURE'
        """


        cursor.execute(query)
        courseTeacher = []
        for row in cursor:
            COURSE_ID = row[0]
            EMPLOYEE_ID = row[1]


            # Create an instance of Halls
            courseteacher = CourseTeacherLink.CourseTeacherLink(
                course_id=COURSE_ID,
                teacher_id=EMPLOYEE_ID,
            )
            courseTeacher.append(courseteacher)
        cursor.close()
        return courseTeacher