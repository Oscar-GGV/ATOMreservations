"""page_rooms.py
This file defines the RoomSelectionPage class which displays all available rooms
as selectable cards, shows booking summary information, and navigates to checkout.

Programmers: Astghik, Mahi
Date of code: November 8th, 2025

Description:
This page (index 1 in navigation) displays available rooms after the user checks
availability. It shows a booking summary at the top (dates, guests, nights) and
creates a grid of room cards below. Room data comes from RoomRepository and each
card is clickable to select that room. Uses a grid layout algorithm to arrange
rooms 3 per row and automatically calculates the needed page height.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget
from models import BookingData, RoomRepository
from ui_components import UIFactory, HeaderComponent, RoomCard


class RoomSelectionPage:
    """Controls the room selection screen of the Hotel Eleon booking system.
    
    This View displays booking summary and available rooms. It pulls booking info
    from BookingData singleton to show dates and guests, gets room data from
    RoomRepository, and creates RoomCard components for each room. When a room
    is selected, it saves the choice to BookingData and navigates to checkout.
    """

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Initializes the room selection controller.
        
        Sets up references to navigation and BookingData singleton, then builds
        all UI elements including summary labels and room grid.
        
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
        and the grid of room cards.
        
        Creates a header with back button at the top, four summary labels on the
        left (check-in, check-out, guests, nights), and a grid of room cards in
        the center. The page is wrapped in a scroll area (set up in main.py) to
        handle overflow when there are many rooms.
        """
        
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
        
        This implements a grid layout algorithm that arranges rooms in rows of 3.
        The algorithm:
        1. Gets all rooms from RoomRepository
        2. Places rooms left to right, then moves to next row after 3 cards
        3. Uses modulo operator (%) to detect when to wrap to new row
        4. Calculates total height needed using ceiling division
        5. Sets parent minimum height so scroll area works properly
        
        We chose this grid approach over a vertical list because it uses screen
        space more efficiently and lets users see multiple rooms at once.
        
        Data Structure: Uses enumerate to track both index and room object in the loop,
        which is needed for the modulo calculation to determine row wrapping.
        """
        
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
        
        This is a callback function passed to each RoomCard, implementing the
        Delegation pattern. When a user clicks "Select" on any room card, that
        card delegates the action back to this page controller.
        
        Saves the selected room as a dictionary to BookingData singleton so it's
        available on checkout and confirmation pages, then navigates to checkout.
        
        Parameters:
            title (str): Selected room title (e.g., "Ocean View Suite").
            description (str): Selected room description with features.
        """
        
        self.booking_data.selected_room = {
            "title": title, 
            "description": description
        }
        
        # Navigate to checkout page
        self.stacked_widget.setCurrentIndex(2)
    
    def _go_back_to_home(self):
        """Navigates back to the home page.
        
        Changes stacked widget index to 0 (home page). This allows users to
        change their dates or guest count if needed.
        """
        self.stacked_widget.setCurrentIndex(0)
    
    
    def _update_summary_labels(self):
        """Updates summary labels (check-in, check-out, guests, nights)
        using data from the BookingData model.
        
        Pulls current booking information from BookingData singleton and updates
        all four summary labels. The nights value is calculated by calling
        calculate_nights() method on BookingData. This method is called automatically
        when the page is shown to ensure labels always display current data.
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
        
        # Calculate nights from model
        nights = self.booking_data.calculate_nights()
        
        if nights is not None:
            nights_text = f"Nights: {nights}"
        else:
            nights_text = "Nights: (not calculated)"
        
        self.nights_label.setText(nights_text)
    
 
    def _setup_show_event(self):
        """Overrides the parent widget's showEvent so that summary labels
        refresh every time the room selection page is shown.
        
        This ensures the booking summary is always up-to-date, even if the user
        navigates back from checkout to change their room selection. Preserves
        any existing showEvent by chaining it after our update logic.
        """
        
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