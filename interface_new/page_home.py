"""page_home.py
This file defines the HomePage class which acts as the starting screen of the
Hotel Eleon booking system. It handles date selection, guest selection,
and navigation to the availability results.

Programmers: Astghik, Mahi
Date of code: November 1st, 2025

Description:
This is the landing page (index 0 in navigation) where users start their booking.
It displays the hotel name and provides three main interactions: selecting check-in
and check-out dates using a calendar, choosing number of guests with a counter,
and a button to check availability. The date selection uses a smart algorithm that
automatically swaps dates if the user picks them in the wrong order.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QDate, QTimer
from models import BookingData
from ui_components import UIFactory, HeaderComponent, GuestCounter


class HomePage:
    """Controls the home screen of the Hotel Eleon booking interface.
    
    This is the first View in the booking flow. It uses components from UIFactory
    and custom components (GuestCounter) to build the interface. All selections
    are saved to the BookingData singleton so they're available on other pages.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Initializes the home page controller.
        
        Sets up references to navigation and the BookingData singleton, then
        builds all UI elements including hotel branding, date selector, guest
        counter, and availability button.
        
        Parameters:
            parent (QWidget): Parent widget hosting this page.
            stacked_widget (QStackedWidget): Navigation controller.
        """
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self._build_ui()
    
    def _build_ui(self):
        """Constructs the UI components for the home page, including headers,
        date pickers, guest selector, and navigation button.
        
        Creates the "HOTEL ELEON" branding labels, two date selection buttons that
        share one calendar widget, a guest counter button with dropdown, and a
        "Check Availability" button. The calendar and guest counter start hidden
        and appear when their buttons are clicked.
        """
        
        HeaderComponent(self.parent, show_back=False)
        
        UIFactory.create_label("HOTEL", 370, 300, self.parent,
                               "color: black; font-size: 30px; font-weight: bold;")
        UIFactory.create_label("ELEON", 320, 325, self.parent,
                               "color: black; font-size: 60px; font-weight: bold;")
        
        # Calendar selector (initially hidden)
        self.calendar = UIFactory.create_calendar(690, 425, 500, 250, self.parent)
        self.calendar.hide()
        self.calendar.clicked.connect(self._on_date_selected)
        
        # Date selection buttons
        self.checkin_button = UIFactory.create_button("Check In:        ", 650, 300, 300, 100, self.parent)
        self.checkin_button.clicked.connect(self._toggle_calendar)
        
        self.checkout_button = UIFactory.create_button("Check Out:        ", 950, 300, 300, 100, self.parent)
        self.checkout_button.clicked.connect(self._toggle_calendar)
        
        # Guest selector
        self.guests_button = UIFactory.create_button("Guests: 1", 1250, 300, 300, 100, self.parent)
        
        self.guest_counter = GuestCounter(
            1275, 425, 250, 100, self.parent,
            on_change=self._on_guest_count_changed
        )
        self.guests_button.clicked.connect(self.guest_counter.toggle)
        
        # Availability button
        self.availability_button = UIFactory.create_button(
            "Check Availability", 1550, 300, 300, 100, self.parent,
            "background-color: black; color: white; font-size: 20px;"
        )
        self.availability_button.clicked.connect(self._check_availability)
        
        self._setup_show_event()
    
    def _toggle_calendar(self):
        """Shows or hides the calendar widget when date buttons are clicked.
        
        Uses the calendar's current visibility state to toggle between shown and hidden.
        Both date buttons share the same calendar widget.
        """
        self.calendar.setVisible(not self.calendar.isVisible())
    
    def _on_date_selected(self, date: QDate):
        """Handles selecting dates from the calendar.
        
        This implements a smart date selection algorithm:
        1. First click sets check-in date
        2. Second click sets check-out date, BUT if the user picks an earlier date,
           it automatically swaps them (first becomes check-out, second becomes check-in)
        3. Third click starts over by setting a new check-in and clearing check-out
        
        This prevents users from creating invalid date ranges where check-out is
        before check-in. We chose this algorithm over showing an error message
        because it's more user-friendly and intuitive.
        
        Parameters:
            date (QDate): The date clicked in the calendar widget
        """
        formatted_date = date.toString("yyyy-MM-dd")
        
        if self.booking_data.check_in is None:
            self.booking_data.check_in = formatted_date
        
        elif self.booking_data.check_out is None:
            d1 = QDate.fromString(self.booking_data.check_in, "yyyy-MM-dd")
            d2 = QDate.fromString(formatted_date, "yyyy-MM-dd")
            
            if d2 < d1:
                # If user picks an earlier date for check-out,
                # swap check-in and check-out.
                self.booking_data.check_out = self.booking_data.check_in
                self.booking_data.check_in = formatted_date
            else:
                self.booking_data.check_out = formatted_date
        
        else:
            # Reset cycle: user selects a new check-in and clears old check-out.
            self.booking_data.check_in = formatted_date
            self.booking_data.check_out = None
        
        self._update_date_buttons()
    
    def _on_guest_count_changed(self, count: int):
        """Updates the number of adult guests and refreshes the button label.
        
        This is a callback function passed to GuestCounter. It's called whenever
        the user clicks the +/- buttons in the counter, implementing the Delegation
        pattern where GuestCounter delegates the update action back to this page.
        
        Parameters:
            count (int): Selected number of guests (1-8).
        """
        self.booking_data.adults = count
        self.guests_button.setText(f"Guests: {count}")
    
    def _check_availability(self):
        """Validates that both check-in and check-out are selected.
        If valid, navigates to the room selection page.
        
        This is basic validation - if either date is missing, it flashes the
        date buttons red to give visual feedback. If both dates are present,
        it proceeds to the room selection page (index 1).
        """
        
        if not self.booking_data.check_in or not self.booking_data.check_out:
            self._flash_red_buttons()
            return
        
        self.stacked_widget.setCurrentIndex(1)
    
    def _update_date_buttons(self):
        """Updates the date button text with selected values from the model.
        
        Pulls the current dates from BookingData singleton and updates the button
        labels to show the selected dates. If a date isn't selected yet, shows
        placeholder text with extra spaces for consistent button width.
        """
        
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
        """Highlights date selection buttons in red temporarily
        when the user attempts to proceed without selecting both dates.
        
        Provides visual feedback for validation. Changes button style to red,
        then uses QTimer.singleShot to revert back to normal after 1 second
        (1000 milliseconds). This gives users clear feedback without permanent
        error messages cluttering the interface.
        """
        
        red_style = "border: 3px solid #ff4444; background-color: #ffebeb;"
        self.checkin_button.setStyleSheet(red_style)
        self.checkout_button.setStyleSheet(red_style)
        
        QTimer.singleShot(1000, lambda: self.checkin_button.setStyleSheet(""))
        QTimer.singleShot(1000, lambda: self.checkout_button.setStyleSheet(""))
    
    def _setup_show_event(self):
        """Overrides the parent's showEvent so that calendar and guest selector
        reset visibility every time the home page is shown.
        
        This ensures a clean state when users navigate back to the home page -
        any open dropdowns are hidden. Preserves the original showEvent if it
        exists by chaining it after our logic.
        """
        
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            self.calendar.hide()
            self.guest_counter.hide()
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        self.parent.showEvent = on_show_event