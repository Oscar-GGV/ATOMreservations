"""database.py
This file contains the Room and Hotel classes used to store the rooms,
room types, and other information about the hotel.

Programmer: Taksh Joshi
date of code: October 6th, 2025
modifications: Added a Room class and a Hotel class to store the rooms and their information
"""


class Room:
    """
    A room in the hotel with details like type, price, and availability.

    Attributes:
        room_id (int): A unique number for each room.
        room_type (str): The kind of room (e.g., "Single Room", "Double Room").
        beds (int): The number of beds in the room.
        max_guests (int): How many guests can stay in the room.
        price (float): The cost of the room per night.
        is_available (bool): Whether the room is available for booking.

    Methods:
        __init__(room_id, room_type, beds, max_guests, price):
            Sets up a new room with the given details.
    """

    def __init__(self, room_id, room_type, beds, max_guests, price):
        """
        Creates a room with the specified details.

        Args:
            room_id (int): A unique ID for the room.
            room_type (str): The type of room (e.g., "Single Room").
            beds (int): The number of beds in the room.
            max_guests (int): Maximum number of people allowed.
            price (float): Price per night.
        """
        self.room_id = room_id
        self.room_type = room_type
        self.beds = beds
        self.max_guests = max_guests
        self.price = price
        self.is_available = True


class Hotel:
    """
    A hotel that contains many rooms of different types.

    Attributes:
        rooms (list): A list of all Room objects in the hotel.

    Methods:
        __init__():
            Sets up the hotel with a set number of rooms.
    """

    def __init__(self):
        """
        Creates a hotel with different types of rooms. The hotel will start with:
        - 5 Single Rooms (for 2 guests, $100/night)
        - 10 Double Rooms (for 4 guests, $150/night)
        - 6 Family Rooms (for 6 guests, $200/night)
        - 3 VIP Suites (for 3 guests, $300/night)
        """
        self.rooms = []
        room_id = 101

        # Single Room - 5 rooms
        for _ in range(5):
            self.rooms.append(Room(room_id, "Single Room", 1, 2, 100))
            room_id += 1

        # Double Room - 10 rooms
        for _ in range(10):
            self.rooms.append(Room(room_id, "Double Room", 2, 4, 150))
            room_id += 1

        # Family Room - 6 rooms
        for _ in range(6):
            self.rooms.append(Room(room_id, "Family Room", 3, 6, 200))
            room_id += 1

        # VIP Suite - 3 rooms
        for _ in range(3):
            self.rooms.append(Room(room_id, "VIP Suite", 1, 3, 300))
            room_id += 1
