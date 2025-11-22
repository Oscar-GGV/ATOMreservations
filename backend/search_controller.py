"""search_controller.py
This file contains the SearchController class which manages search operations in the hotel reservation system.
Programmer: Oscar Guevara
date of code: November 5th, 2025"""
from backend.reservation_system import ReservationSystem
from backend.search import Search
class SearchController:
    """Controller for handling search operations in the reservation system."""
    def __init__(self):
        """Initializes the SearchController with a ReservationSystem instance."""
        self.system = ReservationSystem() #initialize reservation system

    def search_available_rooms(self, search: Search):
        """Searches for available room types based on the search criteria.
        Parameters:
            search (Search): The search criteria including check-in date, check-out date, and number of guests.
        Returns:
            list: A list of available room types that match the search criteria."""
        available_rooms = self.system.get_available_room_types(
            search.check_in_date,
            search.check_out_date,
            search.guests
        )
        return available_rooms
#gives the available rooms based on search criteria
