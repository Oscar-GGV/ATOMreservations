"""address.py
This file contains the Address class which represents an address in the hotel reservation system.
Programmer: Oscar Guevara
date of code: october 4th, 2025"""
class Address:
    """Represents an address in the hotel reservation system."""
    def __init__(self, street, city, state, zipcode, country):
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country
