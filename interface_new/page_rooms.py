"""page_rooms.py
This file defines the RoomSelectionPage class which displays all available rooms
as selectable cards, shows booking summary information, and navigates to checkout.
Programmers: 
date of code: November th, 2025
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from models import BookingData, RoomRepository
from ui_components import UIFactory, HeaderComponent, RoomCard


class RoomSelectionPage:
    """Controls the room selection screen of the Hotel Eleon booking system.
    Displays booking summary (dates, guests, nights) and all available room cards.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Initializes the room selection controller.
        Parameters:
            parent (QWidget): Container widget for this page.
            stacked_widget (QStackedWidget): Page navigation controller.
        """
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()  # Model (Singleton)
        
        # Build the UI
        self._build_ui()
    

    def _build_ui(self):
        """Constructs all UI elements, including header, summary labels,
        and the grid of room cards."""
        
        # Create header with back button
        HeaderComponent(
            self.parent, 
            show_back=True, 
            back_callback=self._go_back_to_home
        )

        # Check-in date label
        self.checkin_label = UIFactory.create_label(
            "Check In: (not selected)", 50, 200, self.parent
        )
        
        # Check-out date label
        self.checkout_label = UIFactory.create_label(
            "Check Out: (not selected)", 50, 230, self.parent
        )
        
        # Number of guests label
        self.guests_label = UIFactory.create_label(
            "Guests: (not selected)", 50, 260, self.parent
        )
        
        # Number of nights label (calculated later)
        self.nights_label = UIFactory.create_label(
            "Nights: (not calculated)", 50, 290, self.parent
        )

        # Create grid of room cards (3 per row)
        self._create_room_grid()

        # Setup show event to update summary when page loads
        self._setup_show_event()

    
    def _create_room_grid(self):
        """Builds the grid of RoomCard widgets based on the repository.
        Automatically arranges them in rows and adjusts page height."""
        
        rooms = RoomRepository.get_all_rooms()

        room_width = 300
        room_height = 500
        spacing = 20
        max_per_row = 3
        
        # Starting position
        x_start = 500
        y_start = 300
        x = x_start
        y = y_start
        
        for idx, room in enumerate(rooms):
            # Create room card at current position
            RoomCard(x, y, self.parent, room, self._on_room_selected)
            
            # Calculate next position
            if (idx + 1) % max_per_row == 0:
                x = x_start
                y += room_height + spacing
            else:
                x += room_width + spacing
        
        # Calculate minimum height needed for full grid
        needed_rows = (len(rooms) + max_per_row - 1) // max_per_row
        total_height = y_start + needed_rows * (room_height + spacing) + 100
        self.parent.setMinimumHeight(total_height)
    
    
    def _on_room_selected(self, title: str, description: str):
        """Handles selection of a room card.
        Saves selection to the BookingData model, then navigates to checkout.
        Parameters:
            title (str): Selected room title.
            description (str): Selected room description.
        """
        
        self.booking_data.selected_room = {
            "title": title, 
            "description": description
        }
        
        # Navigate to checkout page
        self.stacked_widget.setCurrentIndex(2)
    
    def _go_back_to_home(self):
        """Navigates back to the home page."""
        self.stacked_widget.setCurrentIndex(0)
    
    
    def _update_summary_labels(self):
        """Updates summary labels (check-in, check-out, guests, nights)
        using data from the BookingData model."""
        
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
    
 
    def _setup_show_event(self):
        """Overrides the parent widget’s showEvent so that summary labels
        refresh every time the room selection page is shown."""
        
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            """Update summary when page is shown."""
            self._update_summary_labels()
            
            # Call original show event if it exists
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        # Attach show event handler
        self.parent.showEvent = on_show_event
