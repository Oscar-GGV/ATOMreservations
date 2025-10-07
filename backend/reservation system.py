#Reservation System.py

from calendar import get_booked_quantity, store_booking_range, DayNode, MonthNode
reservations_db = {}
reservation_counter = 1
calendar_head = None
from database import room_database

def check_availability(room_type, check_in, check_out):
    global calendar_head
    total_quantity = room_type["quantity"]
    max_booked = 0
    month, day = check_in
    end_month, end_day = check_out
    while True:
        booked = get_booked_quantity(month, day, room_type, calendar_head)
        if booked >= total_quantity:
            return False
        if booked > max_booked:
            max_booked = booked 
        if (month, day) == (end_month, end_day):
            break
        day += 1
        if day > 30:
            day, month = 1, month + 1
    return True
def get_available_room_type(room_type_name, check_in, check_out);
    suitable_rooms = [room for room in room_database if room["max_guests"] >= num_guests]
    return [room for room in suitable_rooms if check_availability(room, check_in, check_out)]
def make_reservation(customer_name, room_type_name, check_in, check_out):
    global calendar_head, reservation_counter
    room_type = next((room for room in room_database if room["type] == room_type_name), None)"]))
    if not room_type:
        return None
    if not check_availability(room_type, check_in, check_out):
        return None
     rid = generate_reservation_id()
    reservations_db[rid] = {
        "customer_name": customer_name,
        "room_type": room_type_name,
        "check_in": check_in,
        "check_out": check_out
    }
    calendar_head = store_booking_range(check_in[0], check_in[1], check_out[0], check_out[1], room_type, calendar_head)
    return rid
def generate_reservation_id():
    global reservation_counter
    rid = f"R{reservation_counter:04d}"
    reservation_counter += 1
    return rid
def cancel_reservation(reservation_id):
    global calendar_head
    if rid not in reservations_db:
        return False
    reservation = reservations_db[rid]
    room_type = next((room for room in room_database if room["type"] == reservation["room_type"]), None)
    if not room_type:
        return False
    check_in = reservation["check_in"]
    check_out = reservation["check_out"]
    month, day = check_in
    end_month, end_day = check_out
    calendar_head = remove_booking_range(check_in[0], check_in[1], check_out[0], check_out[1], room_type, calendar_head)
    del reservations_db[rid]
    return True
