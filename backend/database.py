# database.py
"""
room_database = [
    {"name": "Single Room", "max_guests": 2, "features": ["1 Queen Bed", "Free WiFi", "Mini Fridge", "TV"], "quantity": 5, "price": 100},
    {"name": "Double Room", "max_guests": 4, "features": ["2 Queen Beds", "Free WiFi", "Mini Fridge", "TV"], "quantity": 10, "price": 150},
    {"name": "Family Room", "max_guests": 6, "features": ["2 Queen Beds", "Sofa-bed", "WiFi", "Crib Available"], "quantity": 6, "price": 200},
    {"name": "VIP Suite", "max_guests": 3, "features": ["King Bed", "Living Area", "Balcony", "TV", "WiFi"], "quantity": 3, "price": 300},
]
"""
class Room:
    def __init__(self, room_id, room_type, beds, max_guests, price):
        self.room_id = room_id
        self.room_type = room_type
        self.beds = beds
        self.max_guests = max_guests
        self.price = price
        self.is_available = True  #See if room is booked


class Hotel:
    def __init__(self):
        self.rooms = []
        room_id = 101

        # Single Room - 5 rooms (max 2 guests, $100/night)
        for i in range(5):
            self.rooms.append(Room(room_id, "Single Room", 1, 2, 100))
            room_id += 1

        # Double Room - 10 rooms (max 4 guests, $150/night)
        for i in range(10):
            self.rooms.append(Room(room_id, "Double Room", 2, 4, 150))
            room_id += 1

        # Family Room - 6 rooms (max 6 guests, $200/night)
        for i in range(6):
            self.rooms.append(Room(room_id, "Family Room", 3, 6, 200))
            room_id += 1

        # VIP Suite - 3 rooms (max 3 guests, $300/night)
        for i in range(3):
            self.rooms.append(Room(room_id, "VIP Suite", 1, 3, 300))
            room_id += 1
// Test change
#This a comment