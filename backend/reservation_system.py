"""Reservation_system.py
This file contains the ReservationSystem class which manages reservations in the hotel reservation system.
Programmers: Mike and Oscar
date of code: November 5th, 2025
adjusted November 10th, 2025"""
from backend.database import Hotel, Room
from backend.calendar import store_booking_range, get_booked_quantity
from backend.customer import Customer

reservation_counter = 1

class ReservationSystem:
    """Manages reservations and room availability in the hotel reservation system."""
    def __init__(self):
        """Initializes the ReservationSystem with a Hotel instance and reservation database."""
        self.calendar_head = None
        self.hotel = Hotel()
        self.reservations_db = {}

    def check_availability(self, room_type, check_in, check_out): #check in has to be mm dd
        """Checks if a room type is available for the given date range.
        Parameters:
            room_type (str): The type of room to check availability for.
            check_in (tuple): The check-in date as (month, day).
            check_out (tuple): The check-out date as (month, day).
        Returns:
            bool: True if the room type is available, False otherwise."""
        total_quantity = sum(1 for room in self.hotel.rooms if room.room_type == room_type)
        month, day = check_in
        end_month, end_day = check_out

        while True:
            booked = get_booked_quantity(month, day, room_type, self.calendar_head) #uses calendar.py function
            if booked >= total_quantity:
                return False

            # Stop when reaching end date
            if (month, day) == (end_month, end_day):
                break
#this increments the day and handles the month rollover
            day += 1
            if day > 30:  # assume 30 days per month, this is done for simplicity
                day = 1
                month += 1
                
        return True

    def get_available_room_types(self, check_in, check_out, num_guests): #FIX
        """Gets a list of available room types for the given date range and number of guests.
        Parameters:
            check_in (tuple): The check-in date as (month, day).
            check_out (tuple): The check-out date as (month, day).
            num_guests (int): The number of guests.
        Returns:
            list: A list of available room types that can accommodate the number of guests."""
        available_rooms = []
        room_types = set(room.room_type for room in self.hotel.rooms)

        for rtype in room_types: #rtype ~ roomtype iterates through room_types from room manager
            sample_room = next(room for room in self.hotel.rooms if room.room_type == rtype) #
            if sample_room.max_guests >= num_guests and self.check_availability(rtype, check_in, check_out):
                available_rooms.append({
                    "name": rtype,
                    "max_guests": sample_room.max_guests,
                    "price": sample_room.price
                })
        return available_rooms

    def generate_reservation_id(self):
        """Generates a unique reservation ID."""
        global reservation_counter
        rid = f"R{reservation_counter:04d}" #starts with R has 4 0's and starts at 1 at the end of the 4th place
        reservation_counter += 1
        return rid

    def make_reservation(self, customer, room_type, check_in, check_out):
        """Makes a reservation for a customer if the room type is available.
        Parameters:
            customer (Customer): The customer making the reservation.
            room_type (str): The type of room to reserve.
            check_in (tuple): The check-in date as (month, day).
            check_out (tuple): The check-out date as (month, day).
        Returns:
            str or None: The reservation ID if successful, None if the room type is not available."""
        if not self.check_availability(room_type, check_in, check_out): 
            return None

        rid = self.generate_reservation_id()
        self.reservations_db[rid] = {
            "customer": customer, #customer object
            "room_type": room_type,
            "check_in": check_in,
            "check_out": check_out
        }

        self.calendar_head = store_booking_range(check_in[0], check_in[1], check_out[0], check_out[1], {"name": room_type}, self.calendar_head) ##NNEDS FIXCING
        return rid
