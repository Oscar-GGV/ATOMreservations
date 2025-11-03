# account.py
from backend.customer import Customer
from backend.customer_controller import CustomerController
import hashlib
import uuid

class Account:
    accounts = {}

    def __init__(self, customer, email, password, role="customer"):
        """
        customer: Customer object
        email: account login email
        password: plain text password
        role: "customer" or "manager"
        """
        self.account_id = str(uuid.uuid4())
        self.customer = customer
        self.email = email.lower()
        self.password_hash = self._hash_password(password)
        self.role = role
        Account.accounts[self.account_id] = self

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self._hash_password(password) == self.password_hash

    @classmethod
    def login(cls, email, password):
        for account in cls.accounts.values():
            if account.email == email.lower() and account.check_password(password):
                return account
        return None

    @classmethod
    def get_account_by_customer(cls, customer):
        for account in cls.accounts.values():
            if account.customer == customer:
                return account
        return None

    def __str__(self):
        return f"Account {self.email} ({self.role}) linked to {self.customer.first_name} {self.customer.last_name}"
