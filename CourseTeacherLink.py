import Courses 
import Teachers 

class CourseTeacherLink:
    def __init__(self, course_id, teacher_id):
        self._course_id = course_id
        self._teacher_id = teacher_id

    # Getter methods
    def get_course_id(self):
        return self._course_id

    def get_teacher_id(self):
        return self._teacher_id

    # Setter methods
    def set_course_id(self, course_id):
        self._course_id = course_id

    def set_teacher_id(self, teacher_id):
        self._teacher_id = teacher_id

    def __str__(self):
        return f"CourseTeacherLink(Course ID: {self._course_id}, Teacher ID: {self._teacher_id})"

