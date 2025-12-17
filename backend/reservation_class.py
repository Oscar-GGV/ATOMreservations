"""reservation.py
Represents a reservation in the hotel reservation system.
Programmer: Oscar Guevara
"""

class Reservation:
    """
    Represents a reservation.
    Attributes: reservation_id (str): Unique ID for the reservation. customer_email (str): Email of the customer who made the reservation. room_type (str): Type of room reserved. check_in (str):  check_out (str): 
    """

    def __init__(self, reservation_id, customer_email, room_type, check_in, check_out):
        self.reservation_id = reservation_id
        self.customer_email = customer_email
        self.room_type = room_type
        self.check_in = check_in
        self.check_out = check_out

    def to_dict(self): #makes object inro a dict
        return {
            "reservation_id": self.reservation_id,
            "customer_email": self.customer_email,
            "room_type": self.room_type,
            "check_in": self.check_in,
            "check_out": self.check_out,
        }
    #Create Reservation object From a csv ROw
    @staticmethod
    def from_dict(data): #makes dict back into object
        return Reservation(
            data["reservation_id"],
            data["customer_email"],
            data["room_type"],
            data["check_in"],
            data["check_out"],
        )

