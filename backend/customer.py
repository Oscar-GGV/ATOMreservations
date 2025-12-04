""""Customer.py 
This file contains the Customer class which represents a customer in the hotel reservation system.
Programmer: Oscar Guevara
date of code: October 4th, 2025
"""
from backend.address import Address 
#imports the address class
class Customer:
    """represents a customer in the hotel reservation system."""
    number_of_customers = 0
    def __init__(self, first_name, last_name, email, phone, address):
        """Customer constructor to initialize customer attributes.
            parameters:
            first_name (str): The first name of the customer.
            last_name (str): The last name of the customer.
            email (str): The email address of the customer.
            phone (str): The phone number of the customer.
            address (Address): The address object of the customer.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        #address is an object of the Address class imported from address.py
        Customer.add_to_customercount()
        #here the code uses the class method add_to_customercount in order to save the number of "Customer" objects created by the init
    @classmethod
    def get_customercount(cls):
        """Returns the total number of customers."""
        return cls.number_of_customers
    #uses a class method to return the number of customers that is shared by all instances not just individual instance  
    @classmethod  
    
    def add_to_customercount(cls):
        """Increments the customer count by one."""
        cls.number_of_customers += 1
        #used classmethod so it keeps the variable for the entire class, makes it easier to get the information later.
    
    def get_custinfo(self):
        """Returns a dictionary with the customer's information."""
        return { "Firstname" : self.first_name, "Lastname" :self.last_name, "Email" : self.email, "Phone number" : self.phone, "Address": self.address }
    #returns a dictionary, might be useful later on when implementing the front end and saving data {"Key" : "Value"}
    
    #potential next step could be the file/database interaction(either reading/writing text files or excel)
    
