from PyQt5.QtWidgets import QWidget, QStackedWidget
from models import BookingData, RoomRepository
from ui_components import UIFactory, HeaderComponent, RoomCard


class RoomSelectionPage:
    
    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self._build_ui()
    
    def _build_ui(self):
        # Header with back button
        HeaderComponent(
            self.parent, 
            show_back=True, 
            back_callback=self._go_back_to_home
        )
        
        # Booking summary labels
        self.checkin_label = UIFactory.create_label(
            "Check In: (not selected)", 50, 200, self.parent
        )
        
        self.checkout_label = UIFactory.create_label(
            "Check Out: (not selected)", 50, 230, self.parent
        )
        
        self.guests_label = UIFactory.create_label(
            "Guests: (not selected)", 50, 260, self.parent
        )
        
        self.nights_label = UIFactory.create_label(
            "Nights: (not calculated)", 50, 290, self.parent
        )
        
        # Create room cards
        self._create_room_grid()
        
        self._setup_show_event()
    
    def _create_room_grid(self):
        # Get all rooms
        rooms = RoomRepository.get_all_rooms()
        
        room_width = 300
        room_height = 500
        spacing = 20
        max_per_row = 3
        
        x_start = 500
        y_start = 300
        x = x_start
        y = y_start
        
        # Create card for each room
        for idx, room in enumerate(rooms):
            RoomCard(x, y, self.parent, room, self._on_room_selected)
            
            # Move to next position
            if (idx + 1) % max_per_row == 0:
                # Next row
                x = x_start
                y += room_height + spacing
            else:
                # Next column
                x += room_width + spacing
        
        # Set page height for scrolling
        needed_rows = (len(rooms) + max_per_row - 1) // max_per_row
        total_height = y_start + needed_rows * (room_height + spacing) + 100
        self.parent.setMinimumHeight(total_height)
    
    def _on_room_selected(self, title: str, description: str):
        # Save selected room
        self.booking_data.selected_room = {
            "title": title, 
            "description": description
        }
        
        # Go to login page
        self.stacked_widget.setCurrentIndex(2)
    
    def _go_back_to_home(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def _update_summary_labels(self):
        # Update check-in
        if self.booking_data.check_in:
            checkin_text = f"Check In: {self.booking_data.check_in}"
        else:
            checkin_text = "Check In: (not selected)"
        self.checkin_label.setText(checkin_text)
        
        # Update check-out
        if self.booking_data.check_out:
            checkout_text = f"Check Out: {self.booking_data.check_out}"
        else:
            checkout_text = "Check Out: (not selected)"
        self.checkout_label.setText(checkout_text)
        
        # Update guests
        guests_text = f"Guests: {self.booking_data.adults}"
        self.guests_label.setText(guests_text)
        
        # Update nights
        nights = self.booking_data.calculate_nights()
        if nights is not None:
            nights_text = f"Nights: {nights}"
        else:
            nights_text = "Nights: (not calculated)"
        self.nights_label.setText(nights_text)
    
    def _setup_show_event(self):
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            self._update_summary_labels()
            
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        self.parent.showEvent = on_show_event