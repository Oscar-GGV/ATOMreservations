"""page_checkout.py
This file creates the checkout page where users enter their personal information.
It shows a booking summary and collects customer details through a form.

Programmers: Astghik, Mahi
Date of code: November 8th, 2025
Modified: December 3rd, 2025 - Reorganized layout with overlapping sections

Description:
This page (index 3) displays the checkout form with Personal Information on left,
Billing Address in the middle overlapping, Payment at bottom, and booking summary
on the right side.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QTimer
from models import BookingData, CustomerData
from ui_components import UIFactory, HeaderComponent


class CheckoutPage:
    
    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget, login_page=None):
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self.customer_data = CustomerData()
        self.input_fields = {}
        self.login_page = login_page
        self._build_ui()
    
    def _build_ui(self):
        HeaderComponent(
            self.parent, 
            show_back=True, 
            back_callback=self._go_back_to_login
        )
        
        # Right side - booking summary (stays same as original)
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
        
        self._create_customer_form()
        
        # Confirm button at original position
        self.confirm_button = UIFactory.create_button(
            "Confirm Booking", 
            1600, 900, 
            280, 60, 
            self.parent
        )
        self.confirm_button.clicked.connect(self._confirm_booking)
        
        # Set minimum height for scrolling
        self.parent.setMinimumHeight(1200)
        
        self._setup_show_event()
    
    def _create_customer_form(self):
        input_width = 400
        input_height = 40
        spacing = 60
        
        # LEFT SIDE - Section 1: Personal Information
        x_left = 156
        y_left = 250
        
        section_header = UIFactory.create_label(
            "Personal Information", x_left, y_left, self.parent,
            "font-size: 18px; font-weight: bold; color: black;"
        )
        y_left += 50
        
        personal_fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Date of Birth:", "date_of_birth")
        ]
        
        for label_text, field_key in personal_fields:
            label = UIFactory.create_label(label_text, x_left, y_left, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")
            
            field = UIFactory.create_input_field(
                x_left + 200,
                y_left, 
                input_width, 
                input_height, 
                self.parent
            )
            
            self.input_fields[field_key] = field
            
            field.textChanged.connect(
                lambda text, key=field_key: self._on_field_changed(key, text)
            )
            
            y_left += spacing
        
        # MIDDLE - Section 3: Billing Address (overlapping with Personal Info)
        x_middle = 800
        y_middle = 250
        
        section_header = UIFactory.create_label(
            "Billing Address", x_middle, y_middle, self.parent,
            "font-size: 18px; font-weight: bold; color: black;"
        )
        y_middle += 50
        
        address_fields = [
            ("Country/Territory:", "country"),
            ("Street:", "street"),
            ("City:", "city"),
            ("State:", "state"),
            ("Zip Code:", "zip_code")
        ]
        
        for label_text, field_key in address_fields:
            label = UIFactory.create_label(label_text, x_middle, y_middle, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")
            
            field = UIFactory.create_input_field(
                x_middle + 200,
                y_middle, 
                input_width, 
                input_height, 
                self.parent
            )
            
            self.input_fields[field_key] = field
            
            field.textChanged.connect(
                lambda text, key=field_key: self._on_field_changed(key, text)
            )
            
            y_middle += spacing
        
        # BOTTOM LEFT - Section 2: Payment
        y_bottom = max(y_left, y_middle) + 40  # Start after both columns
        x_bottom = 150
        
        section_header = UIFactory.create_label(
            "Payment", x_bottom, y_bottom, self.parent,
            "font-size: 18px; font-weight: bold; color: black;"
        )
        y_bottom += 50
        
        payment_fields = [
            ("Name on Card:", "card_name"),
            ("Card Number:", "card_number"),
            ("Exp. Date (MM/YY):", "exp_date"),
            ("CVV:", "cvv")
        ]
        
        for label_text, field_key in payment_fields:
            label = UIFactory.create_label(label_text, x_bottom, y_bottom, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")
            
            field = UIFactory.create_input_field(
                x_bottom + 200,
                y_bottom, 
                input_width, 
                input_height, 
                self.parent
            )
            
            self.input_fields[field_key] = field
            
            field.textChanged.connect(
                lambda text, key=field_key: self._on_field_changed(key, text)
            )
            
            y_bottom += spacing
    
    def _on_field_changed(self, field_key, text):
        """Saves input to CustomerData."""
        setattr(self.customer_data, field_key, text)
    
    def _auto_fill_from_login(self):
        """Auto-fill from logged-in user."""
        if not self.login_page:
            return
        
        user = self.login_page.get_current_user()
        if not user:
            return
        
        if user.get('first_name'):
            self.input_fields['first_name'].setText(user['first_name'])
        
        if user.get('last_name'):
            self.input_fields['last_name'].setText(user['last_name'])
        
        if user.get('email'):
            self.input_fields['email'].setText(user['email'])
        
        if user.get('phone') and user['phone']:
            self.input_fields['phone'].setText(user['phone'])
    
    def _go_back_to_login(self):
        """Go back to login page."""
        self.stacked_widget.setCurrentIndex(2)
    
    def _confirm_booking(self):
        required_fields = [
            "first_name", "last_name", "email", "phone", "date_of_birth",
            "card_name", "card_number", "exp_date", "cvv",
            "country", "street", "city", "state", "zip_code"
        ]
        
        has_empty_fields = False
        
        for field_key in required_fields:
            field_value = getattr(self.customer_data, field_key, "")
            
            if not field_value or field_value.strip() == "":
                has_empty_fields = True
                
                if field_key in self.input_fields:
                    self._flash_field_red(self.input_fields[field_key])
        
        if has_empty_fields:
            return
        
        self.stacked_widget.setCurrentIndex(4)
    
    def _update_display(self):
        room = self.booking_data.selected_room
        
        if room:
            room_text = f"{room['title']}\n{room['description']}"
            self.room_info_label.setText(room_text)
        else:
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
        
        nights = self.booking_data.calculate_nights()
        
        if nights is not None:
            nights_text = f"Nights: {nights}"
        else:
            nights_text = "Nights: (not calculated)"
        
        self.nights_label.setText(nights_text)
    
    def _flash_field_red(self, field):
        original_style = field.styleSheet()
        
        red_style = (
            "border: 3px solid #ff4444; "
            "background-color: #ffebeb;"
        )
        field.setStyleSheet(red_style)
        
        QTimer.singleShot(1000, lambda: field.setStyleSheet(original_style))
    
    def _setup_show_event(self):
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            self._update_display()
            self._auto_fill_from_login()
            
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        self.parent.showEvent = on_show_event