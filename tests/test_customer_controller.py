import unittest
from backend.customer_controller import CustomerController
from backend.address import Address
from backend.customer import Customer

#IMPORTANT****** cannot have more than one instance at the same time because the csv file only can handle one read and write at the same time
  #because of this tests will be run one at time and ones not running will be commented out 
    
class TestCustomerController(unittest.TestCase):
 
    def test_add_customer(self):
        
        cc = CustomerController() #instance of the customer controller 

        #test number 1 - run twice to see if duplicate email is caught

        #test command python3 -munittest discover -s tests
        """
        address = Address("123 csun street", "Northridge", "CA", "91330", "USA") #object of the address
        result = cc.add_customer("oscar", "g", "csun@gmail.com", "818-123-4567", address)
        print("This test is expected to pass when run the first time")
        self.assertTrue(result, "customer should be added successfully")
        print("check csv file to see if customer was added")

"""

       
        #test number 2 - checks add_customer method - expected to succeed, checks if more than one customer can be
        #added to customers.csv
        
        """
        address = Address("1234 superman street", "metropolis", "OK", "23939", "USA") 
        result = cc.add_customer("Super", "man","superman@gmail.com","818-987-6543", address)
        self.assertTrue(result, "Customer should be added successfully")
        print("check csv file and look for Super man")
        """

        #test number 3 - adds customer and deletes them from csv file 
        """
        
        address = Address("1234 sepulveda street", "north Hills", "CA", "91343", "USA")
        cc.add_customer("youshouldnotseeme","test","yippie@gmail.com", "818-132-4567", address)
        result = cc.remove_customer("yippie@gmail.com")
        self.assertTrue(result, "customer added and removed consecutively")
        print("there should be nothing added in customers.csv go check")
        print("look for youshouldnotseeme")
        
"""
        

        #test number 4 - test to delete an already existing customer
        
        result = cc.remove_customer("csun@gmail.com")
        self.assertTrue(result, "deleted oscar from 1st test")
        print("Success: Go check CSV if oscar was deleted from the customer.csv")
        

        #test number 5 - tests the find_customer_by_email method by itself 
        """
        address = Address("1111 disney street", "anaheim", "CA", "92802", "USA")
        cc.add_customer("Mickey", "mouse", "disney@gmail.com", "111-111-1111", address)
        found = cc.find_customer_by_email("disney@gmail.com")
        self.assertIsNotNone(found, "Customer should be found")
        self.assertEqual(found.first_name, "mickey") #purposefuly mispell name to see the customer it retrieves
        """
        
        #test number 6 tests the is valid email method - should return false because email is invalid
        """
        address = Address("20202 minecraft street", "minecraft city", "mc", "20172", "Minecraftland")
        result = cc.add_customer("steve", "miner", "notvalid", "818-123-4567", address)
        if self.assertTrue(result):
            print("TestFailed:Invalid email accepted")
        else:
            print("test passed: invalid email rejected")
            """
        


        

       




if __name__ == "__main__":
    unittest.main()
