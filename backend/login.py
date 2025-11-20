"""login.py
This file contains the login class which handles user authentication and registration.
Programmer: Taksh Joshi
date of code: November 2nd, 2025
modifications: Added default password for admin user, added password change functionality, added email validation, added user registration, added logout functionality, added user role checks
"""
import csv
from datetime import datetime
from backend.customer import Customer
from backend.customer_controller import CustomerController
from backend.address import Address

class LoginSystem:
     """
    This class handles the login, registration, and authentication
    of users in the system
    Attributes:
    csv_file : str
    The file path to the CSV that contains user data
    customer_controller : CustomerController
    Controller that manages customer data
    current_user : dict or None
    Information about the currently logged-in user
    """

    def __init__(self, csv_file="users.csv"):
         """
        Initializes the LoginSystem with a given CSV file.
         Parameters:
        csv_file : str
            The file path for the CSV containing user data. Defaults to 'users.csv'
        """
        self.csv_file = csv_file
        self.customer_controller = CustomerController()
        self.current_user = None
        self.load_users()
    
    def load_users(self):
          """
        Loads the users from the CSV file and adds non-admin users to the customer controller.
        
        Creates the CSV file with a default admin if it doesn't exist.
        """
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Create customer objects for non-admin users
                    if row['role'] != 'admin':
                        address = Address("", "", "", "", "")
                        if not self.customer_controller.find_customer_by_email(row['email']):
                            self.customer_controller.add_customer(
                                row['first_name'],
                                row['last_name'],
                                row['email'],
                                row.get('phone', ''),
                                address
                            )
        except FileNotFoundError:
            # Create CSV file with default admin user if it doesn't exist
            self._create_default_csv()
    
    def _create_default_csv(self):
        """Create default CSV file with admin user"""
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['username', 'password', 'role', 'first_name', 'last_name', 'email', 'phone', 'registered_date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            # Default admin credentials: username = admin, password = admin123
            writer.writerow({
                'username': 'admin',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@hotel.com',
                'phone': '',
                'registered_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    
    def login(self, username, password):
        """
        Authenticates the user with the given username and password.
        Parameters:
        username : str
        The username of the user trying to log in
        password : str
        The password of the user trying to log in
        Returns:
        tuple
        A tuple containing a success flag and a message
        """
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username and row['password'] == password:
                        self.current_user = {
                            'username': row['username'],
                            'role': row['role'],
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'email': row['email'],
                            'phone': row.get('phone', '')
                        }
                        return True, f"Welcome, {row['first_name']}!"
                return False, "Invalid username or password"
        except FileNotFoundError:
            return False, "User database not found"
    
    def register(self, username, password, first_name, last_name, email, phone="", role="customer"):
         """
        Registers a new user in the system
        Parameters:
        username : str
        The username for the new user
        password : str
        The password for the new user
        first_name : str
        The first name of the new user
        last_name : str
        The last name of the new user
        email : str
        The email address of the new user
        phone : str, optional
        The phone number of the new user 
        role : str, optional
        The role of the new user (default is "customer")
        Returns:
        tuple
        A tuple containing a success flag and a message
        """
        # Validate email
        if not self.customer_controller.is_valid_email(email):
            return False, "Invalid email format"
        
        # Check if username already exists
        if self._username_exists(username):
            return False, "Username already exists"
        
        # Check if email already exists
        if self._email_exists(email):
            return False, "Email already registered"
        
        # Add to CSV
        with open(self.csv_file, 'a', newline='') as file:
            fieldnames = ['username', 'password', 'role', 'first_name', 'last_name', 'email', 'phone', 'registered_date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({
                'username': username,
                'password': password,
                'role': role,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'registered_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Add customer to customer controller
        address = Address("", "", "", "", "")
        self.customer_controller.add_customer(first_name, last_name, email, phone, address)
        
        return True, "Registration successful! Please login."
    
    def _username_exists(self, username):
         """
        Checks if a username already exists in the system.
         Parameters:
         username : str
        The username to check.
        Returns:
        bool
        True if the username exists, False otherwise.
        """
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username:
                        return True
        except FileNotFoundError:
            return False
        return False
    
    def _email_exists(self, email):
           """
        Checks if an email already exists in the system
        Parameters:
        email : str
        The email to check
        Returns:
        bool
        True if the email exists, False otherwise
        """
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['email'] == email:
                        return True
        except FileNotFoundError:
            return False
        return False
    
    def logout(self):
       """
        Logs the current user out of the system.
        Returns:
        tuple
        A tuple containing a success flag and a message.
        """
        if self.current_user:
            username = self.current_user['username']
            self.current_user = None
            return True, f"Goodbye, {username}!"
        return False, "No user currently logged in"
    
    def is_logged_in(self):
         """
        Checks if a user is currently logged in.
        Returns:
        bool
        True if a user is logged in, False otherwise.
        """
        return self.current_user is not None
    
    def get_current_user(self):
      """
        Gets the current logged-in user.
        Returns:
        dict or None
        Information about the current user, or None if no user is logged in.
        """
        return self.current_user
    
    def is_admin(self):
        """
        Checks if the current user is an admin.
        Returns:
        bool
        True if the current user is an admin, False otherwise.
        """
        return self.current_user and self.current_user['role'] == 'admin'
    
    def is_manager(self):
         """
        Checks if the current user is a manager.
        Returns:
        bool
        True if the current user is a manager, False otherwise.
        """
        return self.current_user and self.current_user['role'] == 'manager'
    
    def change_password(self, old_password, new_password):
        """
        Changes the password for the currently logged-in user.
        Parameters:
        old_password : str
        The current password of the user.
        new_password : str
        The new password for the user.
        Returns:
        tuple
        A tuple containing a success flag and a message.
        """
        if not self.current_user:
            return False, "No user logged in"
        
        # Read all users
        users = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                users = list(reader)
        except FileNotFoundError:
            return False, "User database not found"
        
        # Update password
        updated = False
        for user in users:
            if user['username'] == self.current_user['username']:
                if user['password'] != old_password:
                    return False, "Old password is incorrect"
                user['password'] = new_password
                updated = True
                break
        
        if not updated:
            return False, "User not found"
        
        # Write back to CSV
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['username', 'password', 'role', 'first_name', 'last_name', 'email', 'phone', 'registered_date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        
        return True, "Password changed successfully"
    
    def get_default_admin_credentials(self):
        """Return the default admin credentials for reference"""
        return {
            'username': 'admin',
            'password': 'admin123'
        }