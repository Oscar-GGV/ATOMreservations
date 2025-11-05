import unittest
from backend.customer import Customer
from backend.address import Address
class TestCustomer(unittest.TestCase):
    def test_customer_creation(self):
        add = Address("18206 Plummer st", "Northridge", "California", "91330", "USA")
        cust = Customer("Joe", "Apple", "JoeApple@gmail.com", "818-203-2819", add)
        self.assertEqual(cust.first_name, "Joe")
        self.assertEqual(add.street, "18206 Plummer st")
    def test_customer_count_increases(self):
        start_count = Customer.get_customercount()
        add = Address("18206 Plummer st", "Northridge", "California", "91330", "USA")
        cust = Customer("Joe", "Apple", "JoeApple@gmail.com", "818-203-2819", add)
        self.assertEqual(Customer.get_customercount(), start_count + 1)
if __name__ == "__main__":
    unittest.main()




