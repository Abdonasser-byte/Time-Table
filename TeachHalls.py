from Halls import Halls


class TeachingHall(Halls):
    def __init__(self, hall_id, code, description, normal_capacity, exam_capacity):
        super().__init__(hall_id, code, description, normal_capacity, exam_capacity)
    
    def __str__(self):
        return (super().__str__() )

