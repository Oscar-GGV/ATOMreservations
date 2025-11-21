"""ui_components.py
This file contains reusable UI components that are used across all pages.
It has helper functions to create buttons, labels, and other widgets consistently.

Programmers: Astghik, Mahi
Date of code: October 28th, 2025

Description:
This file provides simple functions to create UI elements without repeating code.
UIFactory has methods to create common widgets like buttons and labels with consistent
styling. The other classes (HeaderComponent, GuestCounter, RoomCard) are ready-made
components that combine multiple widgets together. All pages import from this file
to build their interfaces.
"""

from PyQt5.QtWidgets import (
    QPushButton, QFrame, QCalendarWidget, 
    QLabel, QLineEdit, QWidget
)
from PyQt5.QtGui import QFont
from typing import Callable, Optional


class UIFactory:
    """Helper class with methods to create UI widgets quickly and consistently.
    All methods are static so you can call them without creating an instance.
    """
  
    @staticmethod
    def create_button(text: str, x: int, y: int, width: int, height: int, 
                     parent: QWidget, style: Optional[str] = None) -> QPushButton:
        """Creates a button at a specific position.
        
        Parameters:
            text: Button label
            x, y: Position on screen
            width, height: Button size
            parent: Widget to attach button to
            style: Optional CSS styling
            
        Returns:
            Configured button ready to use
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
        """Creates a text label at a specific position.
        
        Parameters:
            text: Text to display
            x, y: Position on screen
            parent: Widget to attach label to
            style: Optional CSS styling
            
        Returns:
            Configured label
        """

        label = QLabel(text, parent)
        label.move(x, y)
        
        if style:
            label.setStyleSheet(style)
        
        return label
    
    @staticmethod
    def create_input_field(x: int, y: int, width: int, height: int, 
                          parent: QWidget, placeholder: str = "") -> QLineEdit:
        """Creates a text input box.
        
        Parameters:
            x, y: Position on screen
            width, height: Input box size
            parent: Widget to attach to
            placeholder: Hint text when empty
            
        Returns:
            Input field widget
        """

        field = QLineEdit(parent)
        field.setGeometry(x, y, width, height)
        field.setPlaceholderText(placeholder)
        field.setFont(QFont("Arial", 10))
        
        return field
    
    @staticmethod
    def create_rectangle(x: int, y: int, width: int, height: int, 
                        color: str, parent: QWidget) -> QFrame:
        """Creates a colored rectangle for backgrounds.
        
        Parameters:
            x, y: Position on screen
            width, height: Rectangle size
            color: Color name or hex code
            parent: Widget to attach to
            
        Returns:
            Rectangular frame
        """

        rect = QFrame(parent)
        rect.setGeometry(x, y, width, height)
        rect.setStyleSheet(f"background-color: {color};")
        
        return rect
    
    @staticmethod
    def create_calendar(x: int, y: int, width: int, height: int, 
                       parent: QWidget) -> QCalendarWidget:
        """Creates a calendar widget for date selection.
        
        Parameters:
            x, y: Position on screen
            width, height: Calendar size
            parent: Widget to attach to
            
        Returns:
            Calendar widget
        """

        calendar = QCalendarWidget(parent)
        calendar.move(x, y)
        calendar.resize(width, height)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        
        return calendar


class HeaderComponent:
    """Creates the black header bar that appears at the top of every page.
    Can optionally include a back button depending on the page.
    """

    def __init__(self, parent: QWidget, show_back: bool = False, 
                 back_callback: Optional[Callable] = None):
        """Builds the header with optional back button.
        
        Parameters:
            parent: Page to attach header to
            show_back: Whether to show back button
            back_callback: Function to call when back is clicked
        """
        self.parent = parent
        
        # Create black header background across full width
        self.header_frame = UIFactory.create_rectangle(
            0, 0, 1980, 150, "black", parent
        )

        # Add back button if needed
        if show_back and back_callback:
            self.back_button = UIFactory.create_button(
                "Back", 50, 70, 150, 40, parent
            )
            self.back_button.clicked.connect(back_callback)
            self.back_button.raise_()  # Make sure it's on top

        # Navigation menu text
        nav_text = "Home\t\t\tAbout\t\t\tReservation\t\t\tAmenites"
        self.nav_label = UIFactory.create_label(
            nav_text, 450, 70, self.header_frame,
            "color: white; font-size: 22px;"
        )


class GuestCounter:
    """Creates a dropdown widget with +/- buttons to select number of guests.
    Shows and hides when the guests button is clicked.
    """

    def __init__(self, x: int, y: int, width: int, height: int, 
                 parent: QWidget, on_change: Optional[Callable] = None):
        """Builds the guest counter with controls.
        
        Parameters:
            x, y: Position on screen
            width, height: Counter size
            parent: Page to attach to
            on_change: Function to call when count changes
        """
        self.parent = parent
        self.on_change = on_change
        self.count = 1  # Start with 1 guest
        
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

        # Left button (decrease)
        self.left_button = UIFactory.create_button(
            "<", 100, 15, 25, 25, self.container
        )
        self.left_button.clicked.connect(self._decrease)
        
        # Right button (increase)
        self.right_button = UIFactory.create_button(
            ">", 145, 15, 25, 25, self.container
        )
        self.right_button.clicked.connect(self._increase)
    
    def _decrease(self):
        """Decreases guest count, but not below 1."""
        if self.count > 1:
            self.count -= 1
            self._update_display()
    
    def _increase(self):
        """Increases guest count, up to 8."""
        if self.count < 8:
            self.count += 1
            self._update_display()
    
    def _update_display(self):
        """Updates the displayed count and notifies parent page."""
        self.count_display.setText(str(self.count))
        
        if self.on_change:
            self.on_change(self.count)
    
    def toggle(self):
        """Shows or hides the counter."""
        self.container.setVisible(not self.container.isVisible())
    
    def hide(self):
        """Hides the counter."""
        self.container.hide()
    
    def get_count(self) -> int:
        """Returns current guest count."""
        return self.count


class RoomCard:
    """Creates a visual card for one room with its details and select button.
    Combines multiple elements into one card component.
    """

    def __init__(self, x: int, y: int, parent: QWidget, room, 
                 on_select: Callable):
        """Builds a room card with title, description, and select button.
        
        Parameters:
            x, y: Position on screen
            parent: Page to attach to
            room: Room object with title and description
            on_select: Function to call when room is selected
        """
        self.room = room
        
        # Card size
        width = 300
        height = 500

        # White card background with border
        self.card = UIFactory.create_rectangle(x, y, width, height, "white", parent)
        self.card.setStyleSheet("border: 2px solid gray; border-radius: 10px;")
        
        # Blue header at top of card
        UIFactory.create_rectangle(0, 0, width, 150, "lightblue", self.card)

        # Room title
        UIFactory.create_label(
            room.title, 10, 160, self.card,
            "font-size: 16px; font-weight: bold; border: none; background: transparent;"
        )
        
        # Description with bullet points
        desc_lines = room.get_description_lines()
        desc_text = '\n'.join(f"• {line}" for line in desc_lines)
        
        UIFactory.create_label(
            desc_text, 10, 190, self.card,
            "font-size: 13px; border: none; background: transparent;"
        )

        # Select button at bottom
        select_btn = UIFactory.create_button(
            "Select", 100, 450, 100, 35, self.card,
        )
        
        # Connect button to selection handler
        select_btn.clicked.connect(
            lambda: on_select(room.title, room.description)
        )