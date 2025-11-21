"""page_checkout.py
This file creates the checkout page where users enter their personal information.
It shows a booking summary and collects customer details through a form.

Programmers: Astghik, Mahi
Date of code: November 8th, 2025

Description:
This page (index 2) displays the checkout form on the left and booking summary on
the right. Users fill in their name, contact info, address, and payment details.
As they type, the information gets saved to CustomerData automatically. The booking
summary shows the selected room, dates, guests, and nights from BookingData.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QTimer
from models import BookingData, CustomerData
from ui_components import UIFactory, HeaderComponent


class CheckoutPage:
    """Builds and controls the checkout page.
    Creates form fields and displays booking summary.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Sets up the checkout page.
        
        Parameters:
            parent: Widget container for this page
            stacked_widget: Navigation controller to switch pages
        """

        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self.customer_data = CustomerData()
        self.input_fields = {}  # Stores all input fields for easy access
        
        self._build_ui()
    
    def _build_ui(self):
        """Creates all UI elements on checkout page.
        
        Builds header with back button, booking summary labels on right side,
        and customer form with 9 input fields on left side.
        """
        
        # Header with back button
        HeaderComponent(
            self.parent, 
            show_back=True, 
            back_callback=self._go_back_to_rooms
        )
        
        # Booking summary labels on right
        self.room_info_label = UIFactory.create_label(
            "(room details here)", 1600, 300, self.parent, 
            "font-size: 18px;"
        )
        
        self.checkin_label = UIFactory.create_label(
            "Check In: (not selected)", 1600, 330, self.parent
        )
        
        self.checkout_label = UIFactory.create_label(
            "Check Out: (not selected)", 1600, 360, self.parent
        )
        
        self.guests_label = UIFactory.create_label(
            "Guests: (not selected)", 1600, 390, self.parent
        )
        
        self.nights_label = UIFactory.create_label(
            "Nights: (not calculated)", 1600, 420, self.parent
        )
        
        # Create customer form on left
        self._create_customer_form()
        
        # Confirm button
        self.confirm_button = UIFactory.create_button(
            "Confirm Booking", 
            1600, 900, 
            280, 60, 
            self.parent,
        )
        self.confirm_button.clicked.connect(self._confirm_booking)
        
        # Update summary when page shows
        self._setup_show_event()
    
    def _create_customer_form(self):
        """Creates all the input fields for customer information.
        
        Makes 9 labeled input fields in a vertical list. Each field is connected
        to CustomerData so it saves automatically when user types. Uses a loop
        to avoid repeating code for each field.
        """
        
        y = 300  # Starting position
        x = 200
        input_width = 400
        input_height = 40
        spacing = 60
        
        # List of all form fields with their labels
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Street:", "street"),
            ("Zip Code:", "zip_code"),
            ("Card Number:", "card_number"),
            ("Exp. Date (MM/YY):", "exp_date"),
            ("CVV:", "cvv")
        ]
        
        for label_text, field_key in fields:
            
            # Create label
            label = UIFactory.create_label(label_text, x, y, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")
            
            # Create input field
            field = UIFactory.create_input_field(
                x + 200, 
                y, 
                input_width, 
                input_height, 
                self.parent
            )
            
            # Store field for later access
            self.input_fields[field_key] = field
            
            # Save to CustomerData when user types
            field.textChanged.connect(
                lambda text, key=field_key: self._on_field_changed(key, text)
            )
            
            y += spacing
    
    def _on_field_changed(self, field_key: str, text: str):
        """Saves input field value to CustomerData when user types.
        
        Parameters:
            field_key: Name of the field (like "first_name")
            text: What user typed
        """
        setattr(self.customer_data, field_key, text)
    
    def _go_back_to_rooms(self):
        """Goes back to room selection page."""
        self.stacked_widget.setCurrentIndex(1)
    
    def _confirm_booking(self):
        """Goes to confirmation page when confirm button clicked."""
        self.stacked_widget.setCurrentIndex(3)
        
    def _update_display(self):
        """Updates booking summary labels with current data.
        Gets room, dates, guests info from BookingData and displays it.
        """
        
        room = self.booking_data.selected_room
        
        if room:
            room_text = f"{room['title']}"
            self.room_info_label.setText(room_text)
        else:
            self.room_info_label.setText("(room details here)")
        
        # Update date labels
        if self.booking_data.check_in:
            checkin_text = f"Check In: {self.booking_data.check_in}"
        else:
            checkin_text = "Check In: (not selected)"
        self.checkin_label.setText(checkin_text)
        
        if self.booking_data.check_out:
            checkout_text = f"Check Out: {self.booking_data.check_out}"
        else:
            checkout_text = "Check Out: (not selected)"
        self.checkout_label.setText(checkout_text)
        
        # Update guests
        guests_text = f"Guests: {self.booking_data.adults}"
        self.guests_label.setText(guests_text)

        # Calculate and show nights
        nights = self.booking_data.calculate_nights()
        if nights is not None:
            nights_text = f"Nights: {nights}"
        else:
            nights_text = "Nights: (not calculated)"
        self.nights_label.setText(nights_text)
    
    def _flash_field_red(self, field):
        """Makes an input field flash red for 1 second.
        Used to show validation errors (not currently used).
        
        Parameters:
            field: The input field to highlight
        """
        
        original_style = field.styleSheet()
        
        red_style = (
            "border: 3px solid #ff4444; "
            "background-color: #ffebeb;"
        )
        field.setStyleSheet(red_style)
        
        # Revert back after 1 second
        QTimer.singleShot(1000, lambda: field.setStyleSheet(original_style))
    
    def _setup_show_event(self):
        """Makes summary update automatically when page is shown.
        This keeps the booking info current.
        """
        
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            self._update_display()
            
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        self.parent.showEvent = on_show_event