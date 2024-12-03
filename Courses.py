class Course:
    def __init__(self, course_id, course_code, course_name, course_name_AR, lecture_hours, lab_hours, section_id , number_of_students,type = 0):
        self._course_id = course_id
        self._course_code = course_code
        self._course_name = course_name
        self._lecture_hours = lecture_hours
        self._section_id = section_id
        self._course_name_AR = course_name_AR
        self._lab_hours = lab_hours
        self._number_of_students = number_of_students
        self._type = type 

    def get_course_id(self):
        return self._course_id

    def get_course_name_Ar(self):
        return self._course_name_AR
    
    def get_course_code(self):
        return self._course_code

    def get_course_name(self):
        return self._course_name

    def get_lecture_hours(self):
        return self._lecture_hours

    def get_lab_hours(self):
        return self._lab_hours

    def get_section_id(self):
        return self._section_id

    def get_number_of_students(self):
        return self._number_of_students

    def set_course_id(self, course_id):
        self._course_id = course_id

    def set_course_code(self, course_code):
        self._course_code = course_code

    def set_course_name(self, course_name):
        self._course_name = course_name

    def set_lecture_hours(self, lecture_hours):
        self._lecture_hours = lecture_hours

    def set_lab_hours(self, lab_hours):
        self._lab_hours = lab_hours

    def set_section_id(self, section_id):
        self._section_id = section_id

    def set_type(self,type):
        self._type=type
    
    def get_type(self):
        return self._type

    def set_number_of_students(self, number_of_students):
        self._number_of_students = number_of_students

    def __str__(self):
        return (f"Course ID: {self._course_id}, Course Code: {self._course_code}, Course Name: {self._course_name}, "
                f"Lecture Hours: {self._lecture_hours}, Lab Hours: {self._lab_hours}, Section ID: {self._section_id}, "
                
                f"Number of Students: {self._number_of_students}")
