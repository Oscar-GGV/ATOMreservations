from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QDate, QTimer
from models import BookingData
from ui_components import UIFactory, HeaderComponent, GuestCounter
from main import get_Nx, get_Ny  # Import functions to access Nx, Ny


class HomePage:
    
    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
      
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()  # Model (Singleton)
        
        self._build_ui()
    
    
    def _build_ui(self):
        
        Nx = get_Nx()
        Ny = get_Ny()
        
        # Create header without back button (home page)
        HeaderComponent(self.parent, show_back=False)
        
        # "HOTEL" text (smaller, above ELEON)
        # Original: (370, 300)
        # 370/1920 = 0.193, 300/1080 = 0.278
        UIFactory.create_label(
            "HOTEL", int(Nx / 5.19), int(Ny / 3.6), self.parent,
            "color: black; font-size: 30px; font-weight: bold;"
        )
        
        # "ELEON" text (large brand name)
        # Original: (320, 325)
        # 320/1920 = 0.167, 325/1080 = 0.301
        UIFactory.create_label(
            "ELEON", int(Nx / 6), int(Ny / 3.32), self.parent,
            "color: black; font-size: 60px; font-weight: bold;"
        )
        
        
        # Create calendar (hidden by default, shown when date button clicked)
        # Original: (690, 425, 500, 250)
        # 690/1920 = 0.359, 425/1080 = 0.394, 500/1920 = 0.260, 250/1080 = 0.231
        self.calendar = UIFactory.create_calendar(
            int(Nx / 2.78), int(Ny / 2.54), int(Nx / 3.84), int(Ny / 4.32), self.parent
        )
        self.calendar.hide()
        
        self.calendar.clicked.connect(self._on_date_selected)
        
        # Check-in button
        # Original: (650, 300, 300, 100)
        # 650/1920 = 0.339, 300/1080 = 0.278, 300/1920 = 0.156, 100/1080 = 0.093
        self.checkin_button = UIFactory.create_button(
            "Check In:        ", int(Nx / 2.95), int(Ny / 3.6), int(Nx / 6.4), int(Ny / 10.8), self.parent
        )
        self.checkin_button.clicked.connect(self._toggle_calendar)
        
        # Check-out button
        # Original: (950, 300, 300, 100)
        # 950/1920 = 0.495, 300/1080 = 0.278, 300/1920 = 0.156, 100/1080 = 0.093
        self.checkout_button = UIFactory.create_button(
            "Check Out:        ", int(Nx / 2.02), int(Ny / 3.6), int(Nx / 6.4), int(Ny / 10.8), self.parent
        )
        self.checkout_button.clicked.connect(self._toggle_calendar)
        
        #-----

        # Guests button (shows counter when clicked)
        # Original: (1250, 300, 300, 100)
        # 1250/1920 = 0.651, 300/1080 = 0.278, 300/1920 = 0.156, 100/1080 = 0.093
        self.guests_button = UIFactory.create_button(
            "Guests: 1", int(Nx / 1.54), int(Ny / 3.6), int(Nx / 6.4), int(Ny / 10.8), self.parent
        )
        
        # Guest counter component (popup)
        # Original: (1275, 425, 250, 100)
        # 1275/1920 = 0.664, 425/1080 = 0.394, 250/1920 = 0.130, 100/1080 = 0.093
        self.guest_counter = GuestCounter(
            int(Nx / 1.51), int(Ny / 2.54), int(Nx / 7.68), int(Ny / 10.8), self.parent, 
            on_change=self._on_guest_count_changed #Any time the number changes
        )
        
        # Toggle guest counter visibility
        self.guests_button.clicked.connect(self.guest_counter.toggle)

        #----

        # Black button to proceed to room selection
        # Original: (1550, 300, 300, 100)
        # 1550/1920 = 0.807, 300/1080 = 0.278, 300/1920 = 0.156, 100/1080 = 0.093
        self.availability_button = UIFactory.create_button(
            "Check Availability", int(Nx / 1.24), int(Ny / 3.6), int(Nx / 6.4), int(Ny / 10.8), self.parent,
            "background-color: black; color: white; font-size: 20px;"
        )
        self.availability_button.clicked.connect(self._check_availability)
        
        
        # Setup show event to hide popups when returning to page
        self._setup_show_event()
    

    
    def _toggle_calendar(self):

        self.calendar.setVisible(not self.calendar.isVisible())
    
    def _on_date_selected(self, date: QDate):

        formatted_date = date.toString("yyyy-MM-dd")
        
        # First selection: set check-in
        if self.booking_data.check_in is None:
            self.booking_data.check_in = formatted_date
            
        # Second selection: set check-out
        elif self.booking_data.check_out is None:
            d1 = QDate.fromString(self.booking_data.check_in, "yyyy-MM-dd")
            d2 = QDate.fromString(formatted_date, "yyyy-MM-dd")
            
            # Ensure check-out is after check-in (swap if needed)
            if d2 < d1:
                self.booking_data.check_out = self.booking_data.check_in
                self.booking_data.check_in = formatted_date
            else:
                self.booking_data.check_out = formatted_date
        
        # Both dates set: reset and start new selection
        else:
            self.booking_data.check_in = formatted_date
            self.booking_data.check_out = None
        
        # Update UI to show selected dates
        self._update_date_buttons()
    
    def _on_guest_count_changed(self, count: int):
     
        # Update model
        self.booking_data.adults = count
        
        # Update button text
        self.guests_button.setText(f"Guests: {count}")
    
    def _check_availability(self):

        # Check if both dates are selected
        if not self.booking_data.check_in or not self.booking_data.check_out:
            # Flash red on both date buttons
            self._flash_red_buttons()
            return  # Don't navigate
        
        
        # Both dates are selected, proceed to room selection
        self.stacked_widget.setCurrentIndex(1)

    
    def _update_date_buttons(self):

        # Check-in button text
        if self.booking_data.check_in:
            checkin_text = f"Check In: {self.booking_data.check_in}"
        else:
            checkin_text = "Check In:        "
        
        # Check-out button text
        if self.booking_data.check_out:
            checkout_text = f"Check Out: {self.booking_data.check_out}"
        else:
            checkout_text = "Check Out:        "
        
        # Update buttons
        self.checkin_button.setText(checkin_text)
        self.checkout_button.setText(checkout_text)
    
    def _flash_red_buttons(self):
  

        # Red style for error state
        red_style = (
            "border: 3px solid #ff4444; "
            "background-color: #ffebeb;"
        )
        
        # Apply red style to both date buttons
        self.checkin_button.setStyleSheet(red_style)
        self.checkout_button.setStyleSheet(red_style)
        
        
        # Remove styling after 1000ms (1 second)
        QTimer.singleShot(1000, lambda: self.checkin_button.setStyleSheet(""))
        QTimer.singleShot(1000, lambda: self.checkout_button.setStyleSheet(""))
    
    
    def _setup_show_event(self):

        original_show_event = self.parent.showEvent ## inherited from QWidget
        
        def on_show_event(event):
            """Hide popups when page is shown."""
            self.calendar.hide()
            self.guest_counter.hide()
            
            # Call original show event if it exists
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        # Attach show event handler
        self.parent.showEvent = on_show_event