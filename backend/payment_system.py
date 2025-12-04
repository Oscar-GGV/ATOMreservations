"""payment_system.py
This file contains the Payment, Transaction, and PaymentController classes which handle 
payment processing in the hotel reservation system.
Programmer: Taksh Joshi
Date of code: November 29th, 2025
"""

import uuid
from datetime import datetime
import hashlib
import random


class Transaction:
    """Represents a unique transaction for payment tracking."""
    
    transaction_counter = 1000
    
    def __init__(self, payment_id, amount, payment_method):
        """
        Initializes a Transaction object with a unique transaction ID.
        
        Parameters:
            payment_id (str): The payment ID associated with this transaction.
            amount (float): The transaction amount.
            payment_method (str): Payment method used.
        """
        self.transaction_id = self._generate_transaction_id()
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.timestamp = datetime.now()
        self.status = "completed"
        Transaction.transaction_counter += 1
    
    def _generate_transaction_id(self):
        """
        Generates a unique transaction ID.
        Format: TXN-YYYYMMDD-NNNN-XXXX
        where YYYYMMDD is date, NNNN is counter, XXXX is random hex
        
        Returns:
            str: Unique transaction ID.
        """
        date_part = self.timestamp.strftime("%Y%m%d") if hasattr(self, 'timestamp') else datetime.now().strftime("%Y%m%d")
        counter_part = f"{Transaction.transaction_counter:04d}"
        random_part = f"{random.randint(0, 65535):04X}"
        return f"TXN-{date_part}-{counter_part}-{random_part}"
    
    def get_transaction_info(self):
        """
        Returns transaction information.
        
        Returns:
            dict: Transaction details.
        """
        return {
            "transaction_id": self.transaction_id,
            "payment_id": self.payment_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status
        }


class Payment:
    """Represents a payment transaction in the hotel reservation system."""
    
    def __init__(self, reservation_id, customer, amount, payment_method, card_details=None):
        """
        Initializes a Payment object.
        
        Parameters:
            reservation_id (str): The reservation ID associated with this payment.
            customer (Customer): The customer making the payment.
            amount (float): The total amount to be paid.
            payment_method (str): Payment method - "card" or "cash".
            card_details (dict, optional): Dictionary containing card information if payment_method is "card".
                Expected keys: card_number, card_holder_name, expiry_date, cvv
        """
        self.payment_id = self._generate_payment_id()
        self.reservation_id = reservation_id
        self.customer = customer
        self.amount = amount
        self.payment_method = payment_method.lower()
        self.timestamp = datetime.now()
        self.status = "pending"
        self.transaction = None
        
        # Store masked card details for security
        if payment_method.lower() == "card" and card_details:
            self.card_details = self._mask_card_details(card_details)
        else:
            self.card_details = None
    
    def _generate_payment_id(self):
        """Generates a unique payment ID."""
        return f"PAY-{uuid.uuid4().hex[:8].upper()}"
    
    def create_transaction(self):
        """
        Creates a transaction for this payment.
        
        Returns:
            Transaction: The created transaction object.
        """
        self.transaction = Transaction(self.payment_id, self.amount, self.payment_method)
        return self.transaction
    
    def _mask_card_number(self, card_number):
        """
        Masks the card number, showing only the last 4 digits.
        
        Parameters:
            card_number (str): The full card number.
            
        Returns:
            str: Masked card number (e.g., "**** **** **** 1234").
        """
        # Remove any spaces or dashes
        clean_number = card_number.replace(" ", "").replace("-", "")
        if len(clean_number) < 4:
            return "****"
        return f"**** **** **** {clean_number[-4:]}"
    
    def _mask_card_details(self, card_details):
        """
        Creates a masked version of card details for secure storage.
        
        Parameters:
            card_details (dict): Dictionary containing card information.
            
        Returns:
            dict: Masked card details.
        """
        return {
            "card_number": self._mask_card_number(card_details.get("card_number", "")),
            "card_holder_name": card_details.get("card_holder_name", ""),
            "expiry_date": card_details.get("expiry_date", ""),
            "card_type": self._detect_card_type(card_details.get("card_number", ""))
        }
    
    def _detect_card_type(self, card_number):
        """
        Detects the card type based on the card number.
        
        Parameters:
            card_number (str): The card number.
            
        Returns:
            str: Card type (Visa, Mastercard, Amex, Discover, or Unknown).
        """
        clean_number = card_number.replace(" ", "").replace("-", "")
        
        if clean_number.startswith("4"):
            return "Visa"
        elif clean_number.startswith(("51", "52", "53", "54", "55")):
            return "Mastercard"
        elif clean_number.startswith(("34", "37")):
            return "American Express"
        elif clean_number.startswith("6011") or clean_number.startswith("65"):
            return "Discover"
        else:
            return "Unknown"
    
    def get_payment_summary(self):
        """
        Returns a summary of the payment transaction.
        
        Returns:
            dict: Payment summary information.
        """
        summary = {
            "payment_id": self.payment_id,
            "reservation_id": self.reservation_id,
            "customer_name": f"{self.customer.first_name} {self.customer.last_name}",
            "customer_email": self.customer.email,
            "amount": self.amount,
            "payment_method": self.payment_method.capitalize(),
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status
        }
        
        if self.transaction:
            summary["transaction_id"] = self.transaction.transaction_id
            summary["transaction_timestamp"] = self.transaction.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        if self.card_details:
            summary["card_details"] = self.card_details
        
        return summary


