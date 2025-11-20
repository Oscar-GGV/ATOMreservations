"""ui_components.py
This file defines reusable UI components for the Hotel Eleon booking system.
Includes factories for buttons, labels, rectangles, calendars, and composite
widgets like the header, guest counter, and room card components.
Programmers: You
date of code: November 20th, 2025
"""

from PyQt5.QtWidgets import (
    QPushButton, QFrame, QCalendarWidget, 
    QLabel, QLineEdit, QWidget
)
from PyQt5.QtGui import QFont
from typing import Callable, Optional


class UIFactory:
    """Factory class providing helper methods for creating PyQt5 UI elements.
    All components are created with consistent geometry and optional styling.
    """
  
    @staticmethod
    def create_button(text: str, x: int, y: int, width: int, height: int, 
                     parent: QWidget, style: Optional[str] = None) -> QPushButton:
        """Creates a QPushButton at a specific position with optional CSS style."""
   
        button = QPushButton(text, parent)
        button.move(x, y)
        button.setFixedSize(width, height)
        
        if style:
            button.setStyleSheet(style)
        
        return button
    
    @staticmethod
    def create_label(text: str, x: int, y: int, parent: QWidget, 
                    style: Optional[str] = None) -> QLabel:
        """Creates a QLabel positioned at (x, y) with optional styling."""

        label = QLabel(text, parent)
        label.move(x, y)
        
        if style:
            label.setStyleSheet(style)
        
        return label
    
    @staticmethod
    def create_input_field(x: int, y: int, width: int, height: int, 
                          parent: QWidget, placeholder: str = "") -> QLineEdit:
        """Creates a text input field with dimensions and optional placeholder."""

        field = QLineEdit(parent)
        field.setGeometry(x, y, width, height)
        field.setPlaceholderText(placeholder)
        field.setFont(QFont("Arial", 10))
        
        return field
    
    @staticmethod
    def create_rectangle(x: int, y: int, width: int, height: int, 
                        color: str, parent: QWidget) -> QFrame:
        """Creates a colored rectangular QFrame used for backgrounds and containers."""

        rect = QFrame(parent)
        rect.setGeometry(x, y, width, height)
        rect.setStyleSheet(f"background-color: {color};")
        
        return rect
    
    @staticmethod
    def create_calendar(x: int, y: int, width: int, height: int, 
                       parent: QWidget) -> QCalendarWidget:
        """Creates a styled QCalendarWidget positioned on screen."""

        calendar = QCalendarWidget(parent)
        calendar.move(x, y)
        calendar.resize(width, height)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        
        return calendar


class HeaderComponent:
    """Reusable header bar displayed at the top of each page.
    Optionally includes a back button and navigation text.
    """

    def __init__(self, parent: QWidget, show_back: bool = False, 
                 back_callback: Optional[Callable] = None):
        """Builds the header bar and optional back button."""
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
    Provides +/− controls and notifies the parent when values change.
    """

    def __init__(self, x: int, y: int, width: int, height: int, 
                 parent: QWidget, on_change: Optional[Callable] = None):
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
        """Decreases guest count but not below 1."""
        if self.count > 1:
            self.count -= 1
            self._update_display()
    
    def _increase(self):
        """Increases guest count up to 8."""
        if self.count < 8:
            self.count += 1
            self._update_display()
    
    def _update_display(self):
        """Updates the label and triggers callback if provided."""
        self.count_display.setText(str(self.count))
        
        if self.on_change:
            self.on_change(self.count)
    
    def toggle(self):
        """Shows or hides the guest counter."""
        self.container.setVisible(not self.container.isVisible())
    
    def hide(self):
        """Forces the container to be hidden."""
        self.container.hide()
    
    def get_count(self) -> int:
        """Returns the current number of selected guests."""
        return self.count


class RoomCard:
    """UI component representing a single room option with description and select button."""

    def __init__(self, x: int, y: int, parent: QWidget, room, 
                 on_select: Callable):
        """Creates a visual card showing a room title, features, and select action."""
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
