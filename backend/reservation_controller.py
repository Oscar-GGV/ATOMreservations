"""reservation_controller.py
This file contains the ReservationController class which manages reservation operations in the hotel reservation system.
Programmer: Oscar Guevara
date of code: November 5th, 2025
updated: Novemeber 27th, 2025
"""
import csv
from backend.reservation_system import ReservationSystem
from backend.customer_controller import CustomerController
from backend.reservation_class import Reservation


class ReservationController:
    """
    Controller for handling reservation operations in the reservation system.

    Usage:
        cc = CustomerController()           # loads customers automatically
        rs = ReservationSystem()            # reservation system instance
        rc = ReservationController(cc, rs)  # reservations load automatically
    """

    FIELDNAMES = ["reservation_id", "customer_email", "room_type", "check_in", "check_out"]

    def __init__(self, customer_controller: CustomerController, reservation_system: ReservationSystem,
                 csv_file: str = "reservations.csv"):
        self.customer_controller = customer_controller
        self.reservation_system = reservation_system
        self.csv_file = csv_file

        # In-memory list of Reservation objects
        self.reservations: list[Reservation] = []

        # Load existing reservations (if any)
        self.load_reservations_from_csv()

 
    def make_reservation(self, customer, room_type: str, check_in: tuple, check_out: tuple) -> dict:
        """
        Make a reservation for a customer.

        Args:
            customer: a Customer object (expected)
            room_type: str
            check_in: (month, day) tuple
            check_out: (month, day) tuple

        Returns:
            dict with status and reservation_id or reason
        """
        if not customer:
            return {"status": "failed", "reason": "Invalid customer"}

        #check if customer exists in controller 
        exists = self.customer_controller.find_customer_by_email(customer.email)
        if not exists:
            # add_customer expects (first_name, last_name, email, phone, address)
            # (CustomerController.add_customer saves to CSV)
            self.customer_controller.add_customer(
                customer.first_name,
                customer.last_name,
                customer.email,
                customer.phone,
                customer.address
            )

        # Ask ReservationSystem to create the booking (it returns a reservation id or None)
        reservation_id = self.reservation_system.make_reservation(customer, room_type, check_in, check_out)
        if not reservation_id:
            return {"status": "failed", "reason": "No availability or invalid room type"}

        # Convert dates to "MM-DD" strings and create Reservation model
        check_in_str = f"{check_in[0]:02d}-{check_in[1]:02d}"
        check_out_str = f"{check_out[0]:02d}-{check_out[1]:02d}"

        new_reservation = Reservation(
            reservation_id=reservation_id,
            customer_email=customer.email,
            room_type=room_type,
            check_in=check_in_str,
            check_out=check_out_str
        )

        # Keep in memory and persist
        self.reservations.append(new_reservation)
        self.save_reservation_to_csv(new_reservation)

        return {"status": "success", "reservation_id": reservation_id}

    def cancel_reservation(self, reservation_id: str) -> dict:
        """
        Cancel reservation by id. Will call ReservationSystem.cancel_reservation() if present,
        and will also update in-memory list & CSV.
        """
        # Try to cancel via reservation_system if available
        cancelled_by_system = False
        if hasattr(self.reservation_system, "cancel_reservation"):
            try:
                cancelled_by_system = self.reservation_system.cancel_reservation(reservation_id)
            except Exception:
                cancelled_by_system = False

        # Remove from in-memory list (if present)
        original_len = len(self.reservations)
        self.reservations = [r for r in self.reservations if r.reservation_id != reservation_id]

        if len(self.reservations) < original_len:
            # Persist the change
            self.save_all_reservations_to_csv()
            return {"status": "success"}
        else:
            # If ReservationSystem reported success but we didn't have it locally, treat as success
            if cancelled_by_system:
                return {"status": "success"}
            return {"status": "failed", "reason": "Reservation ID not found"}

    def get_available_room_types(self, check_in: tuple, check_out: tuple, num_guests: int) -> list:
        """
        Wrapper around ReservationSystem.get_available_room_types.
        Signature matches ReservationSystem: (check_in, check_out, num_guests)
        """
        return self.reservation_system.get_available_room_types(check_in, check_out, num_guests)

    def is_room_type_available(self, room_type: str, check_in: tuple, check_out: tuple) -> bool:
        """
        Check availability for a specific room_type across a date range.
        Uses ReservationSystem.check_availability(room_type, check_in, check_out).
        """
        return self.reservation_system.check_availability(room_type, check_in, check_out)

 
    # CSV Persistence
   
    def save_reservation_to_csv(self, reservation: Reservation) -> None:
        """Append a single reservation to the CSV file (writes header if missing)."""
        write_header = not self._csv_exists()
        with open(self.csv_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            if write_header:
                writer.writeheader()
            writer.writerow({
                "reservation_id": reservation.reservation_id,
                "customer_email": reservation.customer_email,
                "room_type": reservation.room_type,
                "check_in": reservation.check_in,
                "check_out": reservation.check_out
            })

    def save_all_reservations_to_csv(self) -> None:
        """Overwrite the reservations CSV with the current in-memory list."""
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            for r in self.reservations:
                writer.writerow({
                    "reservation_id": r.reservation_id,
                    "customer_email": r.customer_email,
                    "room_type": r.room_type,
                    "check_in": r.check_in,
                    "check_out": r.check_out
                })

    def load_reservations_from_csv(self) -> None:
        """Load reservations from CSV into memory. For each reservation, try to link the Customer object if present."""
        try:
            with open(self.csv_file, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # build Reservation object (reservation_id kept as string)
                    r = Reservation(
                        reservation_id=row["reservation_id"],
                        customer_email=row["customer_email"],
                        room_type=row["room_type"],
                        check_in=row["check_in"],
                        check_out=row["check_out"]
                    )
                    self.reservations.append(r)

                    # Also hydrate reservation_system.reservations_db if possible (non-destructive)
                    try:
                        # If reservation_system expects the original (customer object, tuples), we try to approximate:
                        cust = self.customer_controller.find_customer_by_email(r.customer_email)
                        # Convert MM-DD back to tuple for system storage if needed
                        def mmdd_to_tuple(s: str) -> tuple:
                            parts = s.split("-")
                            return (int(parts[0]), int(parts[1]))
                        check_in_tuple = mmdd_to_tuple(r.check_in)
                        check_out_tuple = mmdd_to_tuple(r.check_out)
                        # store into reservation_system.reservations_db if attribute exists
                        if hasattr(self.reservation_system, "reservations_db"):
                            # store a representation similar to how make_reservation stores it
                            self.reservation_system.reservations_db[r.reservation_id] = {
                                "customer": cust,  # may be None if not found
                                "room_type": r.room_type,
                                "check_in": check_in_tuple,
                                "check_out": check_out_tuple
                            }
                    except Exception:
                        # Don't fail loading if reservation_system structure is different
                        pass
        except FileNotFoundError:
            # No CSV yet, ok cause its gonna be created on first save
            pass

    def _csv_exists(self) -> bool:
        try:
            open(self.csv_file, "r").close()
            return True
        except FileNotFoundError:
            return False
