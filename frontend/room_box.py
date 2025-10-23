from PyQt5.QtWidgets import QLabel
from helpers import create_custom_button, create_label, create_rectangle, connect_action

def build_room_display(x, y, parent, room_data, on_select):
    width = 300
    height = 500

    # Main white box
    box = create_rectangle(x, y, width, height, "white", parent)
    box.setStyleSheet("border: 2px solid gray; border-radius: 10px;")

    # 🔷 Blue header
    header = create_rectangle(0, 0, width, 150, "lightblue", box)

    # 🏷️ Title
    title_label = create_label(room_data["title"], 10, 160, box)
    title_label.setStyleSheet("font-size: 16px; font-weight: bold; border: none; background: transparent;")

    # 📃 Description (comma-split)
    desc_parts = [part.strip() for part in room_data["description"].split(',')]
    desc_text = '\n'.join(f"• {line}" for line in desc_parts)
    description_label = create_label(desc_text, 10, 190, box)
    description_label.setStyleSheet("font-size: 13px; border: none; background: transparent;")

    # 🔵 Regular blue button with white "Select" text
    select_btn = create_custom_button("Select", 100, 450, 100, 35, box)
    select_btn.setStyleSheet("""
        QPushButton {
            background-color: #0078d4;
            color: white;
            font-size: 14px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #005fa3;
        }
    """)
    connect_action(select_btn, lambda: on_select(room_data["title"], room_data["description"]))

    return box