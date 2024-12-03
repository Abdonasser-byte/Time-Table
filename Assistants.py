from Employees import Employees


class Assistant(Employees):
    def __init__(self, name, emp_id, available_days, emp_type):
        super().__init__(name, emp_id, available_days, emp_type)

    def __str__(self):
        return super().__str__() 
    

