from PyQt5.QtWidgets import QPushButton, QTextEdit, QFrame, QCalendarWidget, QLabel

# Create a button
def create_custom_button(text, x, y, width, height, parent):
    button = QPushButton(text, parent)
    button.move(x, y)
    button.setFixedSize(width, height)
    return button

# Connect button to an action
def connect_action(button, action_function):
    button.clicked.connect(action_function)

# Create a textbox
def create_textbox(x, y, width, height, parent, placeholder="Type here..."):
    box = QTextEdit(parent)
    box.move(x, y)
    box.setFixedSize(width, height)
    box.setPlaceholderText(placeholder)
    return box

# Create a rectangle block
def create_rectangle(x, y, width, height, color, parent):
    rect = QFrame(parent)
    rect.setGeometry(x, y, width, height)
    rect.setStyleSheet(f"background-color: {color};")
    return rect

# Create a calendar
def create_calendar(x, y, width, height, parent):
    calendar = QCalendarWidget(parent)
    calendar.move(x, y)
    calendar.resize(width, height)
    calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
    return calendar

# Toggle visibility
def toggle_widget(widget):
    if widget.isVisible():
        widget.hide()
    else:
        widget.show()

# Create a simple label
def create_label(text, x, y, parent):
    label = QLabel(text, parent)
    label.move(x, y)
    return label

def create_header(parent, show_back=False, stacked_widget=None, back_target_index=0):
    # Create black rectangle header
    header = create_rectangle(0, 0, 1980, 150, "black", parent)

    # Optional Back button
    if show_back and stacked_widget is not None:
        back_button = create_custom_button("Back", 50, 70, 150, 40, parent)
        connect_action(back_button, lambda: stacked_widget.setCurrentIndex(back_target_index))
        back_button.raise_()

    # Navigation label
    label = create_label("Home\t\t\tAbout\t\t\tReservation\t\t\tAmenites", 450, 70, header)
    label.setStyleSheet("color: white; font-size: 22px;")

    return header


# Guest box with counter
def create_guest_box_with_counter(x, y, width, height, parent, on_value_change=None):
    box = QFrame(parent)
    box.setGeometry(x, y, width, height)
    box.setStyleSheet("background-color: white; border: none;")

    # Adults Label
    adults_label = QLabel("Adults", box)
    adults_label.move(20, 20)
    adults_label.setStyleSheet("font-size: 16px;")

    # Display for number (starts at 1)
    count_display = QLabel("1", box)
    count_display.move(130, 20)
    count_display.setFixedWidth(20)
    count_display.setStyleSheet("font-size: 16px;")

    # Left arrow button <
    left_button = QPushButton("<", box)
    left_button.move(100, 15)
    left_button.setFixedSize(25, 25)

    # Right arrow button >
    right_button = QPushButton(">", box)
    right_button.move(145, 15)
    right_button.setFixedSize(25, 25)

    # Internal counter value
    counter = {"value": 1}

    def decrease():
        if counter["value"] > 1:
            counter["value"] -= 1
            count_display.setText(str(counter["value"]))
            if on_value_change:
                on_value_change(counter["value"])

    def increase():
        if counter["value"] < 8:
            counter["value"] += 1
            count_display.setText(str(counter["value"]))
            if on_value_change:
                on_value_change(counter["value"])

    left_button.clicked.connect(decrease)
    right_button.clicked.connect(increase)

    return box, counter
