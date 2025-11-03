# login.py

import csv
from datetime import datetime
from backend.customer import Customer
from backend.customer_controller import CustomerController
from backend.address import Address

class LoginSystem:
    def __init__(self, csv_file="users.csv"):
        self.csv_file = csv_file
        self.customer_controller = CustomerController()
        self.current_user = None
        self.load_users()
    
    def load_users(self):
        """Load users from CSV file"""
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
        """Authenticate user with username and password"""
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
        """Register a new user"""
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
        """Check if username already exists"""
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
        """Check if email already exists"""
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
        """Logout current user"""
        if self.current_user:
            username = self.current_user['username']
            self.current_user = None
            return True, f"Goodbye, {username}!"
        return False, "No user currently logged in"
    
    def is_logged_in(self):
        """Check if a user is currently logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.current_user and self.current_user['role'] == 'admin'
    
    def is_manager(self):
        """Check if current user is manager"""
        return self.current_user and self.current_user['role'] == 'manager'
    
    def change_password(self, old_password, new_password):
        """Change password for current user"""
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