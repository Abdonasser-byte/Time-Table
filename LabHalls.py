
from Halls import Halls


class LabHall(Halls):
    def __init__(self, hall_id,name, code, normal_capacity, exam_capacity):
        super().__init__( hall_id,name, code, normal_capacity, exam_capacity)

    def __str__(self):
        return (super().__str__() )

