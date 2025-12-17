
"""search.py
This file contains the Search class which represents a search query in the hotel reservation system.
Programmer: Oscar Guevara
date of code: November 5th, 2025"""
class Search:
    """Represents a search query in the hotel reservation system."""
    def __init__(self, check_in_date, check_out_date, num_guests):
        """Initializes a Search object with the given parameters.
            parameters:
            check_in_date (tuple): The check-in date for the search.
            check_out_date (tuple): The check-out date for the search.
            guests (int): The number of guests for the search."""
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.num_guests = num_guests
