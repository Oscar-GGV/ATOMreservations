from backend.address import Address
from backend.customer import Customer
import re #used for email validation

class CustomerController:
    def __init__(self):
        self.customers = []
        #Func below creates customer and adds customer to list of Customers that will later be connected to either text file or excel
    def add_customer(self, first_name, last_name, email, phone, address):
        check_if_already_exists = self.find_customer_by_email(email)
        if check_if_already_exists:
            return False #Customer with email already exists in the system.
        customer = Customer(first_name, last_name, email, phone, address)
        self.customers.append(customer) #the customer is being appended to the customers list
        return True #Customer successfully added
    
    def find_customer_by_email(self, email): #email is customer email
        for customer in self.customers: # iterates through the list self.customers
            if customer.email == email: # checks for email given in the parameter, if found V
                return customer # returns the object of the customer
        return None #otherwise return None because customer wasn't found
    
    def update_customer(self, email, new_info): #parameters are the object, email and the new info
        customer = self.find_customer_by_email(email) 
        if customer: #if the customer is found should be True V
            customer.first_name = new_info.get("first_name", customer.first_name)
            customer.last_name = new_info.get("last_name", customer.last_name)
            customer.phone = new_info.get("phone", customer.phone) #customer.phone is equal to the new phone number
            customer.email = new_info.get("email", customer.email) #customer.email is now equal to the new email
            customer.address = new_info.get("address", customer.address)
            return True #after return True
        return False #customer not found return false/// maybe can add a new function later to deal with the fact that customer does not have an account
    
    def remove_customer(self, email): #remove_customer function parameters are the customer
        customer = self.find_customer_by_email(email) #finds the customer object by calling on the find customer func
        if customer: #should be true if customer was found V
            self.customers.remove(customer) #removes from the list
            return True #return true because the remove was successful 
        return False #return false because customer does not exist in system /// could be updated later to connect to a customer not found func.
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
        
    #Might add a get total customers for the manager report later on, MUST connect to something filewise, either excel or plain text
#hello this is a new change





        