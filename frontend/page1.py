from helpers import create_custom_button, create_calendar, connect_action, toggle_widget, create_guest_box_with_counter, create_label, create_header
from PyQt5.QtCore import QDate

# Global dictionary to store selected data
selected_dates = {
    "check_in": None,
    "check_out": None,
    "adults": 1
}

def build_page1(window, stacked_widget, page2_index):
    create_header(window)  # Header without back button

    label = create_label("HOTEL", 370, 300, window)
    label.setStyleSheet("color: black; font-size: 30px; font-weight: bold;")
    label = create_label("ELEON", 320, 325, window)
    label.setStyleSheet("color: black; font-size: 60px; font-weight: bold;")

    calendar = create_calendar(690, 425, 500, 250, window)
    calendar.hide()

    checkin_button = create_custom_button("Check In:        ", 650, 300, 300, 100, window)
    checkout_button = create_custom_button("Check Out:        ", 950, 300, 300, 100, window)
    guests_button = create_custom_button("Guests: 1", 1250, 300, 300, 100, window)

    def update_guest_text(value):
        guests_button.setText(f"Guests: {value}")

    guest_box, adults_counter = create_guest_box_with_counter(1275, 425, 250, 100, window, on_value_change=update_guest_text)
    guest_box.hide()
    connect_action(guests_button, lambda: toggle_widget(guest_box))

    def go_to_page2():
        selected_dates["adults"] = adults_counter["value"]
        stacked_widget.setCurrentIndex(page2_index)

    availability_button = create_custom_button("Check Availability", 1550, 300, 300, 100, window)
    availability_button.setStyleSheet("background-color: black; color: white; font-size: 20px;")
    connect_action(availability_button, go_to_page2)

    connect_action(checkin_button, lambda: toggle_widget(calendar))
    connect_action(checkout_button, lambda: toggle_widget(calendar))

    def on_date_selected(date: QDate):
        formatted_date = date.toString("yyyy-MM-dd")

        if selected_dates["check_in"] is None:
            selected_dates["check_in"] = formatted_date
        elif selected_dates["check_out"] is None:
            d1 = QDate.fromString(selected_dates["check_in"], "yyyy-MM-dd")
            d2 = QDate.fromString(formatted_date, "yyyy-MM-dd")

            if d2 < d1:
                selected_dates["check_out"] = selected_dates["check_in"]
                selected_dates["check_in"] = formatted_date
            else:
                selected_dates["check_out"] = formatted_date
        else:
            selected_dates["check_in"] = formatted_date
            selected_dates["check_out"] = None

        checkin_text = f"Check In: {selected_dates['check_in']}" if selected_dates['check_in'] else "Check In:        "
        checkout_text = f"Check Out: {selected_dates['check_out']}" if selected_dates['check_out'] else "Check Out:        "
        checkin_button.setText(checkin_text)
        checkout_button.setText(checkout_text)

    calendar.clicked.connect(on_date_selected)

    def on_show_event(event):
        calendar.hide()
        guest_box.hide()
        try:
            super(type(window), window).showEvent(event)
        except AttributeError:
            pass
    window.showEvent = on_show_event