class PaymentController:
    """Controller for handling payment operations in the reservation system."""
    
    def __init__(self):
        """Initializes the PaymentController with empty payment and transaction databases."""
        self.payments_db = {}  # {payment_id: Payment object}
        self.transactions_db = {}  # {transaction_id: Transaction object}
    
    def validate_card_details(self, card_details):
        """
        Validates card details format.
        
        Parameters:
            card_details (dict): Dictionary containing card information.
            
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        required_fields = ["card_number", "card_holder_name", "expiry_date", "cvv"]
        
        # Check if all required fields are present
        for field in required_fields:
            if field not in card_details or not card_details[field]:
                return False, f"Missing required field: {field}"
        
        # Validate card number (should be 13-19 digits)
        card_number = card_details["card_number"].replace(" ", "").replace("-", "")
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False, "Invalid card number format"
        
        # Validate CVV (should be 3-4 digits)
        cvv = card_details["cvv"]
        if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
            return False, "Invalid CVV format"
        
        # Validate expiry date format (MM/YY or MM/YYYY)
        expiry = card_details["expiry_date"]
        if "/" not in expiry:
            return False, "Invalid expiry date format (use MM/YY or MM/YYYY)"
        
        parts = expiry.split("/")
        if len(parts) != 2:
            return False, "Invalid expiry date format"
        
        month, year = parts[0].strip(), parts[1].strip()
        if not month.isdigit() or not year.isdigit():
            return False, "Invalid expiry date format"
        
        month_int = int(month)
        if month_int < 1 or month_int > 12:
            return False, "Invalid expiry month"
        
        # Check if card is expired
        current_date = datetime.now()
        year_int = int(year)
        if len(year) == 2:
            year_int += 2000
        
        if year_int < current_date.year or (year_int == current_date.year and month_int < current_date.month):
            return False, "Card has expired"
        
        return True, "Valid"
    
    def process_payment(self, reservation_id, customer, amount, payment_method, card_details=None):
        """
        Processes a payment for a reservation.
        
        Parameters:
            reservation_id (str): The reservation ID.
            customer (Customer): The customer making the payment.
            amount (float): The amount to be paid.
            payment_method (str): Payment method - "card" or "cash".
            card_details (dict, optional): Card information if payment_method is "card".
            
        Returns:
            dict: Payment result with status and details.
        """
        # Validate payment method
        if payment_method.lower() not in ["card", "cash"]:
            return {
                "success": False,
                "message": "Invalid payment method. Must be 'card' or 'cash'."
            }
        
        # Validate amount
        if amount <= 0:
            return {
                "success": False,
                "message": "Invalid payment amount. Amount must be greater than zero."
            }
        
        # Validate card details if payment method is card
        if payment_method.lower() == "card":
            if not card_details:
                return {
                    "success": False,
                    "message": "Card details are required for card payments."
                }
            
            is_valid, error_message = self.validate_card_details(card_details)
            if not is_valid:
                return {
                    "success": False,
                    "message": f"Card validation failed: {error_message}"
                }
        
        # Create payment object
        payment = Payment(reservation_id, customer, amount, payment_method, card_details)
        
        # Create transaction for this payment
        transaction = payment.create_transaction()
        
        # Simulate payment processing
        payment.status = "completed"
        
        # Store payment and transaction in databases
        self.payments_db[payment.payment_id] = payment
        self.transactions_db[transaction.transaction_id] = transaction
        
        # Return success response
        return {
            "success": True,
            "message": "Payment processed successfully",
            "payment": payment.get_payment_summary()
        }
    
    def get_transaction_by_id(self, transaction_id):
        """
        Retrieves a transaction by its ID.
        
        Parameters:
            transaction_id (str): The transaction ID.
            
        Returns:
            Transaction or None: Transaction object if found, None otherwise.
        """
        return self.transactions_db.get(transaction_id)
    
    def get_transactions_by_payment(self, payment_id):
        """
        Retrieves all transactions associated with a payment.
        
        Parameters:
            payment_id (str): The payment ID.
            
        Returns:
            list: List of Transaction objects.
        """
        return [txn for txn in self.transactions_db.values() 
                if txn.payment_id == payment_id]
    
    def get_payment_by_id(self, payment_id):
        """
        Retrieves a payment by its ID.
        
        Parameters:
            payment_id (str): The payment ID.
            
        Returns:
            Payment or None: Payment object if found, None otherwise.
        """
        return self.payments_db.get(payment_id)
    
    def get_payments_by_reservation(self, reservation_id):
        """
        Retrieves all payments associated with a reservation.
        
        Parameters:
            reservation_id (str): The reservation ID.
            
        Returns:
            list: List of Payment objects.
        """
        return [payment for payment in self.payments_db.values() 
                if payment.reservation_id == reservation_id]
    
    def get_payments_by_customer(self, customer_email):
        """
        Retrieves all payments made by a customer.
        
        Parameters:
            customer_email (str): The customer's email.
            
        Returns:
            list: List of Payment objects.
        """
        return [payment for payment in self.payments_db.values() 
                if payment.customer.email == customer_email]
    
    def generate_receipt(self, payment_id):
        """
        Generates a receipt for a payment.
        
        Parameters:
            payment_id (str): The payment ID.
            
        Returns:
            str or None: Formatted receipt string or None if payment not found.
        """
        payment = self.get_payment_by_id(payment_id)
        
        if not payment:
            return None
        
        receipt = f"""
{'='*90}
                    PAYMENT RECEIPT
{'='*90}

