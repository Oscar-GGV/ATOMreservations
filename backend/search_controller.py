# search_controller.py
from reservation_system import ReservationSystem
from search import Search
class SearchController:
    def __init__(self):
        self.system = ReservationSystem() #initialize reservation system

    def search_available_rooms(self, search: Search):
        available_rooms = self.system.get_available_room_types(
            search.check_in_date,
            search.check_out_date,
            search.guests
        )
        return available_rooms
#gives the available rooms based on search criteria
