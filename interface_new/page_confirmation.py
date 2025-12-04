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
        
        x = 650
        y = 250
        spacing = 50
        
        # Title
        title_label = UIFactory.create_label(
            "Thank You for Your Reservation",
            x - 50, y, self.parent,
            "font-size: 28px; font-weight: bold; color: black;"
        )
        title_label.setFixedWidth(900)
        title_label.setWordWrap(True)
        y += spacing + 10
        
        # Email confirmation
        self.confirmation_email_label = UIFactory.create_label(
            "A confirmation email was sent to: ",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.confirmation_email_label.setFixedWidth(800)
        self.confirmation_email_label.setWordWrap(True)
        y += spacing
        
        # Reservation ID
        self.reservation_id_label = UIFactory.create_label(
            "Reservation ID: ",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.reservation_id_label.setFixedWidth(800)
        y += spacing
        
        # Room info
        self.room_info_label = UIFactory.create_label(
            "Room: (not selected)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.room_info_label.setFixedWidth(800)
        y += spacing
        
        # Check-in
        self.checkin_label = UIFactory.create_label(
            "Check In: (not selected)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.checkin_label.setFixedWidth(800)
        y += spacing
        
        # Check-out
        self.checkout_label = UIFactory.create_label(
            "Check Out: (not selected)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.checkout_label.setFixedWidth(800)
        y += spacing
        
        # Guests
        self.guests_label = UIFactory.create_label(
            "Guests: (not selected)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.guests_label.setFixedWidth(800)
        y += spacing
        
        # Nights
        self.nights_label = UIFactory.create_label(
            "Nights: (not calculated)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.nights_label.setFixedWidth(800)
        y += spacing
        
        # Guest name
        self.guest_name_label = UIFactory.create_label(
            "Guest: (not provided)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.guest_name_label.setFixedWidth(800)
        y += spacing
        
        # Guest email
        self.guest_email_label = UIFactory.create_label(
            "Email: (not provided)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.guest_email_label.setFixedWidth(800)
        y += spacing
        
        # Guest phone
        self.guest_phone_label = UIFactory.create_label(
            "Phone: (not provided)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.guest_phone_label.setFixedWidth(800)
        y += spacing
        
        # Payment
        self.payment_label = UIFactory.create_label(
            "Payment: (not provided)",
            x, y, self.parent,
            "font-size: 14px; color: black;"
        )
        self.payment_label.setFixedWidth(800)
        
        # New reservation button
        self.new_reservation_button = UIFactory.create_button(
            "Make a New Reservation",
            1600, 900, 280, 60, self.parent,
            "background-color: black; color: white; font-size: 18px;"
        )
        self.new_reservation_button.clicked.connect(self._make_new)
        
        self._setup_show_event()
    
    def _update_display(self):
        # Email confirmation
        if self.customer_data.email:
            text = f"A confirmation email was sent to: {self.customer_data.email}"
        else:
            text = "A confirmation email was sent to: (not provided)"
        self.confirmation_email_label.setText(text)
        
        # Reservation ID
        reservation_id = getattr(self.booking_data, 'reservation_id', 'R0001')
        self.reservation_id_label.setText(f"Reservation ID: {reservation_id}")
        
        # Room
        room = self.booking_data.selected_room
        if room:
            self.room_info_label.setText(f"Room: {room['title']}")
        else:
            self.room_info_label.setText("Room: (not selected)")
        
        # Check-in
        if self.booking_data.check_in:
            self.checkin_label.setText(
                f"Check In: {self.booking_data.check_in} after 4:00 PM"
            )
        else:
            self.checkin_label.setText("Check In: (not selected)")
        
        # Check-out
        if self.booking_data.check_out:
            self.checkout_label.setText(
                f"Check Out: {self.booking_data.check_out} before 11:00 AM"
            )
        else:
            self.checkout_label.setText("Check Out: (not selected)")
        
        # Guests
        self.guests_label.setText(f"Guests: {self.booking_data.adults}")
        
        # Nights
        nights = self.booking_data.calculate_nights()
        if nights is not None:
            self.nights_label.setText(f"Nights: {nights}")
        else:
            self.nights_label.setText("Nights: (not calculated)")
        
        # Guest name
        first = self.customer_data.first_name or ""
        last = self.customer_data.last_name or ""
        full_name = (first + " " + last).strip()
        
        if full_name:
            self.guest_name_label.setText(f"Guest: {full_name}")
        else:
            self.guest_name_label.setText("Guest: (not provided)")
        
        # Guest email
        if self.customer_data.email:
            self.guest_email_label.setText(f"Email: {self.customer_data.email}")
        else:
            self.guest_email_label.setText("Email: (not provided)")
        
        # Guest phone
        if self.customer_data.phone:
            self.guest_phone_label.setText(f"Phone: {self.customer_data.phone}")
        else:
            self.guest_phone_label.setText("Phone: (not provided)")
        
        # Payment
        card = getattr(self.customer_data, 'card_number', '')
        if card and len(card) >= 4:
            last_four = card[-4:]
            self.payment_label.setText(f"Payment: ******{last_four}")
        else:
            self.payment_label.setText("Payment: (not provided)")
    
    def _make_new(self):
        # Save dates and guests
        saved_check_in = self.booking_data.check_in
        saved_check_out = self.booking_data.check_out
        saved_adults = self.booking_data.adults
        
        # Reset booking
        self.booking_data.reset()
        
        # Restore dates and guests
        self.booking_data.check_in = saved_check_in
        self.booking_data.check_out = saved_check_out
        self.booking_data.adults = saved_adults
        
        # Go to home
        self.stacked_widget.setCurrentIndex(0)
    
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