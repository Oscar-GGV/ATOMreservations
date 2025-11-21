"""models.py
This file contains core data models used across the Hotel Eleon booking system.
Includes singleton classes for storing booking details and customer information,
as well as room-related classes and an in-memory repository.

Programmers: Aatghik, Mahi
Date of code: October 28th, 2025

Description:
This file implements the Model layer of the MVC architecture. It uses the Singleton
pattern for BookingData and CustomerData to ensure only one instance exists throughout
the application, allowing all pages to access the same booking information. The
RoomRepository provides centralized access to available rooms using the Repository pattern.

Important Data Structures:
- BookingData stores: check_in (str), check_out (str), adults (int), selected_room (dict)
- CustomerData stores: first_name, last_name, email, phone, street, zip_code, 
  card_number, exp_date, cvv (all strings)
- Room stores: title (str), description (str)
- RoomRepository contains: _rooms (List[Room]) with 5 predefined rooms
"""

from datetime import datetime
from typing import Optional, Dict, List


class BookingData:
    """Singleton class that stores all temporary booking-related data during the
    reservation flow. This includes dates, number of adults, and selected room.
    
    The Singleton pattern ensures all pages access the same booking data without
    passing it between pages. When a user selects dates on the home page, those
    same dates appear on the room selection and checkout pages automatically.
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensures only one instance of BookingData is ever created.
        
        This method is called before __init__ and controls object creation.
        If an instance already exists, it returns that instance instead of
        creating a new one.
        
        Returns:
            BookingData: The single shared instance of this class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initializes booking data fields only once.
        
        The _initialized flag prevents reinitializing the data if __init__
        is called multiple times (which happens with singletons).
        """
        if self._initialized:
            return
        self._initialized = True
        
        self.check_in: Optional[str] = None
        self.check_out: Optional[str] = None
        self.adults: int = 1
        self.selected_room: Optional[Dict[str, str]] = None
    
    def calculate_nights(self) -> Optional[int]:
        """Calculates the number of nights between check-in and check-out dates.
        
        Uses Python's datetime module to parse date strings and calculate the
        difference. This is displayed on room selection, checkout, and confirmation pages.
        
        Input:
            Uses self.check_in and self.check_out (format: "YYYY-MM-DD")
        
        Returns:
            int: Number of nights if both dates are valid
            None: If either date is missing or dates are in invalid format
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
        """Resets all booking fields to their initial default state.
        
        This would be called when starting a new reservation, clearing all
        previously selected booking information.
        """
        self.check_in = None
        self.check_out = None
        self.adults = 1
        self.selected_room = None



class CustomerData:
    """Singleton class storing customer information used during checkout.
    
    Like BookingData, this uses the Singleton pattern so customer information
    entered on the checkout page is available on the confirmation page without
    passing it manually.
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensures a single shared instance of CustomerData.
        
        Returns:
            CustomerData: The single shared instance of this class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initializes customer details only once.
        
        Stores personal information, address, and payment details as strings.
        All fields start empty and are filled as user types in the checkout form.
        """
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
    """Represents a hotel room with a title and descriptive features.
    
    Simple data class that holds room information. The description is stored
    as a comma-separated string and can be split into individual features.
    """
    
    def __init__(self, title: str, description: str):
        """Creates a Room object.
        
        Parameters:
            title (str): Room name (e.g., "Ocean View Suite")
            description (str): Comma-separated room features (e.g., "2 Queen Beds, Ocean View")
        """
        self.title = title
        self.description = description
    
    def get_description_lines(self) -> List[str]:
        """Splits the comma-separated description into a clean list of features.
        
        This is used by RoomCard to display each feature as a separate bullet point.
        
        Returns:
            list of str: Individual description parts with whitespace removed
        """
        return [part.strip() for part in self.description.split(',')]



class RoomRepository:
    """Simple in-memory repository containing all room definitions.
    
    Uses the Repository pattern to centralize room data access. All rooms are
    stored in a class-level list, so they're shared across all instances.
    In a real application, this would connect to a database instead.
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
        """Returns a list of all predefined Room objects.
        
        Called by RoomSelectionPage to get rooms for display. Using a class method
        means we don't need to create an instance of RoomRepository.
        
        Returns:
            List[Room]: All 5 available rooms
        """
        return cls._rooms