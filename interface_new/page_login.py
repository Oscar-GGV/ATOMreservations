import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQt5.QtWidgets import QWidget, QStackedWidget
from models import BookingData
from ui_components import UIFactory, HeaderComponent
from backend.login import LoginSystem

class LoginPage:
    
    def __init__(self, parent: QWidget, stacked_widget: QStackedWidget):
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.booking_data = BookingData()
        self.login_system = LoginSystem()
        self.current_user = None
        self._build_ui()
    
    def _build_ui(self):
        # Header with back button
        HeaderComponent(self.parent, show_back=True, back_callback=self._go_back)
        
        # Hotel name
        UIFactory.create_label("HOTEL", 900, 200, self.parent,
                               "color: black; font-size: 30px; font-weight: bold;")
        UIFactory.create_label("ELEON", 850, 225, self.parent,
                               "color: black; font-size: 60px; font-weight: bold;")
        
        # Login title
        UIFactory.create_label("Login", 900, 350, self.parent,
                               "color: black; font-size: 32px; font-weight: bold;")
        
        # Username field
        UIFactory.create_label("Username:", 550, 450, self.parent,
                               "font-weight: bold; font-size: 10pt;")
        self.username_field = UIFactory.create_input_field(750, 450, 400, 40, self.parent)
        
        # Password field
        UIFactory.create_label("Password:", 550, 520, self.parent,
                               "font-weight: bold; font-size: 10pt;")
        self.password_field = UIFactory.create_input_field(750, 520, 400, 40, self.parent)
        self.password_field.setEchoMode(self.password_field.Password)
        
        # Login button
        self.login_button = UIFactory.create_button(
            "Login", 750, 590, 400, 50, self.parent,
            "background-color: black; color: white; font-size: 18px;"
        )
        self.login_button.clicked.connect(self._handle_login)
        
        # Forgot password button
        self.forgot_button = UIFactory.create_button(
            "Forgot Password?", 750, 660, 195, 40, self.parent,
            "background-color: transparent; color: #666; font-size: 14px; border: none;"
        )
        
        # Create account button
        self.create_button = UIFactory.create_button(
            "Create New Account", 920, 660, 195, 40, self.parent,
            "background-color: transparent; color: #666; font-size: 14px; border: none;"
        )
        self.create_button.clicked.connect(self._go_to_register)
        
        # Message label
        self.message_label = UIFactory.create_label(
            "", 650, 720, self.parent,
            "color: red; font-size: 14px;"
        )
        self.message_label.setFixedWidth(600)
        
        self._setup_show_event()
    
    def _handle_login(self):
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()
        
        # Validate fields
        if not username or not password:
            self.message_label.setStyleSheet("color: red; font-size: 14px;")
            self.message_label.setText("Please enter username and password")
            return
        
        # Login using backend
        success, message = self.login_system.login(username, password)
        
        if success:
            # Save user info
            self.current_user = self.login_system.get_current_user()
            self._go_to_checkout()
        else:
            # Show error
            self.message_label.setStyleSheet("color: red; font-size: 14px;")
            self.message_label.setText(message)
    
    def _go_to_register(self):
        self.stacked_widget.setCurrentIndex(5)
    
    def _go_to_checkout(self):
        self.stacked_widget.setCurrentIndex(3)
    
    def _go_back(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def get_current_user(self):
        return self.current_user
    
    def _setup_show_event(self):
        original_show = self.parent.showEvent
        
        def on_show(event):
            # Clear password for security
            self.password_field.clear()
            self.message_label.clear()
            
            if original_show:
                try:
                    original_show(event)
                except:
                    pass
        
        self.parent.showEvent = on_show