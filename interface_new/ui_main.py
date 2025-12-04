import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QScrollArea
from PyQt5.QtCore import Qt
from page_home import HomePage
from page_rooms import RoomSelectionPage
from page_login import LoginPage
from page_checkout import CheckoutPage
from page_confirmation import ConfirmationPage
from page_register import RegisterPage


class HotelBookingApp:
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self._setup_main_window()
        self._setup_pages()
    
    def _setup_main_window(self):
        # Create main window
        self.main_window = QWidget()
        self.main_window.setWindowTitle("Hotel Eleon - Booking System")
        self.main_window.resize(1920, 1080)
        
        # Stack widget holds all pages
        self.stacked_widget = QStackedWidget(self.main_window)
        self.stacked_widget.setGeometry(0, 0, 1920, 1080)
    
    def _setup_pages(self):
        # Home page (index 0)
        page_home = QWidget()
        HomePage(page_home, self.stacked_widget)
        self.stacked_widget.addWidget(page_home)
        
        # Room selection page (index 1) - with scroll
        page_rooms = QWidget()
        RoomSelectionPage(page_rooms, self.stacked_widget)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(page_rooms)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.stacked_widget.addWidget(scroll_area)
        
        # Login page (index 2)
        page_login = QWidget()
        self.login_page = LoginPage(page_login, self.stacked_widget)
        self.stacked_widget.addWidget(page_login)
        
        # Checkout page (index 3)
        page_checkout = QWidget()
        CheckoutPage(page_checkout, self.stacked_widget, self.login_page)
        self.stacked_widget.addWidget(page_checkout)
        
        # Confirmation page (index 4)
        page_confirmation = QWidget()
        ConfirmationPage(page_confirmation, self.stacked_widget)
        self.stacked_widget.addWidget(page_confirmation)
        
        # Register page (index 5)
        page_register = QWidget()
        RegisterPage(page_register, self.stacked_widget)
        self.stacked_widget.addWidget(page_register)
        
        # Start on home
        self.stacked_widget.setCurrentIndex(0)
    
    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())


def main():
    app = HotelBookingApp()
    app.run()


if __name__ == "__main__":
    main()