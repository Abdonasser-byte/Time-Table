from Halls import Halls

class ValidationHalls:
    def __init__(self, halls):
        self.halls = halls
        self.hall_availability = [0] * len(halls)

    def find_valid_hall(self, required_capacity, day, hours):
        valid_halls = []
        num = 200
        idx = 0
        endhall = -1
        for hall in self.halls:
            idx += 1
            if (  
                hall.is_hall_available(day, hours) and num>hall.get_normal_capacity()):
                valid_halls.clear()
                valid_halls.append(hall)
                num = hall.get_normal_capacity()
                endhall = idx
        
        if endhall != -1:
            self.hall_availability[endhall - 1] = 1
            return valid_halls[0]
        else : 
            return None
    
    def get_hall_availability(self):
        return self.hall_availability
    
    def reset_valid_hall(self, hall ):
        idx = 0
        endhall = -1 
        for currhall in self.halls:
            idx+=1
            if currhall.get_hall_id() == hall.get_hall_id() :
                endhall=idx
        self.hall_availability[endhall-1]=0  

    def get_halls(self):
        return self.halls
    
    def get_hall_by_id(self, hall_id):
        for hall in self.halls:
            if hall.get_hall_id() == hall_id:
                return hall
        return None

    
# # Creating halls
# hall1 = Halls(1, "H101", "Main Hall", 200, 250)
# hall2 = Halls(2, "H102", "Secondary Hall", 150, 180)
# hall3 = Halls(3, "H103", "Small Hall", 100, 60)
# halls = [hall1, hall2, hall3]

# # Creating validation instance
# validation = ValidationHalls(halls)

# # Example usage: finding valid halls for a required capacity
# required_capacity = 100
# day = "Monday"
# hours = ["8:30", "9:30"]
# valid_halls = validation.find_valid_hall(required_capacity, day, hours)
# hall=valid_halls
# print("Valid Halls for required capacity of", required_capacity, "or more and available on", day, "at", hours)
# print("Hall ID:", hall.get_hall_id(), "Code:", hall.get_code(), "Description:", hall.get_description())

# # Example usage: checking hall availability after taking a hall
# print("\nHall availability after taking a hall:")
# for hall_id, availability in enumerate(validation.get_hall_availability()):
#     print(f"Hall ID: {hall_id + 1}, Available: {'Yes' if availability == 0 else 'No'}")

# # Example usage: resetting availability of a hall
# validation.reset_valid_hall(valid_halls)
