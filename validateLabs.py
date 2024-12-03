from LabHalls import LabHall

class ValidationLabs:
    def __init__(self, labs):
        self.labs = labs  # List of LabHall objects
        self.lab_availability = [0] * len(labs)  
        

    def find_valid_lab(self, required_capacity, day, hours):
        valid_labs = []
        min_capacity = float('inf')  
        selected_lab = None

        for idx, lab in enumerate(self.labs):
            if (lab.get_normal_capacity() >= required_capacity and
                lab.is_hall_available(day, hours) ):  # Only consider labs that are available
                if lab.get_normal_capacity() < min_capacity:
                    valid_labs.clear()
                    valid_labs.append(lab)
                    min_capacity = lab.get_normal_capacity()
                    selected_lab = lab
        if selected_lab:
            lab_index = self.labs.index(selected_lab)
            # self.lab_availability[lab_index] = 1 
            return selected_lab
        else:
            return None  

    def reset_valid_lab(self, lab):
        lab_index = self.labs.index(lab)
        self.lab_availability[lab_index] = 0  

    def get_lab_availability(self):
        return self.lab_availability

    def get_labs(self):
        return self.labs

    def get_lab_by_id(self, lab_id):
        for lab in self.labs:
            if lab.get_hall_id() == lab_id:
                return lab
        return None
