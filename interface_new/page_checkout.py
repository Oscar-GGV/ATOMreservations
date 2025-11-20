from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QTimer
from models import BookingData, CustomerData
from ui_components import UIFactory, HeaderComponent


class CheckoutPage:

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):

        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()  # Model (Singleton)
        self.customer_data = CustomerData()  # Model (Singleton)
        self.input_fields = {}  # Store references to input fields
        
        # Build the UI
        self._build_ui()
    
    def _build_ui(self):
        
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
        
        self.confirm_button = UIFactory.create_button(
            "Confirm Booking", 
            1600, 900, 
            280, 60, 
            self.parent,

        )
        self.confirm_button.clicked.connect(self._confirm_booking)
        
        
        # Setup show event to update display when page loads
        self._setup_show_event()
    
    def _create_customer_form(self):

        
        y = 300  # Starting Y position
        x = 200  # Starting X position (left side)
        input_width = 400
        input_height = 40
        spacing = 60  # Vertical spacing between fields
        
        
        # Define all form fields (label text, field key)
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
                x + 200,  # Position after label
                y, 
                input_width, 
                input_height, 
                self.parent
            )
            
            # Store reference to field
            self.input_fields[field_key] = field
            
            # Connect to update handler (save to model as user types)
            field.textChanged.connect(
                lambda text, key=field_key: self._on_field_changed(key, text)
            )
            
            y += spacing
    
    
    def _on_field_changed(self, field_key: str, text: str):
        # Update customer data model
        setattr(self.customer_data, field_key, text)
    
    def _go_back_to_rooms(self):

        self.stacked_widget.setCurrentIndex(1)
    
    def _confirm_booking(self):
       
        self.stacked_widget.setCurrentIndex(3) 
        
    
    
    def _update_display(self):
        
        room = self.booking_data.selected_room
        
        if room:
            # Display room title and description (multi-line)
            room_text = f"{room['title']}"
            self.room_info_label.setText(room_text)
        else:
            # No room selected
            self.room_info_label.setText("(room details here)")
        
        
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
        
        guests_text = f"Guests: {self.booking_data.adults}"
        self.guests_label.setText(guests_text)

        # Calculate nights from model
        nights = self.booking_data.calculate_nights()
        
        if nights is not None:
            nights_text = f"Nights: {nights}"
        else:
            nights_text = "Nights: (not calculated)"
        
        self.nights_label.setText(nights_text)
    
    def _flash_field_red(self, field):

        # Store original style
        original_style = field.styleSheet()
        
        # Add red border and light red background
        red_style = (
            "border: 3px solid #ff4444; "
            "background-color: #ffebeb;"
        )
        field.setStyleSheet(red_style)
        
        # Remove red styling after 1 second (1000 milliseconds)
        QTimer.singleShot(1000, lambda: field.setStyleSheet(original_style))
    
    
    def _setup_show_event(self):

        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            """Update display when page is shown."""
            self._update_display()
            
            # Call original show event if it exists
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        # Attach show event handler
        self.parent.showEvent = on_show_event