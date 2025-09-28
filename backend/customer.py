from address import Address 
#imports the address class
class Customer:
    number_of_customers = 0
    def __init__(self, first_name, last_name, email, phone, address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        #Here the instance of address is being imported from address.py
        Customer.add_to_customercount()
        #here the code uses the class method add_to_customercount in order to save the number of "Customer" objects created by the init
    @classmethod
    def get_customercount(cls):
        return cls.number_of_customers
    #uses a class method to return the number of customers that is shared by all instances not just individual instance  
    @classmethod  
    def add_to_customercount(cls):
        cls.number_of_customers += 1
        #used classmethod so it keeps the variable for the entire class, makes it easier to get the information later.
    
        
    
