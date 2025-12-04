"""page_rooms.py
This file creates the room selection page where users can see and pick rooms.
It shows available rooms as cards and displays the booking summary.

Programmers: Astghik, Mahi
Date of code: November 8th, 2025
Modified: December 3rd, 2025 - Updated to go to login page

Description:
This page (index 1) appears after user checks availability. It shows booking info
at the top (dates, guests, nights) and displays all available rooms in a grid below.
Room data comes from RoomRepository. Each room is shown as a card with a select button.
When user picks a room, it saves to BookingData and goes to login page.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from models import BookingData, RoomRepository
from ui_components import UIFactory, HeaderComponent, RoomCard


class RoomSelectionPage:
    """Builds and controls the room selection page.
    Shows booking summary and creates room cards from repository data.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Sets up the room selection page.
        
        Parameters:
            parent: Widget container for this page
            stacked_widget: Navigation controller to switch pages
        """
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        
        self._build_ui()
    

    def _build_ui(self):
        """Creates all UI elements on this page.
        
        Builds header with back button, summary labels on the left showing dates
        and guests, and room cards in a grid layout.
        """
        
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

        # Create grid of room cards
        self._create_room_grid()

        # Update labels when page shows
        self._setup_show_event()

    
    def _create_room_grid(self):
        """Creates room cards arranged in a grid, 3 per row.
        
        Gets all rooms from repository and places them in rows. Uses a loop
        to position each card, moving to next row after every 3 cards.
        Also calculates how tall the page needs to be for all rooms.
        """
        
        rooms = RoomRepository.get_all_rooms()

        room_width = 300
        room_height = 500
        spacing = 20
        max_per_row = 3
        
        # Starting position for first card
        x_start = 500
        y_start = 300
        x = x_start
        y = y_start
        
        for idx, room in enumerate(rooms):
            # Create card at current position
            RoomCard(x, y, self.parent, room, self._on_room_selected)
            
            # Figure out next position
            if (idx + 1) % max_per_row == 0:
                # Move to next row
                x = x_start
                y += room_height + spacing
            else:
                # Move to next column
                x += room_width + spacing
        
        # Calculate total height needed for all rooms
        needed_rows = (len(rooms) + max_per_row - 1) // max_per_row
        total_height = y_start + needed_rows * (room_height + spacing) + 100
        self.parent.setMinimumHeight(total_height)
    
    
    def _on_room_selected(self, title: str, description: str):
        """Called when user clicks select on a room card.
        Saves the room choice and goes to login page.
        
        Parameters:
            title: Name of selected room
            description: Room features
        """
        
        self.booking_data.selected_room = {
            "title": title, 
            "description": description
        }
        
        # Go to login page
        self.stacked_widget.setCurrentIndex(2)
    
    def _go_back_to_home(self):
        """Goes back to home page when back button clicked."""
        self.stacked_widget.setCurrentIndex(0)
    
    
    def _update_summary_labels(self):
        """Updates all the summary labels with current booking info.
        Gets data from BookingData and displays it.
        """
        
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
        
        # Calculate and show nights
        nights = self.booking_data.calculate_nights()
        
        if nights is not None:
            nights_text = f"Nights: {nights}"
        else:
            nights_text = "Nights: (not calculated)"
        
        self.nights_label.setText(nights_text)
    
 
    def _setup_show_event(self):
        """Makes labels update automatically when page is shown.
        This keeps the summary current if user goes back and changes dates.
        """
        
        original_show_event = self.parent.showEvent
        
        def on_show_event(event):
            self._update_summary_labels()
            
            if original_show_event:
                try:
                    original_show_event(event)
                except:
                    pass
        
        self.parent.showEvent = on_show_event