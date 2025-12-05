from datetime import datetime
from typing import Optional, Dict, List, Union


class BookingData:
    """
    Shared booking state between pages.
    Stored as a singleton so all pages see the same data.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.check_in: Optional[str] = None
        self.check_out: Optional[str] = None
        self.adults: int = 1
        self.selected_room: Optional[Dict[str, Union[str, float]]] = None
        self.reservation_id: Optional[str] = None

    def calculate_nights(self) -> Optional[int]:
        if not self.check_in or not self.check_out:
            return None

        try:
            d1 = datetime.strptime(self.check_in, "%Y-%m-%d")
            d2 = datetime.strptime(self.check_out, "%Y-%m-%d")
            nights = (d2 - d1).days
            return nights if nights > 0 else None
        except ValueError:
            return None

    def calculate_total_price(self) -> Optional[float]:
        if not self.selected_room:
            return None

        if "price" not in self.selected_room:
            return None

        price = self.selected_room["price"]

        if isinstance(price, str):
            try:
                price = float(price)
            except ValueError:
                return None
        elif not isinstance(price, (int, float)):
            return None

        nights = self.calculate_nights()
        if nights is None or nights <= 0:
            return None

        return price * nights

    def reset(self) -> None:
        self.check_in = None
        self.check_out = None
        self.adults = 1
        self.selected_room = None
        self.reservation_id = None


class CustomerData:
    """
    Shared customer information between checkout and confirmation pages.
    Also stored as a singleton.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.first_name: str = ""
        self.last_name: str = ""
        self.email: str = ""
        self.phone: str = ""
        self.date_of_birth: str = ""

        self.country: str = ""
        self.street: str = ""
        self.city: str = ""
        self.state: str = ""
        self.zip_code: str = ""

        self.card_name: str = ""
        self.card_number: str = ""
        self.exp_date: str = ""
        self.cvv: str = ""


class Room:
    """
    Simple room structure used by UI and RoomRepository.
    """

    def __init__(self, title: str, description: str, price: float):
        self.title = title
        self.description = description
        self.price = price

    def get_description_lines(self) -> List[str]:
        return [part.strip() for part in self.description.split(",")]


class RoomRepository:
    """
    In-memory list of rooms.
    """
    _rooms: List[Room] = [
        Room("Single Room", "1 Bed, 2 Guests Max, Free Wi-Fi", 100.0),
        Room("Double Room", "2 Beds, 4 Guests Max, Free Wi-Fi", 150.0),
        Room("Family Room", "3 Beds, 6 Guests Max, Extra Sofa Bed", 200.0),
        Room("VIP Suite", "1 King Bed, 3 Guests Max, Private Balcony", 300.0),
    ]

    @classmethod
    def get_all_rooms(cls) -> List[Room]:
        return cls._rooms