import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QScrollArea
)
from PyQt5.QtCore import Qt
from page1 import build_page1
from page2 import build_page2
from page3 import build_page3

app = QApplication(sys.argv)

# Main container widget
main_window = QWidget()
main_window.setWindowTitle("Modular UI with Shared Header")
main_window.resize(1920, 1080)

# Stack of pages (each builds its own header)
stacked_widget = QStackedWidget(main_window)
stacked_widget.setGeometry(0, 0, 1920, 1080)  # header now inside each page

# Page 1
page1 = QWidget()
build_page1(page1, stacked_widget, page2_index=1)
stacked_widget.addWidget(page1)

# Page 2 (inside scroll area)
page2_widget = QWidget()
build_page2(page2_widget, stacked_widget, page1_index=0)
scroll = QScrollArea()
scroll.setWidgetResizable(True)
scroll.setWidget(page2_widget)
scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
stacked_widget.addWidget(scroll)

# Page 3
page3 = QWidget()
build_page3(page3, stacked_widget=stacked_widget, page2_index=1)  # Page 2 is scroll at index 1
stacked_widget.addWidget(page3)

# Show Page 1 by default
stacked_widget.setCurrentIndex(0)

main_window.show()
sys.exit(app.exec_())
