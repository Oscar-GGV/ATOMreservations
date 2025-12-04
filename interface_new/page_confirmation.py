"""
Confirmation Page Module

This module handles the confirmation page display for hotel reservations,
showing booking details and customer information after a successful reservation.
"""

from typing import Optional
from PyQt5.QtWidgets import QWidget, QStackedWidget, QLabel, QPushButton
from models import BookingData, CustomerData
from ui_components import UIFactory, HeaderComponent


class ConfirmationPageConfig:
    """Configuration constants for the confirmation page layout."""
    
    # Layout positioning
    START_X = 650
    START_Y = 250
    TITLE_OFFSET_X = -50
    VERTICAL_SPACING = 50
    
    # Label dimensions
    LABEL_WIDTH = 800
    TITLE_WIDTH = 900
    
    # Button positioning
    BUTTON_X = 1600
    BUTTON_Y = 900
    BUTTON_WIDTH = 280
    BUTTON_HEIGHT = 60
    
    # Styles
    TITLE_STYLE = "font-size: 28px; font-weight: bold; color: black;"
    LABEL_STYLE = "font-size: 14px; color: black;"
    BUTTON_STYLE = "background-color: black; color: white; font-size: 18px;"
    
    # Text constants
    TITLE_TEXT = "Thank You for Your Reservation"
    BUTTON_TEXT = "Make a New Reservation"
    DEFAULT_RESERVATION_ID = "R0001"


