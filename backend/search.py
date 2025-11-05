#Search class, takes in check-in and check-out dates, room type, and number of guests
from backend.address import dayNode
from backend.address import monthNode
class Search:
    def __init__(self, check_in_date, check_out_date, room_type, guests):
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.room_type = room_type
        self.guests = guests
    
