import unittest
from backend.customer_controller import CustomerController
from backend.address import Address
from backend.customer import Customer

#IMPORTANT****** cannot have more than one instance at the same time because the csv file only can handle one read and write at the same time
  #because of this tests will be run one at time and ones not running will be commented out 
    
class TestCustomerController(unittest.TestCase):
 
    def test_add_customer(self):
        
        cc = CustomerController() #instance of the customer controller 
        #test number 1 - checks find_customer_by_email method - should return false because customer already 
        #exists in the csv file
        """
        address = Address("123 csun street", "Northridge", "CA", "91330", "USA") #object of the address

        result = cc.add_customer("oscar", "g", "csun@gmail.com", "818-123-4567", address)
        self.assertTrue(result) 
       
        #test number 2 - checks add_customer method - should return ok because customer with same email doesnt exist yet
        """
        """
        address = Address("1234 superman street", "metropolis", "OK", "23939", "USA") 
        result = cc.add_customer("Super", "man","superman@gmail.com","818-987-6543", address)
        self.assertTrue(result)
        """

        #test number 3 - deletes customer from csv file -should return true and nothing should be in csv
        """"
        address = Address("1234 sepulveda street", "north Hills", "CA", "91343", "USA")
        cc.add_customer("youshouldnotseeme","test","yippie@gmail.com", "818-132-4567", address)
        result = cc.remove_customer("yippie@gmail.com")
        self.assertTrue(result)
        """

        #test number 4 - tries to delete customer from csv file - should return true and there should be no oscar 
        # g should be in csv
        """"
        result = cc.remove_customer("csun@gmail.com")
        self.assertTrue(result)
        """

        #test number 5 - tests the find_customer_by_email method by itself 
        """
        address = Address("1111 disney street", "anaheim", "CA", "92802", "USA")
        cc.add_customer("Mickey", "mouse", "disney@gmail.com", "111-111-1111", address)
        found = cc.find_customer_by_email("disney@gmail.com")
        self.assertIsNotNone(found, "Customer should be found")
        self.assertEqual(found.first_name, "mickey") #purposefuly mispell name to see the customer it retrieves
        """
        #test number 6 tests the is valid email method - should return false because email is invalid
        
        address = Address("20202 minecraft street", "minecraft city", "mc", "20172", "Minecraftland")
        result = cc.add_customer("steve", "miner", "notvalid", "818-123-4567", address)
        self.assertTrue(result)
        


        

       




if __name__ == "__main__":
    unittest.main()
