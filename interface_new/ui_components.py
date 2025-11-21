"""ui_components.py
This file defines reusable UI components for the Hotel Eleon booking system.
Includes factories for buttons, labels, rectangles, calendars, and composite
widgets like the header, guest counter, and room card components.

Programmers: Astghik, Mahi
Date of code: October 28th, 2025

Description:
This file implements the Controller layer of the MVC architecture and contains
reusable UI components. UIFactory uses the Factory pattern to create standardized
PyQt5 widgets with consistent styling. The composite components (HeaderComponent,
GuestCounter, RoomCard) use the Composite pattern to combine multiple widgets into
single reusable units. These components are used across all pages to maintain
consistency and reduce code duplication.
"""

from PyQt5.QtWidgets import (
    QPushButton, QFrame, QCalendarWidget, 
    QLabel, QLineEdit, QWidget
)
from PyQt5.QtGui import QFont
from typing import Callable, Optional


class UIFactory:
    """Factory class providing helper methods for creating PyQt5 UI elements.
    
    This implements the Factory design pattern to centralize widget creation.
    Instead of each page creating widgets with repetitive PyQt5 code, they call
    these factory methods which handle all the setup. This ensures consistency
    across the application and makes it easy to change styling globally.
    
    All methods are static since they don't need instance-specific data - they
    just create and return configured widgets.
    """
  
    @staticmethod
    def create_button(text: str, x: int, y: int, width: int, height: int, 
                     parent: QWidget, style: Optional[str] = None) -> QPushButton:
        """Creates a QPushButton at a specific position with optional CSS style.
        
        Parameters:
            text (str): Button label text
            x (int): X position in pixels
            y (int): Y position in pixels
            width (int): Button width in pixels
            height (int): Button height in pixels
            parent (QWidget): Parent widget to attach button to
            style (str, optional): CSS styling string for custom appearance
            
        Returns:
            QPushButton: Configured button ready to use
        """
   
        button = QPushButton(text, parent)
        button.move(x, y)
        button.setFixedSize(width, height)
        
        if style:
            button.setStyleSheet(style)
        
        return button
    
    @staticmethod
    def create_label(text: str, x: int, y: int, parent: QWidget, 
                    style: Optional[str] = None) -> QLabel:
        """Creates a QLabel positioned at (x, y) with optional styling.
        
        Parameters:
            text (str): Text to display
            x (int): X position in pixels
            y (int): Y position in pixels
            parent (QWidget): Parent widget
            style (str, optional): CSS styling string
            
        Returns:
            QLabel: Configured label widget
        """

        label = QLabel(text, parent)
        label.move(x, y)
        
        if style:
            label.setStyleSheet(style)
        
        return label
    
    @staticmethod
    def create_input_field(x: int, y: int, width: int, height: int, 
                          parent: QWidget, placeholder: str = "") -> QLineEdit:
        """Creates a text input field with dimensions and optional placeholder.
        
        Sets Arial 10pt font for consistent text input appearance across the app.
        
        Parameters:
            x (int): X position in pixels
            y (int): Y position in pixels
            width (int): Input field width in pixels
            height (int): Input field height in pixels
            parent (QWidget): Parent widget
            placeholder (str, optional): Hint text shown when field is empty
            
        Returns:
            QLineEdit: Configured text input field
        """

        field = QLineEdit(parent)
        field.setGeometry(x, y, width, height)
        field.setPlaceholderText(placeholder)
        field.setFont(QFont("Arial", 10))
        
        return field
    
    @staticmethod
    def create_rectangle(x: int, y: int, width: int, height: int, 
                        color: str, parent: QWidget) -> QFrame:
        """Creates a colored rectangular QFrame used for backgrounds and containers.
        
        QFrame is used instead of drawing shapes because it's simpler and provides
        a widget that can contain other widgets if needed.
        
        Parameters:
            x (int): X position in pixels
            y (int): Y position in pixels
            width (int): Rectangle width in pixels
            height (int): Rectangle height in pixels
            color (str): CSS color name or hex code (e.g., "black" or "#000000")
            parent (QWidget): Parent widget
            
        Returns:
            QFrame: Configured rectangular frame
        """

        rect = QFrame(parent)
        rect.setGeometry(x, y, width, height)
        rect.setStyleSheet(f"background-color: {color};")
        
        return rect
    
    @staticmethod
    def create_calendar(x: int, y: int, width: int, height: int, 
                       parent: QWidget) -> QCalendarWidget:
        """Creates a styled QCalendarWidget positioned on screen.
        
        Removes the vertical header (week numbers) for a cleaner look.
        
        Parameters:
            x (int): X position in pixels
            y (int): Y position in pixels
            width (int): Calendar width in pixels
            height (int): Calendar height in pixels
            parent (QWidget): Parent widget
            
        Returns:
            QCalendarWidget: Configured calendar widget
        """

        calendar = QCalendarWidget(parent)
        calendar.move(x, y)
        calendar.resize(width, height)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        
        return calendar


