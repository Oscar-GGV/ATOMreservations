
"""search.py
This file contains the Search class which represents a search query in the hotel reservation system.
Programmer: Oscar Guevara
date of code: November 5th, 2025"""
from backend.address import dayNode
from backend.address import monthNode
class Search:
    """Represents a search query in the hotel reservation system."""
    def __init__(self, check_in_date, check_out_date, room_type, guests):
        """Initializes a Search object with the given parameters.
            parameters:
            check_in_date (str): The check-in date for the search.
            check_out_date (str): The check-out date for the search.
            room_type (str): The type of room being searched for.
            guests (int): The number of guests for the search."""
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.room_type = room_type
        self.guests = guests
