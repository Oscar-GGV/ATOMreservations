"""reservation_controller.py
This file contains the ReservationController class which manages reservation operations in the hotel reservation system.
Programmer:Oscar Guevara
date of code: November 5th, 2025
"""
from backend.reservation_system import ReservationSystem
from backend.customer_controller import CustomerController

class ReservationController:
    """Controller for handling reservation operations in the reservation system."""
    def __init__(self):
        """Initializes the ReservationController with CustomerController and ReservationSystem instances."""
        #important**** when main.py is made make sure to fix the bottom two lines so that this class doesnt create seperate instances
        self.customer_controller = CustomerController()
        self.reservation_system = ReservationSystem()

    def make_reservation(self, customer, room_type, check_in, check_out):
        """Makes a reservation for a customer.
        Parameters:
            customer (Customer): The customer making the reservation.
            room_type (str): The type of room to reserve.
            check_in (tuple): The check-in date as (month, day).
            check_out (tuple): The check-out date as (month, day).
        Returns:
            dict: A dictionary with reservation status and details."""
        if not customer: #this validates the customer object
            return {"status": "failed", "reason": "Invalid customer"}
    
        exists = self.customer_controller.find_customer_by_email(customer.email)
        if not exists: #if customer does not exist, add to system
            self.customer_controller.customers.append(customer)

        reservation_id = self.reservation_system.make_reservation(customer, room_type, check_in, check_out)
        if reservation_id:
            return {"status": "success", "reservation_id": reservation_id}
        else:
            return {"status": "failed", "reason": "No availability or invalid room type"}

    def cancel_reservation(self, reservation_id):
        """Cancels a reservation by its ID.
        Parameters:
            reservation_id (str): The ID of the reservation to cancel.
        Returns:
            dict: A dictionary with cancellation status."""
        result = self.reservation_system.cancel_reservation(reservation_id)
        if result:
            return {"status": "success"}
        else:
            return {"status": "failed", "reason": "Reservation ID not found"}

    def check_availability(self, room_type, check_in, check_out):
        """Checks availability of a room type for given dates.
        Parameters:
            room_type (str): The type of room to check.
            check_in (tuple): The check-in date as (month, day).
            check_out (tuple): The check-out date as (month, day).
        Returns:
            list: A list of available room types."""
        available_rooms = self.reservation_system.get_available_room_types(room_type, check_in, check_out)
        return available_rooms
    #IMPORTANT***** CSV FILE HANDLING TO BE ADDED LATER
