"""models.py
This file contains core data models used across the Hotel Eleon booking system.
Includes singleton classes for storing booking details and customer information,
as well as room-related classes and an in-memory repository.
Programmers: 
date of code: November th, 2025
"""

from datetime import datetime
from typing import Optional, Dict, List


class BookingData:
    """Singleton class that stores all temporary booking-related data during the
    reservation flow. This includes dates, number of adults, and selected room."""
    
    _instance = None
    
    def __new__(cls):
        """Ensures only one instance of BookingData is ever created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initializes booking data fields only once."""
        if self._initialized:
            return
        self._initialized = True
        
        self.check_in: Optional[str] = None
        self.check_out: Optional[str] = None
        self.adults: int = 1
        self.selected_room: Optional[Dict[str, str]] = None
    
    def calculate_nights(self) -> Optional[int]:
        """Calculates the number of nights between check-in and check-out dates.
        Returns:
            int or None: Number of nights, or None if dates are missing or invalid.
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
        """Resets all booking fields to their initial default state."""
        self.check_in = None
        self.check_out = None
        self.adults = 1
        self.selected_room = None



class CustomerData:
    """Singleton class storing customer information used during checkout."""
    
    _instance = None
    
    def __new__(cls):
        """Ensures a single shared instance of CustomerData."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initializes customer details only once."""
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
    """Represents a hotel room with a title and descriptive features."""
    
    def __init__(self, title: str, description: str):
        """Creates a Room object.
        Parameters:
            title (str): Room name.
            description (str): Comma-separated room features.
        """
        self.title = title
        self.description = description
    
    def get_description_lines(self) -> List[str]:
        """Splits the comma-separated description into a clean list of features.
        Returns:
            list of str: Individual description parts.
        """
        return [part.strip() for part in self.description.split(',')]



class RoomRepository:
    """Simple in-memory repository containing all room definitions."""
    
    _rooms: List[Room] = [
        Room("Ocean View Suite", "2 Queen Beds, Ocean View, Breakfast Included, Sleeps 4"),
        Room("City View Deluxe", "1 King Bed, City View, Free Wi-Fi, Sleeps 2"),
        Room("Family Room", "2 Double Beds, Garden View, Extra Sofa Bed, Sleeps 5"),
        Room("Penthouse", "1 King Bed, Private Balcony, Full Kitchen, Sleeps 2"),
        Room("Economy Room", "1 Full Bed, No View, No Breakfast, Sleeps 1")
    ]
    
    @classmethod
    def get_all_rooms(cls) -> List[Room]:
        """Returns a list of all predefined Room objects."""
        return cls._rooms