class ConfirmationPage:
    """
    Manages the confirmation page UI and displays booking details.
    
    This class creates and manages the confirmation page that shows
    reservation details, customer information, and provides options
    for making new reservations.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """
        Initialize the confirmation page.
        
        Args:
            parent: The parent widget to attach UI components to
            stacked_widget: The stacked widget for page navigation
        """
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self.customer_data = CustomerData()
        
        # UI Components - initialized in _build_ui
        self.confirmation_email_label: Optional[QLabel] = None
        self.reservation_id_label: Optional[QLabel] = None
        self.room_info_label: Optional[QLabel] = None
        self.checkin_label: Optional[QLabel] = None
        self.checkout_label: Optional[QLabel] = None
        self.guests_label: Optional[QLabel] = None
        self.nights_label: Optional[QLabel] = None
        self.guest_name_label: Optional[QLabel] = None
        self.guest_email_label: Optional[QLabel] = None
        self.guest_phone_label: Optional[QLabel] = None
        self.payment_label: Optional[QLabel] = None
        self.new_reservation_button: Optional[QPushButton] = None
        
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the complete user interface for the confirmation page."""
        self._create_header()
        self._create_labels()
        self._create_buttons()
        self._setup_event_handlers()

    def _create_header(self) -> None:
        """Create the page header component."""
        HeaderComponent(self.parent, show_back=False)

    def _create_labels(self) -> None:
        """Create all information labels for the confirmation page."""
        config = ConfirmationPageConfig
        x = config.START_X
        y = config.START_Y
        
        # Title
        title_label = UIFactory.create_label(
            config.TITLE_TEXT,
            x + config.TITLE_OFFSET_X,
            y,
            self.parent,
            config.TITLE_STYLE
        )
        title_label.setFixedWidth(config.TITLE_WIDTH)
        title_label.setWordWrap(True)
        y += config.VERTICAL_SPACING + 10  # Extra spacing after title
        
        # Email confirmation
        self.confirmation_email_label = UIFactory.create_label(
            "A confirmation email was sent to: ",
            x, y, self.parent, config.LABEL_STYLE
        )
        self.confirmation_email_label.setFixedWidth(config.LABEL_WIDTH)
        self.confirmation_email_label.setWordWrap(True)
        y += config.VERTICAL_SPACING
        
        # Reservation details
        self.reservation_id_label = self._create_info_label(
            "Reservation ID: ", x, y
        )
        y += config.VERTICAL_SPACING
        
        self.room_info_label = self._create_info_label(
            "(room details here)", x, y
        )
        y += config.VERTICAL_SPACING
        
        # Check-in/out information
        self.checkin_label = self._create_info_label(
            "Check In: (not selected)", x, y
        )
        y += config.VERTICAL_SPACING
        
        self.checkout_label = self._create_info_label(
            "Check Out: (not selected)", x, y
        )
        y += config.VERTICAL_SPACING
        
        # Guest information
        self.guests_label = self._create_info_label(
            "Guests: (not selected)", x, y
        )
        y += config.VERTICAL_SPACING
        
        self.nights_label = self._create_info_label(
            "Nights: (not calculated)", x, y
        )
        y += config.VERTICAL_SPACING
        
        # Customer details
        self.guest_name_label = self._create_info_label(
            "Guest: (not provided)", x, y
        )
        y += config.VERTICAL_SPACING
        
        self.guest_email_label = self._create_info_label(
            "Email: (not provided)", x, y
        )
        y += config.VERTICAL_SPACING
        
        self.guest_phone_label = self._create_info_label(
            "Phone: (not provided)", x, y
        )
        y += config.VERTICAL_SPACING
        
        # Payment information
        self.payment_label = self._create_info_label(
            "Payment: (not provided)", x, y
        )

    def _create_info_label(self, text: str, x: int, y: int, width: int = None) -> QLabel:
        """
        Create a standard information label with proper width.
        
        Args:
            text: The label text
            x: X coordinate
            y: Y coordinate
            width: Width of the label (default: uses config value)
            
        Returns:
            The created QLabel widget
        """
        if width is None:
            width = ConfirmationPageConfig.LABEL_WIDTH
            
        label = UIFactory.create_label(
            text, x, y, self.parent, ConfirmationPageConfig.LABEL_STYLE
        )
        label.setFixedWidth(width)
        label.setWordWrap(True)  # Enable word wrapping for long text
        return label

    def _create_buttons(self) -> None:
        """Create action buttons for the confirmation page."""
        config = ConfirmationPageConfig
        
        self.new_reservation_button = UIFactory.create_button(
            config.BUTTON_TEXT,
            config.BUTTON_X,
            config.BUTTON_Y,
            config.BUTTON_WIDTH,
            config.BUTTON_HEIGHT,
            self.parent,
            config.BUTTON_STYLE
        )

    def _setup_event_handlers(self) -> None:
        """Set up all event handlers and callbacks."""
        self.new_reservation_button.clicked.connect(self._handle_new_reservation)
        self._setup_show_event()

    def _setup_show_event(self) -> None:
        """Set up the show event to update display when page becomes visible."""
        original_show = self.parent.showEvent

        def on_show(event):
            """Handle the show event by updating the display."""
            self._update_display()
            if original_show:
                try:
                    original_show(event)
                except Exception:
                    # Silently handle any errors from original show event
                    pass

        self.parent.showEvent = on_show

    def _update_display(self) -> None:
        """Update all labels with current booking and customer data."""
        self._update_email_confirmation()
        self._update_reservation_info()
        self._update_room_info()
        self._update_checkin_checkout()
        self._update_guest_count()
        self._update_nights()
        self._update_customer_details()
        self._update_payment_info()

    def _update_email_confirmation(self) -> None:
        """Update the email confirmation label."""
        if self.customer_data.email:
            text = f"A confirmation email was sent to: {self.customer_data.email}"
        else:
            text = "A confirmation email was sent to: (not provided)"
        self.confirmation_email_label.setText(text)

    def _update_reservation_info(self) -> None:
        """Update the reservation ID label."""
        reservation_id = getattr(
            self.booking_data,
            'reservation_id',
            ConfirmationPageConfig.DEFAULT_RESERVATION_ID
        )
        self.reservation_id_label.setText(f"Reservation ID: {reservation_id}")

    def _update_room_info(self) -> None:
        """Update the room information label."""
        room = self.booking_data.selected_room
        if room:
            self.room_info_label.setText(f"Room: {room['title']}")
        else:
            self.room_info_label.setText("Room: (not selected)")

    def _update_checkin_checkout(self) -> None:
        """Update check-in and check-out labels."""
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

    def _update_guest_count(self) -> None:
        """Update the number of guests label."""
        self.guests_label.setText(f"Guests: {self.booking_data.adults}")

    def _update_nights(self) -> None:
        """Update the number of nights label."""
        nights = self.booking_data.calculate_nights()
        if nights is not None:
            self.nights_label.setText(f"Nights: {nights}")
        else:
            self.nights_label.setText("Nights: (not calculated)")

    def _update_customer_details(self) -> None:
        """Update customer name, email, and phone labels."""
        # Full name
        first = self.customer_data.first_name or ""
        last = self.customer_data.last_name or ""
        full_name = (first + " " + last).strip()
        
        if full_name:
            self.guest_name_label.setText(f"Guest: {full_name}")
        else:
            self.guest_name_label.setText("Guest: (not provided)")
        
        # Email
        if self.customer_data.email:
            self.guest_email_label.setText(f"Email: {self.customer_data.email}")
        else:
            self.guest_email_label.setText("Email: (not provided)")
        
        # Phone
        if self.customer_data.phone:
            self.guest_phone_label.setText(f"Phone: {self.customer_data.phone}")
        else:
            self.guest_phone_label.setText("Phone: (not provided)")

    def _update_payment_info(self) -> None:
        """Update the payment information label."""
        card = getattr(self.customer_data, 'card_number', '')
        if card and len(card) >= 4:
            last_four = card[-4:]
            self.payment_label.setText(f"Payment: ******{last_four}")
        else:
            self.payment_label.setText("Payment: (not provided)")

    def _handle_new_reservation(self) -> None:
        """Handle the 'Make a New Reservation' button click."""
        self.booking_data.reset()
        self.stacked_widget.setCurrentIndex(0)