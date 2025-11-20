import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QScrollArea
from PyQt5.QtCore import Qt
from page_home import HomePage
from page_rooms import RoomSelectionPage
from page_checkout import CheckoutPage
from page_confirmation import ConfirmationPage


class HotelBookingApp:
    
    def __init__(self):
  
        self.app = QApplication(sys.argv)
        # required Qt object that manages the whole UI system
        # needed before creating windows or widgets
        
        # Setup main window and navigation
        self._setup_main_window()
        self._setup_pages() 
    
    
    def _setup_main_window(self): #empty window
        
        self.main_window = QWidget() #main application window.
        self.main_window.setWindowTitle("Hotel Eleon - Booking System") #window bar
        self.main_window.resize(1920, 1080)
        
        # QStackedWidget manages multiple pages
        # Only one page is visible at a time
        self.stacked_widget = QStackedWidget(self.main_window)
        self.stacked_widget.setGeometry(0, 0, 1920, 1080)
    
    
    def _setup_pages(self):

        # Create page container widget
        page_home = QWidget()
        
        # Initialize home page controller (builds UI automatically)
        HomePage(page_home, self.stacked_widget)
        
        # Add to navigation stack at index 0
        self.stacked_widget.addWidget(page_home)
        
        # Create page container widget
        page_rooms_widget = QWidget()
        
        # Initialize room selection controller (builds UI automatically)
        RoomSelectionPage(page_rooms_widget, self.stacked_widget)
        
        # Wrap in scroll area for overflow content
        # (allows scrolling when there are many rooms)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Auto-resize content
        scroll_area.setWidget(page_rooms_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No horizontal scroll
        
        # Add scroll area (containing page) to navigation stack at index 1
        self.stacked_widget.addWidget(scroll_area)
    
        
        # Create page container widget
        page_checkout = QWidget()
        
        # Initialize checkout page controller (builds UI automatically)
        CheckoutPage(page_checkout, self.stacked_widget)
        
        # Add to navigation stack at index 2
        self.stacked_widget.addWidget(page_checkout)
        
        
        # Create page container widget
        page_confirmation = QWidget()
        
        # Initialize confirmation page controller (builds UI automatically)
        ConfirmationPage(page_confirmation, self.stacked_widget)
        
        # Add to navigation stack at index 3
        self.stacked_widget.addWidget(page_confirmation)

        
        # Start on home page (index 0)
        self.stacked_widget.setCurrentIndex(0)
    
    
    
    def run(self):

        # Show the main window
        self.main_window.show()
        
        # Start Qt event loop and exit when done
        sys.exit(self.app.exec_())


def main():
    app = HotelBookingApp()   # create the main application object
    app.run()                 # start the UI event loop


if __name__ == "__main__":
    main()   # run main() only when this file is executed directly
