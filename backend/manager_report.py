# manager_report.py

from backend.customer_controller import CustomerController
from backend.reservation_system import reservations_db, calendar_head
from backend.database import room_database
from backend.calendar import MonthNode, DayNode

def generate_occupancy_report(month, year):
    """
    Generate occupancy report for each room type for the given month and year.
    
    Parameters
    ----------
        month : int
            The month number (1-12).
        year : int
            The year (not used in current implementation but can be useful for future extensions).
    
    Returns
    -------
        dict
            A dictionary with room types as keys and a list of daily occupancy data as values.
    """
    report = {}
    total_days = 30
    for room in room_database:
        room_type = room["name"]
        daily_data = []
        for day in range(1, total_days + 1):
            booked_qty = count_booked_rooms(month, day, room, calendar_head)
            occupancy_rate = (booked_qty / room["quantity"]) * 100
            daily_data.append({
                "day": day,
                "booked_rooms": booked_qty,
                "occupancy_rate": occupancy_rate
            })
        report[room_type] = daily_data
    return report
    
def count_booked_rooms(month, day, room_type, calendar_head):
    """
    Count the number of booked rooms for a specific room type on a given date.
    
    Parameters
    ----------
        month : int
            The month number (1-12).
        day : int
            The day number (1-30).
        room_type : dict
            The room type dictionary containing at least the "name" key.
        calendar_head : MonthNode
            The head of the linked list representing the calendar.
    
    Returns
    -------
        int
            The quantity of the specified room type booked on the given date.
            Returns 0 if the month, day, or room type is not found.
    """
    current_month = calendar_head
    while current_month:
        if current_month.month_number == month:
            current_day = current_month.day_list_head
            while current_day:
                if current_day.day_number == day:
                    for rtype, qty in current_day.bookings:
                        if rtype == room_type["name"]:
                            return qty
                current_day = current_day.next_day
            break
        current_month = current_month.next_month
    return 0

def get_reservation_summary():
    """
    Get a summary of all reservations.
    
    Returns
    -------
        list
            A list of dictionaries containing reservation details.
    """
    summary = []
    for rid, details in reservations_db.items():
        summary.append({
            "reservation_id": rid,
            "customer_name": details["customer_name"],
            "room_type": details["room_type"],
            "check_in": details["check_in"],
            "check_out": details["check_out"],
        })
    return summary
    
def get_total_reservations():
    """
    Get the total number of reservations.
    """
    return len(reservations_db)

def get_total_customers():
    """
    Get the total number of customers.
    """
    customer_controller = CustomerController()
    return len(customer_controller.customers)

def calculate_nights(check_in, check_out):
    """
    Calculate the number of nights between check-in and check-out dates.
    
    Parameters
    ----------
        check_in : tuple
            A tuple (month, day) represented the check-in date.
        check_out : tuple
            A tuple (month, day) represented the check-out date.
   
    Returns
    -------
        int
            The number of nights between the two dates.
    """
    month_in, day_in = check_in
    month_out, day_out = check_out
    nights = 0
    while (month_in, day_in) != (month_out, day_out):
        nights += 1
        day_in += 1
        if day_in > 30:
            day_in, month_in = 1, month_in + 1
    return nights
    
def get_total_revenue():
    """
    Calculate the total revenue from all reservations.
    
    Returns
    -------
        float
            The total revenue generated from all reservations.
    """
    total_revenue = 0
    for rid, details in reservations_db.items():
        room_type = next((room for room in room_database if room["name"] == details["room_type"]), None)
        if room_type:
            nights = calculate_nights(details["check_in"], details["check_out"])
            total_revenue += room_type["price"] * nights
    return total_revenue

def generate_full_report(month, year):
    """
    Generate a full report including occupancy, total reservations, total customers, total revenue, and reservation summary.
    
    Parameters
    ----------
        month : int
            The month number (1-12).
        year : int
            The year (not used in current implementation but can be useful for future extensions).
    
    Returns
    -------
        dict
            A dictionary containing all report components.    
    """
    return {
        "occupancy_report": generate_occupancy_report(month, year),
        "total_reservations": get_total_reservations(),
        "total_customers": get_total_customers(),
        "total_revenue": get_total_revenue(),
        "reservation_summary": get_reservation_summary(),
    }
