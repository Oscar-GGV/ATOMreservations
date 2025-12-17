import sys
import os

# Add parent directory to path to access backend folder
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QTimer

from models import BookingData, CustomerData
from ui_components import UIFactory, HeaderComponent
from backend.customer_controller import CustomerController
from backend.reservation_controller import ReservationController
from backend.reservation_system import ReservationSystem
from backend.address import Address
from backend.customer import Customer


class CheckoutPage:
    """
    Checkout screen.

    - Shows booking summary
    - Collects customer info, address, payment
    - Uses LoginPage data to auto fill if available
    - Saves reservation using backend
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget, login_page=None):
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.login_page = login_page

        self.booking_data = BookingData()
        self.customer_data = CustomerData()
        self.input_fields = {}

        self.room_info_label = None
        self.checkin_label = None
        self.checkout_label = None
        self.guests_label = None
        self.nights_label = None
        self.total_label = None  # ADDED

        # Backend
        try:
            self.customer_controller = CustomerController()
            self.reservation_system = ReservationSystem()
            self.reservation_controller = ReservationController(
                self.customer_controller,
                self.reservation_system
            )
        except Exception as e:
            print(f"WARNING: Backend initialization failed: {e}")
            self.customer_controller = None
            self.reservation_system = None
            self.reservation_controller = None

        self._build_ui()
        self._setup_show_event()

    def _build_ui(self):
        HeaderComponent(
            self.parent,
            show_back=True,
            back_callback=self._go_back_to_login
        )

        # Booking summary on the right
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
        # ADDED - Total price label
        self.total_label = UIFactory.create_label(
            "Total: (not calculated)", 1600, 450, self.parent,
            "font-size: 16px; color: black;"
        )

        self._create_customer_form()

        # Confirm button
        self.confirm_button = UIFactory.create_button(
            "Confirm Booking",
            1600, 900,
            280, 60,
            self.parent,
            "background-color: black; color: white; font-size: 18px;"
        )
        self.confirm_button.clicked.connect(self._confirm_booking)

        self.parent.setMinimumHeight(1200)

    def _create_customer_form(self):
        input_width = 400
        input_height = 40
        spacing = 60

        # Personal info
        x_left = 156
        y_left = 250

        UIFactory.create_label(
            "Personal Information", x_left, y_left, self.parent,
            "font-size: 18px; font-weight: bold; color: black;"
        )
        y_left += 50

        personal_fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Date of Birth:", "date_of_birth"),
        ]

        for label_text, field_key in personal_fields:
            label = UIFactory.create_label(label_text, x_left, y_left, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")

            field = UIFactory.create_input_field(
                x_left + 200, y_left, input_width, input_height, self.parent
            )

            self.input_fields[field_key] = field
            field.textChanged.connect(
                lambda text, k=field_key: self._on_field_changed(k, text)
            )

            y_left += spacing

        # Billing address
        x_middle = 800
        y_middle = 250

        UIFactory.create_label(
            "Billing Address", x_middle, y_middle, self.parent,
            "font-size: 18px; font-weight: bold; color: black;"
        )
        y_middle += 50

        address_fields = [
            ("Country/Territory:", "country"),
            ("Street:", "street"),
            ("City:", "city"),
            ("State:", "state"),
            ("Zip Code:", "zip_code"),
        ]

        for label_text, field_key in address_fields:
            label = UIFactory.create_label(label_text, x_middle, y_middle, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")

            field = UIFactory.create_input_field(
                x_middle + 200, y_middle, input_width, input_height, self.parent
            )

            self.input_fields[field_key] = field
            field.textChanged.connect(
                lambda text, k=field_key: self._on_field_changed(k, text)
            )

            y_middle += spacing

        # Payment
        y_bottom = max(y_left, y_middle) + 40
        x_bottom = 150

        UIFactory.create_label(
            "Payment", x_bottom, y_bottom, self.parent,
            "font-size: 18px; font-weight: bold; color: black;"
        )
        y_bottom += 50

        payment_fields = [
            ("Name on Card:", "card_name"),
            ("Card Number:", "card_number"),
            ("Exp. Date (MM/YY):", "exp_date"),
            ("CVV:", "cvv"),
        ]

        for label_text, field_key in payment_fields:
            label = UIFactory.create_label(label_text, x_bottom, y_bottom, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")

            field = UIFactory.create_input_field(
                x_bottom + 200, y_bottom, input_width, input_height, self.parent
            )

            self.input_fields[field_key] = field
            field.textChanged.connect(
                lambda text, k=field_key: self._on_field_changed(k, text)
            )

            y_bottom += spacing

    def _on_field_changed(self, field_key, text):
        setattr(self.customer_data, field_key, text)

    def _auto_fill_from_login(self):
        if not self.login_page:
            return

        user = self.login_page.get_current_user()
        if not user:
            return

        if user.get("first_name"):
            self.input_fields["first_name"].setText(user["first_name"])
        if user.get("last_name"):
            self.input_fields["last_name"].setText(user["last_name"])
        if user.get("email"):
            self.input_fields["email"].setText(user["email"])
        if user.get("phone"):
            self.input_fields["phone"].setText(user["phone"])

    def _go_back_to_login(self):
        self.stacked_widget.setCurrentIndex(2)

    def _confirm_booking(self):
        required_fields = [
            "first_name", "last_name", "email", "phone", "date_of_birth",
            "card_name", "card_number", "exp_date", "cvv",
            "country", "street", "city", "state", "zip_code",
        ]

        has_empty = False

        for key in required_fields:
            value = getattr(self.customer_data, key, "")
            if not value or value.strip() == "":
                has_empty = True
                if key in self.input_fields:
                    self._flash_field_red(self.input_fields[key])

        if has_empty:
            print("DEBUG: Empty required fields")
            return

        # Save reservation
        self._save_reservation_to_backend()

        # Go to confirmation page
        self.stacked_widget.setCurrentIndex(4)

    def _save_reservation_to_backend(self):
        if not self.reservation_controller:
            # Backend not available: fake ID
            import random
            self.booking_data.reservation_id = f"R{random.randint(1000, 9999)}"
            print("WARNING: Backend unavailable, fake reservation ID set")
            return

        if not self.booking_data.selected_room:
            print("ERROR: No selected room")
            return

        if not self.booking_data.check_in or not self.booking_data.check_out:
            print("ERROR: Missing check-in or check-out")
            return

        # BUG FIX: Changed 'zip_code' to 'zipcode'
        address = Address(
            street=self.customer_data.street,
            city=self.customer_data.city,
            state=self.customer_data.state,
            zipcode=self.customer_data.zip_code,
            country=self.customer_data.country,
        )

        customer = Customer(
            first_name=self.customer_data.first_name,
            last_name=self.customer_data.last_name,
            email=self.customer_data.email,
            phone=self.customer_data.phone,
            address=address,
        )

        check_in = self._date_to_tuple(self.booking_data.check_in)
        check_out = self._date_to_tuple(self.booking_data.check_out)
        room_type = self.booking_data.selected_room["title"]

        try:
            result = self.reservation_controller.make_reservation(
                customer=customer,
                room_type=room_type,
                check_in=check_in,
                check_out=check_out,
            )
            if isinstance(result, dict) and result.get("status") == "success":
                self.booking_data.reservation_id = result.get("reservation_id")
            else:
                print("WARNING: Unexpected reservation result:", result)
        except Exception as e:
            print(f"ERROR saving reservation: {e}")
            import random
            self.booking_data.reservation_id = f"R{random.randint(1000, 9999)}"

    def _date_to_tuple(self, date_string):
        try:
            if not date_string:
                raise ValueError("Empty date string")
            parts = date_string.split("-")
            if len(parts) != 3:
                raise ValueError(f"Invalid date format: {date_string}")
            month = int(parts[1])
            day = int(parts[2])
            return (month, day)
        except Exception as e:
            print(f"ERROR: Failed to convert date '{date_string}': {e}")
            return (1, 1)

    def _update_display(self):
        room = self.booking_data.selected_room

        if room:
            text = f"{room['title']}\n{room['description']}"
            self.room_info_label.setText(text)
        else:
            self.room_info_label.setText("(room details here)")

        if self.booking_data.check_in:
            self.checkin_label.setText(f"Check In: {self.booking_data.check_in}")
        else:
            self.checkin_label.setText("Check In: (not selected)")

        if self.booking_data.check_out:
            self.checkout_label.setText(f"Check Out: {self.booking_data.check_out}")
        else:
            self.checkout_label.setText("Check Out: (not selected)")

        self.guests_label.setText(f"Guests: {self.booking_data.adults}")

        nights = self.booking_data.calculate_nights()
        if nights is not None:
            self.nights_label.setText(f"Nights: {nights}")
        else:
            self.nights_label.setText("Nights: (not calculated)")

        # ADDED - Display total price
        total = self.booking_data.calculate_total_price()
        if total is not None:
            self.total_label.setText(f"Total: ${total:.2f}")
        else:
            self.total_label.setText("Total: (not calculated)")

    def _flash_field_red(self, field):
        original_style = field.styleSheet()
        red_style = "border: 3px solid #ff4444; background-color: #ffebeb;"
        field.setStyleSheet(red_style)
        QTimer.singleShot(1000, lambda: field.setStyleSheet(original_style))

    def _setup_show_event(self):
        original_show = self.parent.showEvent

        def on_show(event):
            self._update_display()
            self._auto_fill_from_login()

            if original_show:
                try:
                    original_show(event)
                except:
                    pass

        self.parent.showEvent = on_show