class HeaderComponent:
    """Reusable header bar displayed at the top of each page.
    
    This is a composite component that combines a black background frame, optional
    back button, and navigation text into a single reusable unit. Uses the Delegation
    pattern where the back button's action is delegated to the parent page through
    a callback function.
    """

    def __init__(self, parent: QWidget, show_back: bool = False, 
                 back_callback: Optional[Callable] = None):
        """Builds the header bar and optional back button.
        
        The header appears the same on all pages, but the back button only shows
        when show_back is True and a callback is provided. This allows pages to
        control their own navigation logic through delegation.
        
        Parameters:
            parent (QWidget): Parent widget to attach header to
            show_back (bool): Whether to show the back button
            back_callback (Callable, optional): Function to call when back is clicked
        """
        self.parent = parent
        
        # Create black header background (full width)
        self.header_frame = UIFactory.create_rectangle(
            0, 0, 1980, 150, "black", parent
        )

        # Back button when allowed
        if show_back and back_callback:
            self.back_button = UIFactory.create_button(
                "Back", 50, 70, 150, 40, parent
            )
            self.back_button.clicked.connect(back_callback)
            self.back_button.raise_()  # Bring to front

        # Navigation menu text
        nav_text = "Home\t\t\tAbout\t\t\tReservation\t\t\tAmenites"
        self.nav_label = UIFactory.create_label(
            nav_text, 450, 70, self.header_frame,
            "color: white; font-size: 22px;"
        )


class GuestCounter:
    """Interactive widget for selecting number of adult guests.
    
    This composite component combines a container frame, label, count display,
    and two buttons (+/-) into a single dropdown-style selector. Uses the
    Delegation pattern to notify the parent page when the count changes through
    an on_change callback.
    
    The count is constrained between 1 and 8 guests, which are reasonable limits
    for a hotel booking system.
    """

    def __init__(self, x: int, y: int, width: int, height: int, 
                 parent: QWidget, on_change: Optional[Callable] = None):
        """Creates the guest counter widget with +/- controls.
        
        Parameters:
            x (int): X position in pixels
            y (int): Y position in pixels
            width (int): Counter width in pixels
            height (int): Counter height in pixels
            parent (QWidget): Parent widget
            on_change (Callable, optional): Callback function(count: int) called when count changes
        """
        self.parent = parent
        self.on_change = on_change
        self.count = 1  # Default: 1 guest
        
        # White container box
        self.container = QFrame(parent)
        self.container.setGeometry(x, y, width, height)
        self.container.setStyleSheet("background-color: white; border: none;")
        self.container.hide()  # Hidden by default
  
        UIFactory.create_label(
            "Adults", 20, 20, self.container, "font-size: 16px;"
        )
        
        # Display current count
        self.count_display = UIFactory.create_label(
            str(self.count), 130, 20, self.container, "font-size: 16px;"
        )
        self.count_display.setFixedWidth(20)

        # Left button (decrement)
        self.left_button = UIFactory.create_button(
            "<", 100, 15, 25, 25, self.container
        )
        self.left_button.clicked.connect(self._decrease)
        
        # Right button (increment)
        self.right_button = UIFactory.create_button(
            ">", 145, 15, 25, 25, self.container
        )
        self.right_button.clicked.connect(self._increase)
    
    def _decrease(self):
        """Decreases guest count but not below 1.
        
        Minimum of 1 guest is enforced since you can't book a room with 0 guests.
        """
        if self.count > 1:
            self.count -= 1
            self._update_display()
    
    def _increase(self):
        """Increases guest count up to 8.
        
        Maximum of 8 guests is a reasonable limit for room capacity.
        """
        if self.count < 8:
            self.count += 1
            self._update_display()
    
    def _update_display(self):
        """Updates the label and triggers callback if provided.
        
        This calls the on_change callback (if provided) to notify the parent
        page that the count has changed, implementing the Delegation pattern.
        """
        self.count_display.setText(str(self.count))
        
        if self.on_change:
            self.on_change(self.count)
    
    def toggle(self):
        """Shows or hides the guest counter.
        
        This creates a dropdown-like behavior where the counter appears below
        the guests button when clicked.
        """
        self.container.setVisible(not self.container.isVisible())
    
    def hide(self):
        """Forces the container to be hidden.
        
        Used when navigating to/from the home page to ensure a clean state.
        """
        self.container.hide()
    
    def get_count(self) -> int:
        """Returns the current number of selected guests.
        
        Returns:
            int: Current guest count (1-8)
        """
        return self.count


class RoomCard:
    """UI component representing a single room option with description and select button.
    
    This composite component combines a background card, colored header, title label,
    description text with bullet points, and a select button into one visual unit.
    Uses the Delegation pattern where clicking "Select" delegates the action back to
    the parent page through the on_select callback.
    
    The card uses a fixed 300x500 size which works well in the 3-column grid layout.
    """

    def __init__(self, x: int, y: int, parent: QWidget, room, 
                 on_select: Callable):
        """Creates a visual card showing a room title, features, and select action.
        
        The description is split into bullet points using the Room object's
        get_description_lines() method, then formatted with bullet characters.
        
        Parameters:
            x (int): X position in pixels
            y (int): Y position in pixels
            parent (QWidget): Parent widget
            room (Room): Room object containing title and description
            on_select (Callable): Callback function(title: str, description: str) called when selected
        """
        self.room = room
        
        # Card dimensions
        width = 300
        height = 500

        # White card background
        self.card = UIFactory.create_rectangle(x, y, width, height, "white", parent)
        self.card.setStyleSheet("border: 2px solid gray; border-radius: 10px;")
        
        # Blue header band
        UIFactory.create_rectangle(0, 0, width, 150, "lightblue", self.card)

        # Room title
        UIFactory.create_label(
            room.title, 10, 160, self.card,
            "font-size: 16px; font-weight: bold; border: none; background: transparent;"
        )
        
        # Description as bullet points
        desc_lines = room.get_description_lines()
        desc_text = '\n'.join(f"• {line}" for line in desc_lines)
        
        UIFactory.create_label(
            desc_text, 10, 190, self.card,
            "font-size: 13px; border: none; background: transparent;"
        )

        # Select button
        select_btn = UIFactory.create_button(
            "Select", 100, 450, 100, 35, self.card,
        )
        
        # Connect selection handler
        select_btn.clicked.connect(
            lambda: on_select(room.title, room.description)
        )