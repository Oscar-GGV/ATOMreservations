from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QDate, QTimer
from models import BookingData
from ui_components import UIFactory, HeaderComponent, GuestCounter

class HomePage:
    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self._build_ui()
    
    def _build_ui(self):
        HeaderComponent(self.parent, show_back=False)
        
        UIFactory.create_label("HOTEL", 370, 300, self.parent,
                               "color: black; font-size: 30px; font-weight: bold;")
        UIFactory.create_label("ELEON", 320, 325, self.parent,
                               "color: black; font-size: 60px; font-weight: bold;")
        
        self.calendar = UIFactory.create_calendar(690, 425, 500, 250, self.parent)
        self.calendar.hide()
        self.calendar.clicked.connect(self._on_date_selected)
        
        self.checkin_button = UIFactory.create_button("Check In:        ", 650, 300, 300, 100, self.parent)
        self.checkin_button.clicked.connect(self._toggle_calendar)
        
        self.checkout_button = UIFactory.create_button("Check Out:        ", 950, 300, 300, 100, self.parent)
        self.checkout_button.clicked.connect(self._toggle_calendar)
        
        self.guests_button = UIFactory.create_button("Guests: 1", 1250, 300, 300, 100, self.parent)
        
        self.guest_counter = GuestCounter(1275, 425, 250, 100, self.parent,
                                          on_change=self._on_guest_count_changed)
        self.guests_button.clicked.connect(self.guest_counter.toggle)
        
        self.availability_button = UIFactory.create_button(
            "Check Availability", 1550, 300, 300, 100, self.parent,
            "background-color: black; color: white; font-size: 20px;"
        )
        self.availability_button.clicked.connect(self._check_availability)
        
        self._setup_show_event()
    
    def _toggle_calendar(self):
        self.calendar.setVisible(not self.calendar.isVisible())
    
    def _on_date_selected(self, date: QDate):
        formatted_date = date.toString("yyyy-MM-dd")
        
        if self.booking_data.check_in is None:
            self.booking_data.check_in = formatted_date
        
        elif self.booking_data.check_out is None:
            d1 = QDate.fromString(self.booking_data.check_in, "yyyy-MM-dd")
            d2 = QDate.fromString(formatted_date, "yyyy-MM-dd")
            if d2 < d1:
                self.booking_data.check_out = self.booking_data.check_in
                self.booking_data.check_in = formatted_date
            else:
                self.booking_data.check_out = formatted_date
        
        else:
            self.booking_data.check_in = formatted_date
            self.booking_data.check_out = None
        
        self._update_date_buttons()
    
    def _on_guest_count_changed(self, count: int):
        self.booking_data.adults = count
        self.guests_button.setText(f"Guests: {count}")
    
    def _check_availability(self):
        if not self.booking_data.check_in or not self.booking_data.check_out:
            self._flash_red_buttons()
            return
        
        self.stacked_widget.setCurrentIndex(1)
    
    def _update_date_buttons(self):
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
        red_style = "border: 3px solid #ff4444; background-color: #ffebeb;"
        self.checkin_button.setStyleSheet(red_style)
        self.checkout_button.setStyleSheet(red_style)
        
        QTimer.singleShot(1000, lambda: self.checkin_button.setStyleSheet(""))
        QTimer.singleShot(1000, lambda: self.checkout_button.setStyleSheet(""))
    
    def _setup_show_event(self):
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
