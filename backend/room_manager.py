"""room_manager.py
This file contains the RoomManager class which handles all operations related to rooms in the hotel reservation system
Programmer: Taksh Joshi
date of code: November 5th, 2025
modifications: Added functions to manage room availability, cleanliness, and statistics
"""
from backend.database import Hotel, Room
from backend.calendar import get_booked_quantity

class RoomManager:
    """
    Manages all hotel room operations including availability, cleanliness,
    searching, booking readiness, revenue calculations, and room statistics.
    """
    def __init__(self):
        """
        Initialize the RoomManager with a Hotel instance.
        All rooms start with a default cleanliness status of "clean".
        """
        self.hotel = Hotel()
        # Initialize all rooms as clean
        self.room_cleanliness = {}  # {room_id: "clean" or "dirty"}
        for room in self.hotel.rooms:
            self.room_cleanliness[room.room_id] = "clean"

    def get_all_rooms(self):
        """Return a list of all rooms in the hotel."""
        return self.hotel.rooms

    def get_rooms_by_type(self, room_type):
        """
        Return all rooms of a given type.
        Args:
            room_type (str): The requested room type.
        Returns:
            list[Room]: Matching rooms.
        """
        return [room for room in self.hotel.rooms if room.room_type == room_type]

    def get_available_rooms(self):
        """Return all rooms that are currently available (not booked)."""
        return [room for room in self.hotel.rooms if room.is_available]

    def get_available_rooms_by_type(self, room_type):
        """
        Return available rooms filtered by type.
        Args:
            room_type (str): Target room type.
        Returns:
            list[Room]: Available rooms of that type.
        """
        return [room for room in self.hotel.rooms if room.room_type == room_type and room.is_available]

    def get_room_by_id(self, room_id):
        """
        Retrieve a room object by its ID.
        Args:
            room_id (int): ID of the room.
        Returns:
            Room | None: Room instance if found, else None.
        """
        for room in self.hotel.rooms:
            if room.room_id == room_id:
                return room
        return None

    def mark_room_unavailable(self, room_id):
        """
        Mark a room as booked/unavailable.
        Args:
            room_id (int): Room ID.
        Returns:
            bool: True if successful, False if room not found.
        """
        room = self.get_room_by_id(room_id)
        if room:
            room.is_available = False
            return True
        return False

    def mark_room_available(self, room_id):
        """
        Mark a room as available.
        Args:
            room_id (int): Room ID.
        Returns:
            bool: True if successful, False otherwise.
        """
        room = self.get_room_by_id(room_id)
        if room:
            room.is_available = True
            return True
        return False

    def mark_room_dirty(self, room_id):
        """
        Mark a room as dirty (requires cleaning).
        Args:
            room_id (int): Room ID.
        Returns:
            tuple(bool, str): Status and message.
        """
        room = self.get_room_by_id(room_id)
        if room:
            self.room_cleanliness[room_id] = "dirty"
            return True, f"Room {room_id} marked as dirty"
        return False, f"Room {room_id} not found"

    def mark_room_clean(self, room_id):
        """
        Mark a room as clean after housekeeping.
        Args:
            room_id (int): Room ID.
        Returns:
            tuple(bool, str): Status and message.
        """
        room = self.get_room_by_id(room_id)
        if room:
            self.room_cleanliness[room_id] = "clean"
            return True, f"Room {room_id} marked as clean"
        return False, f"Room {room_id} not found"

    def get_room_cleanliness(self, room_id):
        """
        Get the cleanliness status of a room.
        Args:
            room_id (int): Room ID.
        Returns:
            str: "clean", "dirty", or "unknown".
        """
        if room_id in self.room_cleanliness:
            return self.room_cleanliness[room_id]
        return "unknown"

    def get_dirty_rooms(self):
        """Get all rooms that need cleaning"""
        dirty_rooms = []
        for room in self.hotel.rooms:
            if self.room_cleanliness.get(room.room_id) == "dirty":
                dirty_rooms.append(room)
        return dirty_rooms

    def get_clean_rooms(self):
        """Get all clean rooms"""
        clean_rooms = []
        for room in self.hotel.rooms:
            if self.room_cleanliness.get(room.room_id) == "clean":
                clean_rooms.append(room)
        return clean_rooms

    def get_clean_available_rooms(self):
        """
        Get all rooms that are both available and clean (ready for booking).
        Returns:
            list[Room]: Clean and available rooms.
        """
        return [room for room in self.hotel.rooms 
                if room.is_available and self.room_cleanliness.get(room.room_id) == "clean"]

    def get_dirty_rooms_count(self):
        """Count how many rooms need cleaning"""
        return len(self.get_dirty_rooms())

    def get_clean_rooms_count(self):
        """Count how many rooms are clean"""
        return len(self.get_clean_rooms())

    def get_housekeeping_status(self):
        """
        Return summary statistics for housekeeping.
        Returns:
            dict: Includes totals, clean/dirty counts, and percentages.
        """
        total = len(self.hotel.rooms)
        dirty = self.get_dirty_rooms_count()
        clean = self.get_clean_rooms_count()

        return {
            "total_rooms": total,
            "clean_rooms": clean,
            "dirty_rooms": dirty,
            "clean_percentage": round((clean / total * 100), 2) if total > 0 else 0,
            "dirty_percentage": round((dirty / total * 100), 2) if total > 0 else 0
        }

    def checkout_and_mark_dirty(self, room_id):
        """
        Mark a room as available but dirty upon guest checkout.
        Args:
            room_id (int): Room ID.
        Returns:
            tuple(bool, str): Status and message.
        """
        room = self.get_room_by_id(room_id)
        if room:
            room.is_available = True
            self.room_cleanliness[room_id] = "dirty"
            return True, f"Room {room_id} checked out and marked for cleaning"
        return False, f"Room {room_id} not found"

    def get_rooms_by_cleanliness_type(self, room_type, cleanliness_status):
        """
        Retrieve rooms filtered by type and cleanliness.
        Args:
            room_type (str): Room type.
            cleanliness_status (str): "clean" or "dirty".
        Returns:
            list[Room]: Matching rooms.
        """
        rooms = self.get_rooms_by_type(room_type)
        return [room for room in rooms 
                if self.room_cleanliness.get(room.room_id) == cleanliness_status]

    def get_room_types_summary(self):
        """
        Return a summary of room types including availability, cleanliness,
        pricing, and bed capacity.
        Returns:
            dict: A dictionary keyed by room type.
        """
        room_types = {}
        for room in self.hotel.rooms:
            if room.room_type not in room_types:
                room_types[room.room_type] = {
                    "total": 0,
                    "available": 0,
                    "booked": 0,
                    "clean": 0,
                    "dirty": 0,
                    "price": room.price,
                    "max_guests": room.max_guests,
                    "beds": room.beds
                }
            room_types[room.room_type]["total"] += 1
            if room.is_available:
                room_types[room.room_type]["available"] += 1
            else:
                room_types[room.room_type]["booked"] += 1

            if self.room_cleanliness.get(room.room_id) == "clean":
                room_types[room.room_type]["clean"] += 1
            else:
                room_types[room.room_type]["dirty"] += 1

        return room_types

    def check_availability_for_dates(self, room_type, check_in, check_out, calendar_head):
        """
        Check date-based availability for a room type using the calendar system.
        Args:
            room_type (str): Type of room.
            check_in (tuple[int, int]): (month, day)
            check_out (tuple[int, int]): (month, day)
            calendar_head: Calendar node reference.
        Returns:
            tuple(bool, str): Availability status and explanation.
        """
        rooms_of_type = self.get_rooms_by_type(room_type)
        total_rooms = len(rooms_of_type)

        month, day = check_in
        end_month, end_day = check_out

        room_type_dict = {
            "name": room_type,
            "quantity": total_rooms
        }

        while True:
            booked = get_booked_quantity(month, day, room_type_dict, calendar_head)
            if booked >= total_rooms:
                return False, f"No {room_type} available on {month}/{day}"

            if (month, day) == (end_month, end_day):
                break

            day += 1
            if day > 30:
                day, month = 1, month + 1

        return True, f"{total_rooms - booked} {room_type}(s) available"

    def get_available_room_for_booking(self, room_type):
        """
        Retrieve the first room of a given type that is both clean and available.
        Args:
            room_type (str): Room type.
        Returns:
            Room | None: A room ready for booking.
        """
        available_clean_rooms = [room for room in self.hotel.rooms 
                                if room.room_type == room_type 
                                and room.is_available 
                                and self.room_cleanliness.get(room.room_id) == "clean"]
        if available_clean_rooms:
            return available_clean_rooms[0]
        return None

    def get_room_info(self, room_id):
        """
        Return detailed information about a room.
        Args:
            room_id (int): Room ID.
        Returns:
            dict | None: Room details or None if not found.
        """
        room = self.get_room_by_id(room_id)
        if room:
            return {
                "room_id": room.room_id,
                "room_type": room.room_type,
                "beds": room.beds,
                "max_guests": room.max_guests,
                "price": room.price,
                "is_available": room.is_available,
                "cleanliness": self.room_cleanliness.get(room.room_id, "unknown"),
                "status": "Available" if room.is_available else "Booked",
                "ready_for_booking": room.is_available and self.room_cleanliness.get(room.room_id) == "clean"
            }
        return None

    def search_rooms(self, min_price=None, max_price=None, min_guests=None, available_only=True, clean_only=False):
        """
        Search rooms with multiple filters.
        Args:
            min_price (float | None): Minimum room price.
            max_price (float | None): Maximum room price.
            min_guests (int | None): Minimum guest capacity.
            available_only (bool): Only include available rooms.
            clean_only (bool): Only include clean rooms.
        Returns:
            list[Room]: Filtered room list.
        """
        results = self.hotel.rooms

        if available_only:
            results = [room for room in results if room.is_available]

        if clean_only:
            results = [room for room in results if self.room_cleanliness.get(room.room_id) == "clean"]

        if min_price is not None:
            results = [room for room in results if room.price >= min_price]

        if max_price is not None:
            results = [room for room in results if room.price <= max_price]

        if min_guests is not None:
            results = [room for room in results if room.max_guests >= min_guests]

        return results

    def get_total_rooms_count(self):
        """Get total number of rooms in hotel"""
        return len(self.hotel.rooms)

    def get_occupancy_rate(self):
        """Calculate current occupancy rate"""
        total = len(self.hotel.rooms)
        booked = len([room for room in self.hotel.rooms if not room.is_available])
        if total == 0:
            return 0
        return (booked / total) * 100

    def get_revenue_potential(self):
        """
        Calculate the maximum possible daily revenue if all rooms are booked.
        Returns:
            float: Potential revenue.
        """
        return sum(room.price for room in self.hotel.rooms)

    def get_current_revenue(self):
        """
        Calculate revenue from currently booked rooms.
        Returns:
            float: Revenue.
        """
        return sum(room.price for room in self.hotel.rooms if not room.is_available)

    def get_rooms_by_price_range(self, min_price, max_price):
        """
        Retrieve rooms within a price range.
        Args:
            min_price (float): Minimum price.
            max_price (float): Maximum price.
        Returns:
            list[Room]: Rooms within the range.
        """
        return [room for room in self.hotel.rooms 
                if min_price <= room.price <= max_price]

    def get_cheapest_available_room(self):
        """Get the cheapest available room"""
        available = self.get_available_rooms()
        if not available:
            return None
        return min(available, key=lambda room: room.price)

    def get_most_expensive_available_room(self):
        """Get the most expensive available room"""
        available = self.get_available_rooms()
        if not available:
            return None
        return max(available, key=lambda room: room.price)

    def reset_all_rooms(self):
        """
        Reset all rooms to available status.
        Returns:
            bool: Always True.
        """
        for room in self.hotel.rooms:
            room.is_available = True
        return True

    def get_room_statistics(self):
        """
        Return comprehensive room and hotel statistics including availability,
        cleanliness, revenue, occupancy, and room type summaries.
        Returns:
            dict: Statistics about hotel rooms.
        """
        stats = {
            "total_rooms": self.get_total_rooms_count(),
            "available_rooms": len(self.get_available_rooms()),
            "booked_rooms": len([r for r in self.hotel.rooms if not r.is_available]),
            "clean_rooms": self.get_clean_rooms_count(),
            "dirty_rooms": self.get_dirty_rooms_count(),
            "clean_and_available": len(self.get_clean_available_rooms()),
            "occupancy_rate": round(self.get_occupancy_rate(), 2),
            "potential_revenue": self.get_revenue_potential(),
            "current_revenue": self.get_current_revenue(),
            "room_types": self.get_room_types_summary(),
            "housekeeping_status": self.get_housekeeping_status()
        }
        return stats