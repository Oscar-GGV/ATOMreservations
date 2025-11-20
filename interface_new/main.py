import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QScrollArea
from PyQt5.QtCore import Qt

# Global screen dimensions - set at startup
Nx = 2560  # Screen width in pixels
Ny = 1664  # Screen height in pixels


def get_Nx():
    """Returns screen width in pixels"""
    return Nx


def get_Ny():
    """Returns screen height in pixels"""
    return Ny


class HotelBookingApp:
    
    def __init__(self):
        global Nx, Ny
  
        self.app = QApplication(sys.argv)
        # required Qt object that manages the whole UI system
        # needed before creating windows or widgets
        
        # Detect screen resolution using Qt's screen detection
        # primaryScreen() gets the main monitor
        # geometry() returns a QRect with screen dimensions
        screen = self.app.primaryScreen()
        screen_geometry = screen.geometry()
        Nx = screen_geometry.width()   # Screen width in pixels (e.g., 1920)
        Ny = screen_geometry.height()  # Screen height in pixels (e.g., 1080)
        
        # Now import pages AFTER setting Nx and Ny
        from page_home import HomePage
        from page_rooms import RoomSelectionPage
        from page_checkout import CheckoutPage
        from page_confirmation import ConfirmationPage
        
        # Store page classes for later use
        self.HomePage = HomePage
        self.RoomSelectionPage = RoomSelectionPage
        self.CheckoutPage = CheckoutPage
        self.ConfirmationPage = ConfirmationPage
        
        # Setup main window and navigation
        self._setup_main_window()
        self._setup_pages() #build all pages
    
    
    def _setup_main_window(self): #empty window
        
        self.main_window = QWidget() #main application window.
        self.main_window.setWindowTitle("Hotel Eleon - Booking System") #window bar
        self.main_window.resize(Nx, Ny)
        
        # QStackedWidget manages multiple pages
        # Only one page is visible at a time
        self.stacked_widget = QStackedWidget(self.main_window)
        self.stacked_widget.setGeometry(0, 0, Nx, Ny)
    
    
    def _setup_pages(self):

        # Create page container widget
        page_home = QWidget()
        
        # Initialize home page controller (builds UI automatically)
        self.HomePage(page_home, self.stacked_widget)
        
        # Add to navigation stack at index 0
        self.stacked_widget.addWidget(page_home)

        #-----------

        # Create page container widget
        page_rooms_widget = QWidget()
        
        # Initialize room selection controller (builds UI automatically)
        self.RoomSelectionPage(page_rooms_widget, self.stacked_widget)
        
        # Wrap in scroll area for overflow content
        # (allows scrolling when there are many rooms)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Auto-resize content
        scroll_area.setWidget(page_rooms_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No horizontal scroll
        
        # Add scroll area (containing page) to navigation stack at index 1
        self.stacked_widget.addWidget(scroll_area)
    
        #---------

        # Create page container widget
        page_checkout = QWidget()
        
        # Initialize checkout page controller (builds UI automatically)
        self.CheckoutPage(page_checkout, self.stacked_widget)
        
        # Add to navigation stack at index 2
        self.stacked_widget.addWidget(page_checkout)
        
        
        # Create page container widget
        page_confirmation = QWidget()
        
        # Initialize confirmation page controller (builds UI automatically)
        self.ConfirmationPage(page_confirmation, self.stacked_widget)
        
        # Add to navigation stack at index 3
        self.stacked_widget.addWidget(page_confirmation)

        
        # Start on home page (index 0)
        self.stacked_widget.setCurrentIndex(0)
    
    
    
    def run(self):

        # Show the main window
        #(Up to this point, the window existed in memory, but was invisible)
        self.main_window.show()
        
        # the program is running until the window is closed
        sys.exit(self.app.exec_())


def main():
    app = HotelBookingApp()   # create the main application object
    app.run()                 # start the UI event loop


if __name__ == "__main__":
    main()   # run main() only when this file is executed directly