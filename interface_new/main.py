"""main.py
This file is the starting point of the Hotel Eleon booking application.
It creates the main window and sets up navigation between different pages.

Programmers: Astghik, Mahi
Date of code: November 5th, 2025

Description:
This file builds the main application window and creates all four pages of the booking
system. It uses a QStackedWidget to store these pages and lets users move between them
by changing which page index is active. The pages are: home (0), rooms (1), checkout (2),
and confirmation (3). Each page is built in its own file and gets added here.
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QScrollArea
from PyQt5.QtCore import Qt
from page_home import HomePage
from page_rooms import RoomSelectionPage
from page_checkout import CheckoutPage
from page_confirmation import ConfirmationPage


class HotelBookingApp:
    """Main controller that sets up the whole application.
    Creates the window, builds all pages, and handles the basic structure.
    """

    def __init__(self):
        """Sets up the Qt application and builds the main window with all pages."""
  
        self.app = QApplication(sys.argv)
        # This Qt object is required to run any GUI application
        
        # Setup main window and navigation
        self._setup_main_window()
        self._setup_pages() 
    
    
    def _setup_main_window(self):
        """Creates the main window and the stacked widget for page navigation."""
        
        self.main_window = QWidget()  # main application window
        self.main_window.setWindowTitle("Hotel Eleon - Booking System")
        self.main_window.resize(1920, 1080)
        
        # QStackedWidget holds all pages but only shows one at a time
        self.stacked_widget = QStackedWidget(self.main_window)
        self.stacked_widget.setGeometry(0, 0, 1920, 1080)
    
    
    def _setup_pages(self):
        """Creates all four pages and adds them to the navigation stack.
        
        Each page gets its own container widget and index number:
        0 = Home, 1 = Rooms, 2 = Checkout, 3 = Confirmation
        """
        
        # Home page (index 0)
        page_home = QWidget()
        HomePage(page_home, self.stacked_widget)
        self.stacked_widget.addWidget(page_home)
        
        # Room selection page (index 1) with scroll area
        page_rooms_widget = QWidget()
        RoomSelectionPage(page_rooms_widget, self.stacked_widget)
        
        # Wrap in scroll area so user can scroll if there are many rooms
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(page_rooms_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.stacked_widget.addWidget(scroll_area)
    
        # Checkout page (index 2)
        page_checkout = QWidget()
        CheckoutPage(page_checkout, self.stacked_widget)
        self.stacked_widget.addWidget(page_checkout)
        
        # Confirmation page (index 3)
        page_confirmation = QWidget()
        ConfirmationPage(page_confirmation, self.stacked_widget)
        self.stacked_widget.addWidget(page_confirmation)

        # Start on home page
        self.stacked_widget.setCurrentIndex(0)
    
    
    def run(self):
        """Shows the window and starts the application."""
        
        self.main_window.show()
        sys.exit(self.app.exec_())


def main():
    """Creates the app and runs it."""
    
    app = HotelBookingApp()
    app.run()


if __name__ == "__main__":
    main()