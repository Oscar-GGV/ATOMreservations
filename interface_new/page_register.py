"""page_register.py
Registration page for Hotel Eleon booking system.

Programmers: Integration Team
Date: December 3rd, 2025

Description:
Registration page where new users can create accounts. Uses backend LoginSystem
to register users. After successful registration, redirects to login page.
"""

import sys
import os
# Add parent directory to path so we can import backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QTimer
from ui_components import UIFactory, HeaderComponent
from backend.login import LoginSystem


class RegisterPage:
    """Builds and controls the registration page."""

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Sets up the registration page.
        
        Parameters:
            parent: Widget container for this page
            stacked_widget: Navigation controller
        """
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.login_system = LoginSystem()
        self.input_fields = {}
        
        self._build_ui()
    
    def _build_ui(self):
        """Creates all the UI elements on the registration page."""
        
        # Header with back button
        HeaderComponent(self.parent, show_back=True, back_callback=self._go_back)
        
        # Hotel name at top
        UIFactory.create_label("HOTEL", 870, 150, self.parent,
                               "color: black; font-size: 30px; font-weight: bold;")
        UIFactory.create_label("ELEON", 820, 175, self.parent,
                               "color: black; font-size: 60px; font-weight: bold;")
        
        # Title
        UIFactory.create_label("Create New Account", 770, 280, self.parent,
                               "color: black; font-size: 32px; font-weight: bold;")
        
        # Form fields (same style as checkout page)
        y = 370
        x = 650
        input_width = 400
        input_height = 40
        spacing = 60
        
        # List of all fields
        fields = [
            ("Username:", "username"),
            ("Password:", "password"),
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Phone:", "phone")
        ]
        
        for label_text, field_key in fields:
            # Create label
            label = UIFactory.create_label(label_text, x, y, self.parent)
            label.setStyleSheet("font-weight: bold; font-size: 10pt;")
            
            # Create input field
            field = UIFactory.create_input_field(x + 200, y, input_width, input_height, self.parent)
            
            # Hide password
            if field_key == "password":
                field.setEchoMode(field.Password)
            
            # Store field for later access
            self.input_fields[field_key] = field
            y += spacing
        
        # Create Account button
        self.register_button = UIFactory.create_button(
            "Create Account", 850, y + 20, 400, 50, self.parent,
            "background-color: black; color: white; font-size: 18px;"
        )
        self.register_button.clicked.connect(self._handle_register)
        
        # Status message label
        self.message_label = UIFactory.create_label(
            "", 650, y + 90, self.parent,
            "color: red; font-size: 14px;"
        )
        self.message_label.setFixedWidth(600)
        
        self._setup_show_event()
    
    def _handle_register(self):
        """Handle registration button click - uses backend LoginSystem."""
        # Get all field values
        username = self.input_fields['username'].text().strip()
        password = self.input_fields['password'].text().strip()
        first_name = self.input_fields['first_name'].text().strip()
        last_name = self.input_fields['last_name'].text().strip()
        email = self.input_fields['email'].text().strip()
        phone = self.input_fields['phone'].text().strip()
        
        # Validate required fields (phone is optional)
        if not all([username, password, first_name, last_name, email]):
            self.message_label.setStyleSheet("color: red; font-size: 14px;")
            self.message_label.setText("Please fill in all required fields (Phone is optional)")
            return
        
        # Use backend registration system
        success, message = self.login_system.register(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        
        if success:
            # Show success message in green
            self.message_label.setStyleSheet("color: green; font-size: 14px;")
            self.message_label.setText(message)
            
            # Clear all fields
            for field in self.input_fields.values():
                field.clear()
            
            # Go to login page after 2 seconds
            QTimer.singleShot(2000, self._go_to_login)
        else:
            # Show error message in red
            self.message_label.setStyleSheet("color: red; font-size: 14px;")
            self.message_label.setText(message)
    
    def _go_to_login(self):
        """Go to login page after successful registration."""
        self.stacked_widget.setCurrentIndex(2)  # Login is index 2
    
    def _go_back(self):
        """Go back to login page."""
        self.stacked_widget.setCurrentIndex(2)  # Login is index 2
    
    def _setup_show_event(self):
        """Clear fields when page is shown."""
        original_show = self.parent.showEvent
        
        def on_show(event):
            # Clear all fields
            for field in self.input_fields.values():
                field.clear()
            # Clear message
            self.message_label.clear()
            if original_show:
                try:
                    original_show(event)
                except:
                    pass
        
        self.parent.showEvent = on_show