Payment ID:         {payment.payment_id}
Transaction ID:     {payment.transaction.transaction_id if payment.transaction else 'N/A'}
Reservation ID:     {payment.reservation_id}
Date & Time:        {payment.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

{'='*90}
                  CUSTOMER INFORMATION
{'='*90}

Name:               {payment.customer.first_name} {payment.customer.last_name}
Email:              {payment.customer.email}
Phone:              {payment.customer.phone}

{'='*90}
                  PAYMENT DETAILS
{'='*90}

Payment Method:     {payment.payment_method.capitalize()}
"""
        
        if payment.card_details:
            receipt += f"""Card Type:          {payment.card_details['card_type']}
Card Number:        {payment.card_details['card_number']}
Card Holder:        {payment.card_details['card_holder_name']}
"""
        
        receipt += f"""
Amount Paid:        ${payment.amount:.2f}
Status:             {payment.status.capitalize()}

{'='*90}
            Thank you for your business!
{'='*90}
"""
        return receipt
    
    def get_total_revenue(self):
        """
        Calculates the total revenue from all completed payments.
        
        Returns:
            float: Total revenue.
        """
        return sum(payment.amount for payment in self.payments_db.values() 
                   if payment.status == "completed")
    
    def get_payment_statistics(self):
        """
        Returns statistics about payments and transactions.
        
        Returns:
            dict: Payment statistics.
        """
        total_payments = len(self.payments_db)
        completed_payments = len([p for p in self.payments_db.values() if p.status == "completed"])
        total_revenue = self.get_total_revenue()
        
        card_payments = len([p for p in self.payments_db.values() if p.payment_method == "card"])
        cash_payments = len([p for p in self.payments_db.values() if p.payment_method == "cash"])
        
        total_transactions = len(self.transactions_db)
        
        return {
            "total_payments": total_payments,
            "completed_payments": completed_payments,
            "pending_payments": total_payments - completed_payments,
            "total_revenue": total_revenue,
            "card_payments": card_payments,
            "cash_payments": cash_payments,
            "average_payment": total_revenue / completed_payments if completed_payments > 0 else 0,
            "total_transactions": total_transactions
        }