from PyQt5.QtWidgets import (
    QPushButton, QFrame, QCalendarWidget, 
    QLabel, QLineEdit, QWidget
)
from PyQt5.QtGui import QFont
from typing import Callable, Optional
from main import get_Nx, get_Ny  # Import functions to access Nx, Ny


class UIFactory:
  
    @staticmethod
    def create_button(text: str, x: int, y: int, width: int, height: int, 
                     parent: QWidget, style: Optional[str] = None) -> QPushButton:
   
        button = QPushButton(text, parent)
        button.move(x, y)
        button.setFixedSize(width, height)
        
        if style:
            button.setStyleSheet(style)
        
        return button
    
    @staticmethod
    def create_label(text: str, x: int, y: int, parent: QWidget, 
                    style: Optional[str] = None) -> QLabel:

        label = QLabel(text, parent)
        label.move(x, y)
        
        if style:
            label.setStyleSheet(style)
        
        return label
    
    @staticmethod
    def create_input_field(x: int, y: int, width: int, height: int, 
                          parent: QWidget, placeholder: str = "") -> QLineEdit:

        field = QLineEdit(parent)
        field.setGeometry(x, y, width, height)
        field.setPlaceholderText(placeholder)
        field.setFont(QFont("Arial", 10))
        
        return field
    
    @staticmethod
    def create_rectangle(x: int, y: int, width: int, height: int, 
                        color: str, parent: QWidget) -> QFrame:

        rect = QFrame(parent)
        rect.setGeometry(x, y, width, height)
        rect.setStyleSheet(f"background-color: {color};")
        
        return rect
    
    @staticmethod
    def create_calendar(x: int, y: int, width: int, height: int, 
                       parent: QWidget) -> QCalendarWidget:

        calendar = QCalendarWidget(parent)
        calendar.move(x, y)
        calendar.resize(width, height)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        
        return calendar


class HeaderComponent:

    
    def __init__(self, parent: QWidget, show_back: bool = False, 
                 back_callback: Optional[Callable] = None):

        self.parent = parent
        Nx = get_Nx()
        Ny = get_Ny()
        
        # Create black header background (full width)
        # Original: (0, 0, 1980, 150)
        # 1980/1920 = 1.03125 ≈ full width, 150/1080 = 0.139
        self.header_frame = UIFactory.create_rectangle(
            0, 0, Nx, int(Ny / 7.2), "black", parent
        )

        
        if show_back and back_callback:
            # Original: (50, 70, 150, 40)
            # 50/1920 = 0.026, 70/1080 = 0.065, 150/1920 = 0.078, 40/1080 = 0.037
            self.back_button = UIFactory.create_button(
                "Back", int(Nx / 38.4), int(Ny / 15.43), int(Nx / 12.8), int(Ny / 27), parent
            )
            self.back_button.clicked.connect(back_callback)
            self.back_button.raise_()  # Bring to front

        
        # Navigation menu text (tabs)
        nav_text = "Home\t\t\tAbout\t\t\tReservation\t\t\tAmenites"
        # Original: (450, 70)
        # 450/1920 = 0.234, 70/1080 = 0.065
        self.nav_label = UIFactory.create_label(
            nav_text, int(Nx / 4.27), int(Ny / 15.43), self.header_frame,
            "color: white; font-size: 22px;"
        )


class GuestCounter:

    def __init__(self, x: int, y: int, width: int, height: int, 
                 parent: QWidget, on_change: Optional[Callable] = None):
 
        self.parent = parent
        self.on_change = on_change
        self.count = 1  # Default: 1 guest
        
        
        # Create white container box
        self.container = QFrame(parent)
        self.container.setGeometry(x, y, width, height)
        self.container.setStyleSheet("background-color: white; border: none;")
        self.container.hide()  # Hidden by default
  
        # Original: (20, 20) relative to container
        # 20/width ratio, 20/height ratio
        UIFactory.create_label(
            "Adults", int(width / 10), int(height / 3.5), self.container, "font-size: 16px;"
        )
        
        
        # Display current count
        # Original: (130, 20)
        # 130/200 = 0.65, 20/70 = 0.286
        self.count_display = UIFactory.create_label(
            str(self.count), int(width * 0.65), int(height / 3.5), self.container, "font-size: 16px;"
        )
        # Original width: 20
        self.count_display.setFixedWidth(int(width / 10))

        
        # Original: (100, 15, 25, 25)
        # 100/200 = 0.5, 15/70 = 0.214, 25/200 = 0.125, 25/70 = 0.357
        self.left_button = UIFactory.create_button(
            "<", int(width / 2), int(height / 4.67), int(width / 8), int(height / 2.8), self.container
        )
        self.left_button.clicked.connect(self._decrease)
        
        
        # Original: (145, 15, 25, 25)
        # 145/200 = 0.725
        self.right_button = UIFactory.create_button(
            ">", int(width * 0.725), int(height / 4.67), int(width / 8), int(height / 2.8), self.container
        )
        self.right_button.clicked.connect(self._increase)
    
    def _decrease(self):

        if self.count > 1:
            self.count -= 1
            self._update_display()
    
    def _increase(self):
 
        if self.count < 8:
            self.count += 1
            self._update_display()
    
    def _update_display(self):

        self.count_display.setText(str(self.count))
        
        if self.on_change:
            self.on_change(self.count)
    
    def toggle(self):

        self.container.setVisible(not self.container.isVisible())
    
    def hide(self):

        self.container.hide()
    
    def get_count(self) -> int:

        return self.count


class RoomCard:
    
    def __init__(self, x: int, y: int, parent: QWidget, room, 
                 on_select: Callable):

        self.room = room
        Nx = get_Nx()
        Ny = get_Ny()
        
        # Card dimensions
        # Original: width = 300, height = 500
        # 300/1920 = 0.156, 500/1080 = 0.463
        width = int(Nx / 6.4)
        height = int(Ny / 2.16)

        
        # White card with border
        self.card = UIFactory.create_rectangle(x, y, width, height, "white", parent)
        self.card.setStyleSheet("border: 2px solid gray; border-radius: 10px;")
        
        # Original: (0, 0, 300, 150) - image placeholder
        # 150/500 = 0.3 (30% of card height)
        UIFactory.create_rectangle(0, 0, width, int(height * 0.3), "lightblue", self.card)

        
        # Original: (10, 160)
        # 10/300 = 0.033, 160/500 = 0.32
        UIFactory.create_label(
            room.title, int(width / 30), int(height * 0.32), self.card,
            "font-size: 16px; font-weight: bold; border: none; background: transparent;"
        )
        
        
        # Parse description into bullet points
        desc_lines = room.get_description_lines()
        desc_text = '\n'.join(f"• {line}" for line in desc_lines)
        
        # Original: (10, 190)
        # 10/300 = 0.033, 190/500 = 0.38
        UIFactory.create_label(
            desc_text, int(width / 30), int(height * 0.38), self.card,
            "font-size: 13px; border: none; background: transparent;"
        )

        
        # Blue button with hover effect
        # Original: (100, 450, 100, 35)
        # 100/300 = 0.333, 450/500 = 0.9, 100/300 = 0.333, 35/500 = 0.07
        select_btn = UIFactory.create_button(
            "Select", int(width / 3), int(height * 0.9), int(width / 3), int(height * 0.07), self.card,
            ""
        )
        
        # Connect to selection handler
        select_btn.clicked.connect(
            lambda: on_select(room.title, room.description)
        )