#Reservation Class.py

class Reservation:
    """
    Represents a reservation made by a customer.
    Attributes:
    - room_type: Type of room reserved
    - check_in: Check-in date
    - check_out: Check-out date
    """
    def __init__(self, room_type, check_in, check_out):
        """
        Initializes a Reservation instance.
        Args:
        - room_type: Type of room reserved
        - check_in: Check-in date
        - check_out: Check-out date
        """
        self.room_type = room_type
        self.check_in = check_in
        self.check_out = check_out
