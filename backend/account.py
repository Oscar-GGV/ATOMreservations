# account.py
from backend.customer import Customer
from backend.customer_controller import CustomerController
import hashlib
import uuid

class Account:
    """
    Represents a user account linked to a customer.
    Attributes:
    - account_id: Unique identifier for the account
    - customer: Customer object linked to this account
    - email: Account login email
    - password_hash: Hashed password for security
    - role: Role of the account ("customer" or "manager")
    """
    accounts = {}

    def __init__(self, customer, email, password, role="customer"):
        """
        Initializes an Account instance.
        Args:
        - customer: Customer object to link with this account
        - email: Email for account login
        - password: Plain text password (will be hashed)
        - role: Role of the account ("customer" or "manager")
        """
        self.account_id = str(uuid.uuid4())
        self.customer = customer
        self.email = email.lower()
        self.password_hash = self._hash_password(password)
        self.role = role
        Account.accounts[self.account_id] = self

    def _hash_password(self, password):
        """
        Hashes the password using SHA-256.
        Args:
        - password: Plain text password
        Returns:
        - Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        """
        Checks if the provided password matches the stored password hash.
        Args:
        - password: Plain text password to check
        Returns:
        - True if the password matches, False otherwise
        """
        return self._hash_password(password) == self.password_hash

    @classmethod
    def login(cls, email, password):
        """
        Authenticates a user by email and password.
        Args:
        - email: Email for account login
        - password: Plain text password
        Returns:
        - Account object if authentication is successful, None otherwise
        """
        for account in cls.accounts.values():
            if account.email == email.lower() and account.check_password(password):
                return account
        return None

    @classmethod
    def get_account_by_customer(cls, customer):
        """
        Retrieves an account linked to a specific customer.
        Args:
        - customer: Customer object
        Returns:
        - Account object if found, None otherwise
        """
        for account in cls.accounts.values():
            if account.customer == customer:
                return account
        return None

    def __str__(self):
        """
        Returns a string representation of the Account.
        Returns:
        - String describing the account
        """
        return f"Account {self.email} ({self.role}) linked to {self.customer.first_name} {self.customer.last_name}"
