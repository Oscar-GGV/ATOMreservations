"""customer-controller.py
This file contains the CustomerController class which manages customer operations in the hotel reservation system.
Programmer: Oscar Guevara
date of code: october 19th, 2025
modifications: novemeber 27th, 2025
"""
import csv
from backend.address import Address
from backend.customer import Customer
import re #used for email validation

class CustomerController:
    """Manages customer operations in the hotel reservation system."""
    def __init__(self, csv_file="customers.csv"):
        """Initializes the CustomerController with an empty customer list."""
        self.customers = []
        self.csv_file = csv_file
        self.load_customers_from_csv(self.csv_file)

    def add_customer(self, first_name, last_name, email, phone, address):
        """Adds a new customer to the system.
            parameters:first_name (str): The first name of the customer. last_name (str): The last name of the customer. email (str): The email address of the customer. phone (str): The phone number of the customer. address (Address): The address object of the customer.
            returns: bool: True if the customer was added successfully, False if a customer with the same email already exists."""
        exists = self.find_customer_by_email(email)
        if exists:
            return False #cant add customer if they already exist
#else
        customer = Customer(first_name, last_name, email, phone, address) #creates customer object
        self.customers.append(customer) #adds customer obj to customers list

    
        self.save_customers_to_csv(self.csv_file, customer) #saves customer to csv file

        return True
#end of add custmer method

    
    def find_customer_by_email(self, email): 
        """Finds a customer by their email address.
            parameters: email (str): The email address of the customer to find.
            returns: Customer: The customer object if found, None otherwise."""
        for customer in self.customers: # iterates through list
            if customer.email == email: # checks for email given
                return customer # returns customer object
        return None #Customer not found, none works as false here
    #end of find_custoemr_by_email method
    
    def update_customer(self, email, new_info): 
        """Updates a customer's information.
            parameters: email (str) new_info (dict): A dictionary containing the new customer information.
            returns: bool: True if the customer was updated successfully, False if the customer was not found."""
        customer = self.find_customer_by_email(email) 
        if customer: #true if customer was found
            customer.first_name = new_info.get("first_name", customer.first_name)
            customer.last_name = new_info.get("last_name", customer.last_name)
            customer.phone = new_info.get("phone", customer.phone) 
            customer.email = new_info.get("email", customer.email) 
            customer.address = new_info.get("address", customer.address)
            return True #after return True
        return False #customer not found return false/// maybe can add a new function later to deal with the fact that customer does not have an account
    
    def remove_customer(self, email): 
        """Removes a customer from the system.
            parameters: email (str)
            returns: bool: True if the customer was removed successfully, False if the customer was not found."""
        customer = self.find_customer_by_email(email) #customer = customer object/ TRUE
        if customer: #true
            self.customers.remove(customer) #removes from the list
            self.save_all_customers_to_csv(self.csv_file) #added demeber 3rd to update csv after removal
            return True #return true because the remove was successful 
        return False #return false because customer does not exist in system /// could be updated later to connect to a customer not found func.
    
    def is_valid_email(self, email):
        """Validates the format of an email address.
            parameters:
            email (str): The email address to validate.
            uses regular expressions to check for a valid email format.
            returns:
            bool: True if the email format is valid, False otherwise."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    def load_customers_from_csv(self, file_path):
        """Loads customers from a CSV file.
            parameters:
            file_path (str): The path to the CSV file.
            returns:
            None"""
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    address = Address(
                        row['street'],
                        row['city'],
                        row['state'],
                        row['zipcode'],
                        row['country']
                    )
                    customer = Customer(
                        row['first_name'],
                        row['last_name'],
                        row['email'],
                        row['phone'],
                        address
                    )

                    self.customers.append(customer)
        except FileNotFoundError:
            pass
    def save_customers_to_csv(self, file_path, customer):
        """appends a new customer to the CSV file."""
        file_exists = False
        try:
            with open(file_path, mode = 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
        with open (file_path, mode = 'a', newline = '') as file:
            fieldnames = ['first_name', 'last_name', 'email', 'phone', 'street', 'city', 'state', 'zipcode', 'country']
            writer = csv.DictWriter(file, fieldnames = fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone': customer.phone,
                'street': customer.address.street,
                'city': customer.address.city,
                'state': customer.address.state,
                'zipcode': customer.address.zipcode,
                'country': customer.address.country
            })
    def save_all_customers_to_csv(self, file_path):
        """rewrties the whole csv file with current customer."""
        with open(file_path, mode = 'w', newline = '') as file:
            fieldnames = ["first_name", "last_name", "email", "phone", "street", "city", "state", "zipcode", "country"]
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()

            for customer in self.customers:
                writer.writerow({
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "email": customer.email,
                    "phone": customer.phone,
                    "street": customer.address.street,
                    "city": customer.address.city,
                    "state": customer.address.state,
                    "zipcode": customer.address.zipcode,
                    "country": customer.address.country
                })
                ##important to note that when a conection to the front end is made, dict cannot be used directly, need to extract the values and send them as parameters to create the customer object.


                
        




    
    
        






        