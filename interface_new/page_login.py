"""page_login.py
Login page for Hotel Eleon booking system.

Programmers: Integration Team
Date: December 3rd, 2025

Description:
Login page with username and password fields. Uses backend LoginSystem directly.
After successful login, user info is saved and user goes to checkout page.
Has buttons for "Forgot Password" and "Create New Account".
"""

import sys
import os
# Add parent directory to path so we can import backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import QTimer
from models import BookingData
from ui_components import UIFactory, HeaderComponent
from backend.login import LoginSystem


class LoginPage:
    """Builds and controls the login page."""

    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        """Sets up the login page.
        
        Parameters:
            parent: Widget container for this page
            stacked_widget: Navigation controller
        """
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self.login_system = LoginSystem()
        self.current_user = None  # Will store logged-in user info
        
        self._build_ui()
    
    def _build_ui(self):
        """Creates all the UI elements on the login page."""
        
        # Header with back button
        HeaderComponent(self.parent, show_back=True, back_callback=self._go_back)
        
        # Hotel name at top
        UIFactory.create_label("HOTEL", 870, 200, self.parent,
                               "color: black; font-size: 30px; font-weight: bold;")
        UIFactory.create_label("ELEON", 820, 225, self.parent,
                               "color: black; font-size: 60px; font-weight: bold;")
        
        # Login title
        UIFactory.create_label("Login", 900, 350, self.parent,
                               "color: black; font-size: 32px; font-weight: bold;")
        
        # Username field (same style as checkout page)
        UIFactory.create_label("Username:", 650, 450, self.parent,
                               "font-weight: bold; font-size: 10pt;")
        self.username_field = UIFactory.create_input_field(850, 450, 400, 40, self.parent)
        
        # Password field
        UIFactory.create_label("Password:", 650, 520, self.parent,
                               "font-weight: bold; font-size: 10pt;")
        self.password_field = UIFactory.create_input_field(850, 520, 400, 40, self.parent)
        self.password_field.setEchoMode(self.password_field.Password)  # Hide password with dots
        
        # Login button
        self.login_button = UIFactory.create_button(
            "Login", 850, 590, 400, 50, self.parent,
            "background-color: black; color: white; font-size: 18px;"
        )
        self.login_button.clicked.connect(self._handle_login)
        
        # Forgot password button (transparent, just text)
        self.forgot_button = UIFactory.create_button(
            "Forgot Password?", 850, 660, 195, 40, self.parent,
            "background-color: transparent; color: #666; font-size: 14px; border: none;"
        )
       
        # Create account button
        self.create_button = UIFactory.create_button(
            "Create New Account", 1055, 660, 195, 40, self.parent,
            "background-color: transparent; color: #666; font-size: 14px; border: none;"
        )
        self.create_button.clicked.connect(self._go_to_register)
        
        # Error/success message label
        self.message_label = UIFactory.create_label(
            "", 650, 720, self.parent,
            "color: red; font-size: 14px;"
        )
        self.message_label.setFixedWidth(600)
        
        self._setup_show_event()
    
    def _handle_login(self):
        """Handle login button click - uses backend LoginSystem."""
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()
        
        # Validate fields not empty
        if not username or not password:
            self.message_label.setStyleSheet("color: red; font-size: 14px;")
            self.message_label.setText("Please enter username and password")
            return
        
        # Use backend login system directly
        success, message = self.login_system.login(username, password)
        
        if success:
            # Save user info
            self.current_user = self.login_system.get_current_user()
            
            # Show success message in green
            self.message_label.setStyleSheet("color: green; font-size: 14px;")
            self.message_label.setText(message)
            
            # Go to checkout page after 1 second
            QTimer.singleShot(1000, self._go_to_checkout)
        else:
            # Show error message in red
            self.message_label.setStyleSheet("color: red; font-size: 14px;")
            self.message_label.setText(message)

    
    def _go_to_register(self):
        """Go to registration page (index 5)."""
        self.stacked_widget.setCurrentIndex(5)
    
    def _go_to_checkout(self):
        """Go to checkout page after successful login."""
        self.stacked_widget.setCurrentIndex(3)  # Checkout is now index 3
    
    def _go_back(self):
        """Go back to room selection page."""
        self.stacked_widget.setCurrentIndex(1)
    
    def get_current_user(self):
        """Get logged in user info - other pages can call this."""
        return self.current_user
    
    def _setup_show_event(self):
        """Clear password when page is shown."""
        original_show = self.parent.showEvent
        
        def on_show(event):
            # Clear password field for security
            self.password_field.clear()
            # Clear message
            self.message_label.clear()
            if original_show:
                try:
                    original_show(event)
                except:
                    pass
        
        self.parent.showEvent = on_show