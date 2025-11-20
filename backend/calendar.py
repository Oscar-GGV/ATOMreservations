# calendar.py
class DayNode:
    """
    Node representing a day in the linked list.
    Attributes
    ----------
        day_number : int
            The numerical day of the month (e.g., 1-30).
        bookings : list of tuples
            Each tuple contains (room_type, guantity) booked for that day.
        next_day : DayNode or None
            Pointer to the next day node in the linked list.
    """
    def __init__(self, day_number):
        self.day_number = day_number
        self.bookings = []  # list of tuples (room_type, quantity)
        self.next_day = None


class MonthNode:
    """
    Node representing a month in the linked list.
    Attributes
    ----------
        month_number : int
            The numerical month (e.g., 1–12).
        day_list_head : DayNode or None
            Pointer to the head of the linked list of days for this month.
        next_month : MonthNode or None
            Pointer to the next month node in the linked list.
    """
    def __init__(self, month_number):
        self.month_number = month_number
        self.day_list_head = None
        self.next_month = None


def store_booking_range(start_month, start_day, end_month, end_day, room_type, calendar_head):
    """
    Store a booking for a specific room type over a date range in the calendar linked list.
    Parameters
    ----------
        start_month : int
            The starting month number (1-12).
        start_day : int
            The starting day number (1-30).
        end_month : int
            The ending month number (1-12).
        end_day : int
            The ending day number (1-30).
        room_type : dict
            The room type dictionary containing at leas the "name" key.
        calendar_head : MonthNode
            The head of the linked list representing the calendar.
    Returns
    -------
        MonthNode
            The updated head of the calendar linked list.
    """
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
