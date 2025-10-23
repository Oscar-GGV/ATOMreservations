# ✅ page2.py
from helpers import create_label, create_custom_button, connect_action, create_header
from room_box import build_room_display
from page1 import selected_dates
from room_data import rooms
from datetime import datetime

def build_page2(window, stacked_widget, page1_index):
    create_header(window, show_back=True, stacked_widget=stacked_widget, back_target_index=page1_index)

    checkin_label = create_label("Check In: (not selected)", 50, 200, window)
    checkout_label = create_label("Check Out: (not selected)", 50, 230, window)
    guests_label = create_label("Guests: (not selected)", 50, 260, window)
    nights_label = create_label("Nights: (not calculated)", 50, 290, window)

    def handle_room_select(title, description):
        selected_dates["room"] = {"title": title, "description": description}
        stacked_widget.setCurrentIndex(2)  # jump to Page 3


    def update_labels():
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
        update_labels()
        try:
            super(type(window), window).showEvent(event)
        except AttributeError:
            pass
    window.showEvent = on_show

    room_width = 300
    room_height = 500
    spacing = 20
    max_per_row = 3

    x_start = 500
    y_start = 300
    x = x_start
    y = y_start

    for idx, room in enumerate(rooms):
        box = build_room_display(
            x=x,
            y=y,
            parent=window,
            room_data=room,
            on_select=handle_room_select
        )

        if (idx + 1) % max_per_row == 0:
            x = x_start
            y += room_height + spacing
        else:
            x += room_width + spacing

    needed_rows = (len(rooms) + max_per_row - 1) // max_per_row
    total_height = y_start + needed_rows * (room_height + spacing) + 100
    window.setMinimumHeight(total_height)