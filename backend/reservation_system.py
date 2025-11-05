
# reservation_system.py
from database import Hotel
from calendar import get_booked_quantity, store_booking_range
from customer import Customer

reservation_counter = 1
calendar_head = None


class ReservationSystem:
    def __init__(self):
        self.hotel = Hotel()
        self.reservations_db = {}

    def check_availability(self, room_type, check_in, check_out):
        global calendar_head
        total_quantity = sum(1 for room in self.hotel.rooms if room.room_type == room_type)
        month, day = check_in
        end_month, end_day = check_out

        while True:
            booked = get_booked_quantity(month, day, {"name": room_type}, calendar_head)
            if booked >= total_quantity:
                return False

            # Stop when reaching end date
            if (month, day) == (end_month, end_day):
                break

            day += 1
            if day > 30:  # Simplify month rollover
                day, month = 1, month + 1
        return True

    def get_available_room_types(self, check_in, check_out, num_guests):
        available_rooms = []
        room_types = set(room.room_type for room in self.hotel.rooms)

        for rtype in room_types:
            sample_room = next(room for room in self.hotel.rooms if room.room_type == rtype)
            if sample_room.max_guests >= num_guests and self.check_availability(rtype, check_in, check_out):
                available_rooms.append({
                    "name": rtype,
                    "max_guests": sample_room.max_guests,
                    "price": sample_room.price
                })
        return available_rooms

    def generate_reservation_id(self):
        global reservation_counter
        rid = f"R{reservation_counter:04d}" #starts with R has 4 0's and starts at 1 at the end of the 4th place
        reservation_counter += 1
        return rid

    def make_reservation(self, customer, room_type, check_in, check_out):
        global calendar_head
        if not self.check_availability(room_type, check_in, check_out):
            return None

        rid = self.generate_reservation_id()
        self.reservations_db[rid] = {
            "customer": customer, #customer object
            "room_type": room_type,
            "check_in": check_in,
            "check_out": check_out
        }

        calendar_head = store_booking_range(check_in[0], check_in[1], check_out[0], check_out[1],
                                            {"name": room_type}, calendar_head)
        return rid
