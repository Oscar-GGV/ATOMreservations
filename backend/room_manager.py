# room_manager.py

from backend.database import Hotel, Room
from backend.calendar import get_booked_quantity

class RoomManager:
    def __init__(self):
        self.hotel = Hotel()
    
    def get_all_rooms(self):
        """Get all rooms in the hotel"""
        return self.hotel.rooms
    
    def get_rooms_by_type(self, room_type):
        """Get all rooms of a specific type"""
        return [room for room in self.hotel.rooms if room.room_type == room_type]
    
    def get_available_rooms(self):
        """Get all available rooms"""
        return [room for room in self.hotel.rooms if room.is_available]
    
    def get_available_rooms_by_type(self, room_type):
        """Get available rooms of a specific type"""
        return [room for room in self.hotel.rooms if room.room_type == room_type and room.is_available]
    
    def get_room_by_id(self, room_id):
        """Get a specific room by ID"""
        for room in self.hotel.rooms:
            if room.room_id == room_id:
                return room
        return None
    
    def mark_room_unavailable(self, room_id):
        """Mark a room as unavailable (booked)"""
        room = self.get_room_by_id(room_id)
        if room:
            room.is_available = False
            return True
        return False
    
    def mark_room_available(self, room_id):
        """Mark a room as available (checkout)"""
        room = self.get_room_by_id(room_id)
        if room:
            room.is_available = True
            return True
        return False
    
    def get_room_types_summary(self):
        """Get summary of all room types with counts and availability"""
        room_types = {}
        for room in self.hotel.rooms:
            if room.room_type not in room_types:
                room_types[room.room_type] = {
                    "total": 0,
                    "available": 0,
                    "booked": 0,
                    "price": room.price,
                    "max_guests": room.max_guests,
                    "beds": room.beds
                }
            room_types[room.room_type]["total"] += 1
            if room.is_available:
                room_types[room.room_type]["available"] += 1
            else:
                room_types[room.room_type]["booked"] += 1
        return room_types
    
    def check_availability_for_dates(self, room_type, check_in, check_out, calendar_head):
        """Check if rooms of a specific type are available for given dates"""
        rooms_of_type = self.get_rooms_by_type(room_type)
        total_rooms = len(rooms_of_type)
        
        month, day = check_in
        end_month, end_day = check_out
        
        # Define room type dict for calendar lookup
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
        """Get the first available room of a specific type for booking"""
        available_rooms = self.get_available_rooms_by_type(room_type)
        if available_rooms:
            return available_rooms[0]
        return None
    
    def get_room_info(self, room_id):
        """Get detailed information about a specific room"""
        room = self.get_room_by_id(room_id)
        if room:
            return {
                "room_id": room.room_id,
                "room_type": room.room_type,
                "beds": room.beds,
                "max_guests": room.max_guests,
                "price": room.price,
                "is_available": room.is_available,
                "status": "Available" if room.is_available else "Booked"
            }
        return None
    
    def search_rooms(self, min_price=None, max_price=None, min_guests=None, available_only=True):
        """Search rooms with filters"""
        results = self.hotel.rooms
        
        if available_only:
            results = [room for room in results if room.is_available]
        
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
        """Calculate potential daily revenue if all rooms are booked"""
        return sum(room.price for room in self.hotel.rooms)
    
    def get_current_revenue(self):
        """Calculate current daily revenue from booked rooms"""
        return sum(room.price for room in self.hotel.rooms if not room.is_available)
    
    def get_rooms_by_price_range(self, min_price, max_price):
        """Get rooms within a specific price range"""
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
        """Reset all rooms to available status"""
        for room in self.hotel.rooms:
            room.is_available = True
        return True
    
    def get_room_statistics(self):
        """Get comprehensive statistics about rooms"""
        stats = {
            "total_rooms": self.get_total_rooms_count(),
            "available_rooms": len(self.get_available_rooms()),
            "booked_rooms": len([r for r in self.hotel.rooms if not r.is_available]),
            "occupancy_rate": round(self.get_occupancy_rate(), 2),
            "potential_revenue": self.get_revenue_potential(),
            "current_revenue": self.get_current_revenue(),
            "room_types": self.get_room_types_summary()
        }
        return stats