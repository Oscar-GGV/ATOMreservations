from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QDate, QTimer
from models import BookingData
from ui_components import UIFactory, HeaderComponent, GuestCounter

class HomePage:
    
    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
      
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()  # Model (Singleton)
        
        self._build_ui()
    
    
    def _build_ui(self):
        
        # Create header without back button (home page)
        HeaderComponent(self.parent, show_back=False)
        
        # "HOTEL" text (smaller, above ELEON)
        UIFactory.create_label(
            "HOTEL", 370, 300, self.parent,
            "color: black; font-size: 30px; font-weight: bold;"
        )
        
        # "ELEON" text (large brand name)
        UIFactory.create_label(
            "ELEON", 320, 325, self.parent,
            "color: black; font-size: 60px; font-weight: bold;"
        )
        
        
        # Create calendar (hidden by default, shown when date button clicked)
        self.calendar = UIFactory.create_calendar(690, 425, 500, 250, self.parent)
        self.calendar.hide()
        
        self.calendar.clicked.connect(self._on_date_selected)
        
        # Check-in button
        self.checkin_button = UIFactory.create_button(
            "Check In:        ", 650, 300, 300, 100, self.parent
        )
        self.checkin_button.clicked.connect(self._toggle_calendar)
        
        # Check-out button
        self.checkout_button = UIFactory.create_button(
            "Check Out:        ", 950, 300, 300, 100, self.parent
        )
        self.checkout_button.clicked.connect(self._toggle_calendar)
        
        #-----

        # Guests button (shows counter when clicked)
        self.guests_button = UIFactory.create_button(
            "Guests: 1", 1250, 300, 300, 100, self.parent
        )
        
        # Guest counter component (popup)
        self.guest_counter = GuestCounter(
            1275, 425, 250, 100, self.parent, 
            on_change=self._on_guest_count_changed #Any time the number changes
        )
        
        # Toggle guest counter visibility
        self.guests_button.clicked.connect(self.guest_counter.toggle)

        #----

        # Black button to proceed to room selection
        self.availability_button = UIFactory.create_button(
            "Check Availability", 1550, 300, 300, 100, self.parent,
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