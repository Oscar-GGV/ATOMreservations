
from helpers import create_label, create_header
from PyQt5.QtWidgets import QLineEdit
from page1 import selected_dates
from datetime import datetime
from PyQt5.QtGui import QFont


customer_info = {}

def build_page3(window, stacked_widget, page2_index):
    create_header(window, show_back=True, stacked_widget=stacked_widget, back_target_index=page2_index)

    # Room Info
    room_info_label = create_label("(room details here)", 1600, 300, window)
    room_info_label.setStyleSheet("font-size: 18px;")

    checkin_label = create_label("Check In: (not selected)", 1600, 330, window)
    checkout_label = create_label("Check Out: (not selected)", 1600, 360, window)
    guests_label = create_label("Guests: (not selected)", 1600, 390, window)
    nights_label = create_label("Nights: (not calculated)", 1600, 420, window)

    # Customer Info Fields
    y = 300
    x = 200
    input_width = 400
    input_height = 40
    spacing = 60

    def add_input(label, x, y, key):
        lbl = create_label(label, x, y, window)
        label_font = QFont("Arial", 10)
        label_font.setBold(True)
        lbl.setFont(label_font)

        # Input setup
        field = QLineEdit(window)
        field.setGeometry(x + 200, y, input_width, input_height)
        field.setFont(QFont("Arial", 8))  # this forces size to apply

        customer_info[key] = field

    add_input("First Name:", x, y, "first_name"); y += spacing
    add_input("Last Name:", x, y, "last_name"); y += spacing
    add_input("Email:", x, y, "email"); y += spacing
    add_input("Phone:", x, y, "phone"); y += spacing
    add_input("Street:", x, y, "street"); y += spacing
    add_input("Zip Code:", x, y, "zip"); y += spacing
    add_input("Card Number:", x, y, "card"); y += spacing
    add_input("Exp. Date (MM/YY):", x, y, "exp"); y += spacing
    add_input("CVV:", x, y, "cvv")


    def update_display():
        room = selected_dates.get("room", {})
        title = room.get("title", "N/A")
        desc = room.get("description", "N/A")
        room_info_label.setText(f"{title}\n{desc}")

        checkin_text = f"Check In: {selected_dates['check_in']}" if selected_dates['check_in'] else "Check In: (not selected)"
        checkout_text = f"Check Out: {selected_dates['check_out']}" if selected_dates['check_out'] else "Check Out: (not selected)"
        guests_text = f"Guests: {selected_dates['adults']}" if selected_dates.get("adults") else "Guests: (not selected)"

        checkin_label.setText(checkin_text)
        checkout_label.setText(checkout_text)
        guests_label.setText(guests_text)

        try:
            check_in = datetime.strptime(selected_dates["check_in"], "%Y-%m-%d")
            check_out = datetime.strptime(selected_dates["check_out"], "%Y-%m-%d")
            nights = (check_out - check_in).days
            nights_label.setText(f"Nights: {nights}")
        except:
            nights_label.setText("Nights: (not calculated)")

    def on_show(event):
        update_display()
        try:
            super(type(window), window).showEvent(event)
        except AttributeError:
            pass

    window.showEvent = on_show