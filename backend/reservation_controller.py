from backend.reservation_system import ReservationSystem
from backend.customer_controller import CustomerController

class ReservationController:
    def __init__(self):
        #important**** when main.py is made make sure to fix the bottom two lines so that this class doesnt create seperate instances
        self.customer_controller = CustomerController()
        self.reservation_system = ReservationSystem()

    def make_reservation(self, customer, room_type, check_in, check_out):
        if not customer: #this validates the customer object
            return {"status": "failed", "reason": "Invalid customer"}
    
        exists = self.customer_controller.find_customer_by_email(customer.email)
        if not exists: #if customer does not exist, add to system
            self.customer_controller.customers.append(customer)

        # Make reservation
        reservation_id = self.reservation_system.make_reservation(customer, room_type, check_in, check_out)
        if reservation_id:
            return {"status": "success", "reservation_id": reservation_id}
        else:
            return {"status": "failed", "reason": "No availability or invalid room type"}

    def cancel_reservation(self, reservation_id):
        result = self.reservation_system.cancel_reservation(reservation_id)
        if result:
            return {"status": "success"}
        else:
            return {"status": "failed", "reason": "Reservation ID not found"}

    def check_availability(self, room_type, check_in, check_out):
        available_rooms = self.reservation_system.get_available_room_types(room_type, check_in, check_out)
        return available_rooms
    #IMPORTANT***** CSV FILE HANDLING TO BE ADDED LATER
