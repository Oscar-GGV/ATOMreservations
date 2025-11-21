"""models.py
This file contains all the data classes used throughout the booking system.
It stores booking information, customer details, and room data.

Programmers: Astghik, Mahi
Date of code: October 28th, 2025

Description:
This file holds the data that gets shared between all pages. BookingData stores the
dates, guests, and selected room. CustomerData stores the customer's personal info.
Room is a simple class for room information, and RoomRepository holds all available
rooms. These classes make sure all pages can access the same booking information
without passing it around manually.

Data stored:
- BookingData: check_in, check_out, adults, selected_room
- CustomerData: first_name, last_name, email, phone, street, zip_code, card_number, exp_date, cvv
- Room: title, description
- RoomRepository: list of all rooms
"""

from datetime import datetime
from typing import Optional, Dict, List


class BookingData:
    """Stores all booking information that gets shared across pages.
    Only one copy of this exists in the whole application so all pages see the same data.
    """
    
    _instance = None
    
    def __new__(cls):
        """Makes sure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Sets up the booking fields with default values."""
        if self._initialized:
            return
        self._initialized = True
        
        self.check_in: Optional[str] = None
        self.check_out: Optional[str] = None
        self.adults: int = 1
        self.selected_room: Optional[Dict[str, str]] = None
    
    def calculate_nights(self) -> Optional[int]:
        """Calculates how many nights between check-in and check-out.
        
        Takes the two date strings, converts them to date objects, and finds
        the difference in days. Returns None if dates are missing or invalid.
        
        Returns:
            Number of nights, or None if can't calculate
        """
        if not self.check_in or not self.check_out:
            return None
        
        try:
            d1 = datetime.strptime(self.check_in, "%Y-%m-%d")
            d2 = datetime.strptime(self.check_out, "%Y-%m-%d")
            return (d2 - d1).days
        except ValueError:
            return None
    
    def reset(self):
        """Clears all booking data back to defaults."""
        self.check_in = None
        self.check_out = None
        self.adults = 1
        self.selected_room = None



class CustomerData:
    """Stores customer information entered during checkout.
    Only one copy exists so checkout and confirmation pages see the same data.
    """
    
    _instance = None
    
    def __new__(cls):
        """Makes sure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Sets up all customer fields as empty strings."""
        if self._initialized:
            return
        self._initialized = True
        
        self.first_name: str = ""
        self.last_name: str = ""
        self.email: str = ""
        self.phone: str = ""
        
        self.street: str = ""
        self.zip_code: str = ""
        
        self.card_number: str = ""
        self.exp_date: str = ""
        self.cvv: str = ""



class Room:
    """Simple class that holds information about one room."""
    
    def __init__(self, title: str, description: str):
        """Creates a room with a name and features.
        
        Parameters:
            title: Room name like "Ocean View Suite"
            description: Features separated by commas
        """
        self.title = title
        self.description = description
    
    def get_description_lines(self) -> List[str]:
        """Splits the description into separate lines for display.
        
        Returns:
            List of individual features
        """
        return [part.strip() for part in self.description.split(',')]



class RoomRepository:
    """Holds all the rooms available in the hotel.
    This is where all room data is stored in the application.
    This is temperaraly was made to do testing, the actual data with more infromaton was done by backend
    """
    
    _rooms: List[Room] = [
        Room("Ocean View Suite", "2 Queen Beds, Ocean View, Breakfast Included, Sleeps 4"),
        Room("City View Deluxe", "1 King Bed, City View, Free Wi-Fi, Sleeps 2"),
        Room("Family Room", "2 Double Beds, Garden View, Extra Sofa Bed, Sleeps 5"),
        Room("Penthouse", "1 King Bed, Private Balcony, Full Kitchen, Sleeps 2"),
        Room("Economy Room", "1 Full Bed, No View, No Breakfast, Sleeps 1")
    ]
    
    @classmethod
    def get_all_rooms(cls) -> List[Room]:
        """Returns the list of all available rooms.
        
        Returns:
            List of all 5 rooms
        """
        return cls._rooms