# calendar.py
class DayNode:
    def __init__(self, day_number):
        self.day_number = day_number
        self.bookings = []  # list of tuples (room_type, quantity)
        self.next_day = None


class MonthNode:
    def __init__(self, month_number):
        self.month_number = month_number
        self.day_list_head = None
        self.next_month = None


def get_booked_quantity(month, day, room_type, calendar_head):
    """Return how many rooms of a given type are booked on a given date."""
    month_node = calendar_head
    while month_node and month_node.month_number != month:
        month_node = month_node.next_month

    if not month_node:
        return 0

    day_node = month_node.day_list_head
    while day_node and day_node.day_number != day:
        day_node = day_node.next_day

    if not day_node:
        return 0

    for booked_type, qty in day_node.bookings:
        if booked_type == room_type["name"]:
            return qty
    return 0


def store_booking_range(start_month, start_day, end_month, end_day, room_type, calendar_head):
    """Store bookings for each day in the range into the linked list."""
    month = start_month
    day = start_day

    while True:
        # find or create month node
        if not calendar_head:
            calendar_head = MonthNode(month)

        prev, current = None, calendar_head
        while current and current.month_number < month:
            prev, current = current, current.next_month
        if not current or current.month_number != month:
            new_month = MonthNode(month)
            if prev:
                prev.next_month, new_month.next_month = new_month, current
            else:
                new_month.next_month = calendar_head
                calendar_head = new_month
            current = new_month

        # find or create day node
        prev_day, current_day = None, current.day_list_head
        while current_day and current_day.day_number < day:
            prev_day, current_day = current_day, current_day.next_day
        if not current_day or current_day.day_number != day:
            new_day = DayNode(day)
            if prev_day:
                prev_day.next_day, new_day.next_day = new_day, current_day
            else:
                new_day.next_day = current.day_list_head
                current.day_list_head = new_day
            current_day = new_day

        # update bookings
        updated = False
        for i, (rtype, qty) in enumerate(current_day.bookings):
            if rtype == room_type["name"]:
                current_day.bookings[i] = (rtype, qty + 1)
                updated = True
        if not updated:
            current_day.bookings.append((room_type["name"], 1))

        # stop if reached end date
        if month == end_month and day == end_day:
            break

        day += 1
        if day > 30:  # simplify: assume 30 days/month
            day, month = 1, month + 1

    return calendar_head
