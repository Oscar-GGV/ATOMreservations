# manager_report.py

from backend.customer_controller import CustomerController
from backend.reservation_system import reservations_db, calendar_head
from backend.database import room_database
from backend.calendar import MonthNode, DayNode

def generate_occupancy_report(month, year):
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
    return len(reservations_db)

def get_total_customers():
    customer_controller = CustomerController()
    return len(customer_controller.customers)

def calculate_nights(check_in, check_out):
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
    total_revenue = 0
    for rid, details in reservations_db.items():
        room_type = next((room for room in room_database if room["name"] == details["room_type"]), None)
        if room_type:
            nights = calculate_nights(details["check_in"], details["check_out"])
            total_revenue += room_type["price"] * nights
    return total_revenue

def generate_full_report(month, year):
    return {
        "occupancy_report": generate_occupancy_report(month, year),
        "total_reservations": get_total_reservations(),
        "total_customers": get_total_customers(),
        "total_revenue": get_total_revenue(),
        "reservation_summary": get_reservation_summary(),
    }
