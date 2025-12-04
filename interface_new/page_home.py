"""page_home.py
This file creates the home page where users start their booking.
It lets them pick check-in/check-out dates, number of guests, and check availability.

Programmers: Astghik, Mahi
Date of code: November 1st, 2025
Updated: December 2025 - Added shared BookingData support

Description:
This is the first page (index 0) users see. It shows the hotel name and has three
main things: date picker buttons that share one calendar, a guest counter, and a
check availability button. When users pick dates, it automatically swaps them if
they pick check-out before check-in. All selections get saved to BookingData so
other pages can use them.

IMPORTANT: Now accepts a shared BookingData instance to ensure data persists
across all pages and through the "Make New Reservation" flow.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QDate, QTimer
from models import BookingData
from ui_components import UIFactory, HeaderComponent, GuestCounter


class HomePage:
    """Builds and controls the home page interface.
    Uses UIFactory and custom components to create the UI.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget, 
                 booking_data=None):
        """Sets up the home page.
        
        Parameters:
            parent: Widget container for this page
            stacked_widget: Navigation controller to switch between pages
            booking_data: Shared BookingData instance (optional, creates new if None)
        """
        self.parent = parent
        self.stacked_widget = stacked_widget
        
        # Use shared instance if provided, otherwise create new one
        self.booking_data = booking_data if booking_data else BookingData()
        
        self._build_ui()
    
    def _build_ui(self):
        """Creates all the UI elements on the home page.
        
        Builds the hotel name, date buttons, calendar, guest counter, and
        availability button. Calendar and counter start hidden.
        """
        
        HeaderComponent(self.parent, show_back=False)
        
        UIFactory.create_label("HOTEL", 370, 300, self.parent,
                               "color: black; font-size: 30px; font-weight: bold;")
        UIFactory.create_label("ELEON", 320, 325, self.parent,
                               "color: black; font-size: 60px; font-weight: bold;")
        
        # Calendar (hidden until user clicks date button)
        self.calendar = UIFactory.create_calendar(690, 425, 500, 250, self.parent)
        self.calendar.hide()
        self.calendar.clicked.connect(self._on_date_selected)
        
        # Date buttons (both use same calendar)
        self.checkin_button = UIFactory.create_button("Check In:        ", 650, 300, 300, 100, self.parent)
        self.checkin_button.clicked.connect(self._toggle_calendar)
        
        self.checkout_button = UIFactory.create_button("Check Out:        ", 950, 300, 300, 100, self.parent)
        self.checkout_button.clicked.connect(self._toggle_calendar)
        
        # Guest selector button
        self.guests_button = UIFactory.create_button("Guests: 1", 1250, 300, 300, 100, self.parent)
        
        # Guest counter dropdown
        self.guest_counter = GuestCounter(
            1275, 425, 250, 100, self.parent,
            on_change=self._on_guest_count_changed
        )
        self.guests_button.clicked.connect(self.guest_counter.toggle)
        
        # Check availability button
        self.availability_button = UIFactory.create_button(
            "Check Availability", 1550, 300, 300, 100, self.parent,
            "background-color: black; color: white; font-size: 20px;"
        )
        self.availability_button.clicked.connect(self._check_availability)
        
        self._setup_show_event()
    
    def _toggle_calendar(self):
        """Shows or hides the calendar when date buttons are clicked."""
        self.calendar.setVisible(not self.calendar.isVisible())
    
    def _on_date_selected(self, date: QDate):
        """Handles when user clicks a date in the calendar.
        
        Works in three steps:
        1. First click sets check-in
        2. Second click sets check-out (swaps if user picked earlier date)
        3. Third click resets and starts over with new check-in
        
        This prevents users from picking check-out before check-in.
        
        Parameters:
            date: The date user clicked
        """
        formatted_date = date.toString("yyyy-MM-dd")
        
        if self.booking_data.check_in is None:
            # First click - set check-in
            self.booking_data.check_in = formatted_date
        
        elif self.booking_data.check_out is None:
            # Second click - set check-out
            d1 = QDate.fromString(self.booking_data.check_in, "yyyy-MM-dd")
            d2 = QDate.fromString(formatted_date, "yyyy-MM-dd")
            
            if d2 < d1:
                # User picked earlier date, so swap them
                self.booking_data.check_out = self.booking_data.check_in
                self.booking_data.check_in = formatted_date
            else:
                self.booking_data.check_out = formatted_date
        
        else:
            # Third click - reset and start over
            self.booking_data.check_in = formatted_date
            self.booking_data.check_out = None
        
        self._update_date_buttons()
    
    def _on_guest_count_changed(self, count: int):
        """Called when user changes guest count.
        Updates the booking data and button text.
        
        Parameters:
            count: New number of guests
        """
        self.booking_data.adults = count
        self.guests_button.setText(f"Guests: {count}")
    
    def _check_availability(self):
        """Checks if dates are selected, then goes to room page.
        If dates missing, flashes buttons red as warning.
        """
        
        if not self.booking_data.check_in or not self.booking_data.check_out:
            self._flash_red_buttons()
            return
        
        self.stacked_widget.setCurrentIndex(1)
    
    def _update_date_buttons(self):
        """Updates button text to show selected dates."""
        
        if self.booking_data.check_in:
            checkin_text = f"Check In: {self.booking_data.check_in}"
        else:
            checkin_text = "Check In:        "
        
        if self.booking_data.check_out:
            checkout_text = f"Check Out: {self.booking_data.check_out}"
        else:
            checkout_text = "Check Out:        "
        
        self.checkin_button.setText(checkin_text)
        self.checkout_button.setText(checkout_text)
    
    def _flash_red_buttons(self):
        """Makes date buttons flash red for 1 second as error feedback."""
        
        red_style = "border: 3px solid #ff4444; background-color: #ffebeb;"
        self.checkin_button.setStyleSheet(red_style)
        self.checkout_button.setStyleSheet(red_style)
        
        # Revert back to normal after 1 second
        QTimer.singleShot(1000, lambda: self.checkin_button.setStyleSheet(""))
        QTimer.singleShot(1000, lambda: self.checkout_button.setStyleSheet(""))
    
    def _setup_show_event(self):
        """Makes sure calendar and guest counter hide when page is shown.
        Also updates the date buttons to reflect current BookingData state.
        """
        
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            # Hide popups
            self.calendar.hide()
            self.guest_counter.hide()
            
            # Update UI to reflect current booking data
            self._update_date_buttons()
            self.guests_button.setText(f"Guests: {self.booking_data.adults}")
            
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        self.parent.showEvent = on_show_event