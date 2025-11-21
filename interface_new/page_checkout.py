"""page_checkout.py
This file defines the CheckoutPage class responsible for collecting customer
information, displaying booking details, and navigating to final confirmation.

Programmers: Astghik, Mahi
Date of code: November 8th, 2025

Description:
This page (index 2 in navigation) displays the checkout form where users enter their
personal and payment information. It shows a booking summary on the right side pulled
from BookingData singleton and creates input fields on the left that update CustomerData
as the user types. Uses UIFactory to create consistent form elements and HeaderComponent
for navigation back to room selection.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QTimer
from models import BookingData, CustomerData
from ui_components import UIFactory, HeaderComponent


class CheckoutPage:
    """Controls the checkout page of the Hotel Eleon booking system.
    
    This is the View layer for checkout. It builds the UI using components from
    UIFactory and manages user input. As users type in the form fields, data is
    automatically saved to the CustomerData singleton so it's available on the
    confirmation page.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Initializes the checkout page controller.
        
        Sets up references to the navigation system and both data singletons,
        then builds all UI elements including the form and booking summary.
        
        Parameters:
            parent (QWidget): Container widget for this page.
            stacked_widget (QStackedWidget): Navigation stack for page switching.
        """

        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()      # Model (Singleton)
        self.customer_data = CustomerData()    # Model (Singleton)
        self.input_fields = {}                 # Maps field keys to UI input widgets
        
        # Build the UI
        self._build_ui()
    
    def _build_ui(self):
        """Constructs all UI elements for the checkout page,
        including header, booking summary labels, and form fields.
        
        Creates a two-column layout: left side has the customer form with 9 input
        fields, right side displays booking summary (room, dates, guests, nights).
        """
        
        # Create header with back button
        HeaderComponent(
            self.parent, 
            show_back=True, 
            back_callback=self._go_back_to_rooms
        )
        
        # Room information label
        self.room_info_label = UIFactory.create_label(
            "(room details here)", 1600, 300, self.parent, 
            "font-size: 18px;"
        )
        
        # Check-in date label
        self.checkin_label = UIFactory.create_label(
            "Check In: (not selected)", 1600, 330, self.parent
        )
        
        # Check-out date label
        self.checkout_label = UIFactory.create_label(
            "Check Out: (not selected)", 1600, 360, self.parent
        )
        
        # Number of guests label
        self.guests_label = UIFactory.create_label(
            "Guests: (not selected)", 1600, 390, self.parent
        )
        
        # Number of nights label (calculated)
        self.nights_label = UIFactory.create_label(
            "Nights: (not calculated)", 1600, 420, self.parent
        )
        
        # Create customer information form
        self._create_customer_form()
        
        # Confirmation button
        self.confirm_button = UIFactory.create_button(
            "Confirm Booking", 
            1600, 900, 
            280, 60, 
            self.parent,
        )
        self.confirm_button.clicked.connect(self._confirm_booking)
        
        # Setup show event to update labels when page becomes visible
        self._setup_show_event()
    
    def _create_customer_form(self):
        """Creates all labeled input fields for collecting customer information.
        
        Builds 9 form fields in a vertical layout: name, email, phone, address,
        and payment info. Each field is connected to the CustomerData singleton
        so data updates automatically as the user types. Uses a loop to avoid
        repeating code for each field.
        
        Input fields created:
            - First Name, Last Name (personal info)
            - Email, Phone (contact info)
            - Street, Zip Code (address)
            - Card Number, Exp Date, CVV (payment)
        """
        
        y = 300      # Starting Y position
        x = 200      # Left column X position
        input_width = 400
        input_height = 40
        spacing = 60
        
        # Define all form fields (label text, model attribute key)
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
            
            label = UIFactory.create_label(label_text, x, y, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")
            
            field = UIFactory.create_input_field(
                x + 200, 
                y, 
                input_width, 
                input_height, 
                self.parent
            )
            
            # Track field by key
            self.input_fields[field_key] = field
            
            # Save to customer model when changed
            field.textChanged.connect(
                lambda text, key=field_key: self._on_field_changed(key, text)
            )
            
            y += spacing
    
    def _on_field_changed(self, field_key: str, text: str):
        """Updates the CustomerData singleton whenever an input field changes.
        
        Uses Python's setattr() to dynamically update the correct attribute on
        CustomerData based on the field_key. This is called every time the user
        types a character in any input field.
        
        Parameters:
            field_key (str): Attribute name on the model (e.g., "first_name").
            text (str): New text entered by the user.
        """
        setattr(self.customer_data, field_key, text)
    
    def _go_back_to_rooms(self):
        """Navigates to the room selection page.
        
        Changes the stacked widget index to 1 (room selection page).
        """
        self.stacked_widget.setCurrentIndex(1)
    
    def _confirm_booking(self):
        """Navigates to the final confirmation page.
        
        Changes the stacked widget index to 3 (confirmation page).
        No validation is performed - all fields are optional for this demo.
        """
        self.stacked_widget.setCurrentIndex(3)
        
    def _update_display(self):
        """Refreshes all booking summary labels based on the BookingData model.
        
        Called automatically when the page is shown. Pulls data from the BookingData
        singleton and updates all labels on the right side of the screen with current
        booking information (room, dates, guests, nights).
        """
        
        room = self.booking_data.selected_room
        
        if room:
            room_text = f"{room['title']}"
            self.room_info_label.setText(room_text)
        else:
            self.room_info_label.setText("(room details here)")
        
        # Dates
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
        
        # Guests
        guests_text = f"Guests: {self.booking_data.adults}"
        self.guests_label.setText(guests_text)

        # Nights calculation
        nights = self.booking_data.calculate_nights()
        if nights is not None:
            nights_text = f"Nights: {nights}"
        else:
            nights_text = "Nights: (not calculated)"
        self.nights_label.setText(nights_text)
    
    def _flash_field_red(self, field):
        """Briefly highlights an invalid input field in red.
        
        This function provides visual feedback when validation fails. It changes
        the field's style to red, then uses QTimer to revert back to the original
        style after 1 second (1000 milliseconds).
        
        Note: Currently not used, but kept for future validation features.
        
        Parameters:
            field: The QLineEdit widget to highlight.
        """
        
        original_style = field.styleSheet()
        
        red_style = (
            "border: 3px solid #ff4444; "
            "background-color: #ffebeb;"
        )
        field.setStyleSheet(red_style)
        
        QTimer.singleShot(1000, lambda: field.setStyleSheet(original_style))
    
    def _setup_show_event(self):
        """Overrides the parent widget's showEvent to update the display whenever
        the page becomes visible to the user.
        
        This ensures that if the user goes back and changes dates or room selection,
        the checkout page will show the updated information when they return.
        """
        
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            """Update display when page is shown."""
            self._update_display()
            
            # Chain original showEvent if present
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        # Attach new show event handler
        self.parent.showEvent = on_show_event