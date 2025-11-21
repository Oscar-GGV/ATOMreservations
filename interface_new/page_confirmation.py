"""page_confirmation.py
This file defines the ConfirmationPage class which displays the final booking summary
including room details, dates, guest information, and navigation to begin a new booking.

Programmers: Astghik, Mahi
Date of code: November 12th, 2025

Description:
This is the final page (index 3 in navigation) that shows a complete summary of the
booking after the user confirms. This page should display the user's reservation Id the summery informaton,
 and option to make a new booking

was used the same stucture as prevouse code to just quicly make the file, 
give it the same stucture, buil ui, update and show the event, with some basick customer infroamtion
the code now just has the basic stucture, but is not done, needs to be loinked to back end, and display more infromation
    
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from models import BookingData, CustomerData
from ui_components import UIFactory, HeaderComponent


class ConfirmationPage:


    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self.customer_data = CustomerData()

        self._build_ui()

    def _build_ui(self):
    
        
        HeaderComponent(self.parent, show_back=False)

        self.room_info_label = UIFactory.create_label(
            "(room details here)",
            1600, 300,
            self.parent,
            "font-size: 18px; color: black;"
        )

        self.checkin_label = UIFactory.create_label(
            "Check In: (not selected)",
            1600, 330,
            self.parent,
            "color: black;"
        )

        self.checkout_label = UIFactory.create_label(
            "Check Out: (not selected)",
            1600, 360,
            self.parent,
            "color: black;"
        )

        self.guests_label = UIFactory.create_label(
            "Guests: (not selected)",
            1600, 390,
            self.parent,
            "color: black;"
        )

        self.nights_label = UIFactory.create_label(
            "Nights: (not calculated)",
            1600, 420,
            self.parent,
            "color: black;"
        )

        self.guest_name_label = UIFactory.create_label(
            "Guest: (not provided)",
            1600, 450,
            self.parent,
            "color: black;"
        )

        self.guest_email_label = UIFactory.create_label(
            "Email: (not provided)",
            1600, 480,
            self.parent,
            "color: black;"
        )

        self.guest_phone_label = UIFactory.create_label(
            "Phone: (not provided)",
            1600, 510,
            self.parent,
            "color: black;"
        )

        # NEW BUTTON
        self.new_reservation = UIFactory.create_button(
            "Make a New Reservation",
            1600, 900,
            280, 60,
            self.parent,
            "background-color: black; color: white; font-size: 18px;"
        )

        self.new_reservation.clicked.connect(self._make_new)

        self._setup_show_event()

    def _update_display(self):
      

        # ROOM
        room = self.booking_data.selected_room
        if room:
            self.room_info_label.setText(room["title"])
        else:
            self.room_info_label.setText("(room details here)")

        # DATES
        if self.booking_data.check_in:
            self.checkin_label.setText(f"Check In: {self.booking_data.check_in}")
        else:
            self.checkin_label.setText("Check In: (not selected)")

        if self.booking_data.check_out:
            self.checkout_label.setText(f"Check Out: {self.booking_data.check_out}")
        else:
            self.checkout_label.setText("Check Out: (not selected)")

        # GUESTS
        self.guests_label.setText(f"Guests: {self.booking_data.adults}")

        # NIGHTS
        nights = self.booking_data.calculate_nights()
        if nights is not None:
            self.nights_label.setText(f"Nights: {nights}")
        else:
            self.nights_label.setText("Nights: (not calculated)")

        # CUSTOMER INFO
        first = self.customer_data.first_name or ""
        last = self.customer_data.last_name or ""
        full_name = (first + " " + last).strip()

        if full_name:
            self.guest_name_label.setText(f"Guest: {full_name}")
        else:
            self.guest_name_label.setText("Guest: (not provided)")

        if self.customer_data.email:
            self.guest_email_label.setText(f"Email: {self.customer_data.email}")
        else:
            self.guest_email_label.setText("Email: (not provided)")

        if self.customer_data.phone:
            self.guest_phone_label.setText(f"Phone: {self.customer_data.phone}")
        else:
            self.guest_phone_label.setText("Phone: (not provided)")

    def _setup_show_event(self):

        
        original_show = self.parent.showEvent

        def on_show(event):
            self._update_display()
            if original_show:
                try:
                    original_show(event)
                except:
                    pass

        self.parent.showEvent = on_show

    def _make_new(self):

        self.stacked_widget.setCurrentIndex(0)