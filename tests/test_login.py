import unittest
from backend.login import LoginSystem

class TestLogin(unittest.TestCase):
    """Test class for LoginSystem"""

    def test_successful_login(self):
        """TEST 1: Successful Login with Correct Credentials"""
        login_sys = LoginSystem()  # Instantiating the LoginSystem directly
        
        # Call the login method with correct credentials
        success, message = login_sys.login('admin', 'admin123')

        # Expected values
        expected_success = True
        expected_username = 'admin'
        expected_role = 'admin'
        
        # Observed values
        observed_success = success
        observed_username = login_sys.current_user['username'] if login_sys.current_user else None
        observed_role = login_sys.current_user['role'] if login_sys.current_user else None
        
        # Print expected vs observed
        print(f"Input: username='admin', password='admin123'")
        print(f"Expected Success: {expected_success}")
        print(f"Observed Success: {observed_success}")
        print(f"Expected Username: {expected_username}")
        print(f"Observed Username: {observed_username}")
        print(f"Expected Role: {expected_role}")
        print(f"Observed Role: {observed_role}")
        print(f"Message: {message}")
        
        # PyUnit assertions
        self.assertEqual(observed_success, expected_success, "Login should succeed")
        self.assertEqual(observed_username, expected_username, "Username should match")
        self.assertEqual(observed_role, expected_role, "Role should match")
        
        print("TEST PASSED - Admin login successful!")
    
    def test_failed_login_wrong_password(self):
        """TEST 2: Failed Login with Wrong Password"""
        login_sys = LoginSystem()
        
        # Call login method with wrong password
        success, message = login_sys.login('admin', 'wrongpassword')
        
        # Expected values
        expected_success = False
        expected_current_user = None
        
        # Observed values
        observed_success = success
        observed_current_user = login_sys.current_user
        
        # Print expected vs observed
        print(f"Input: username='admin', password='wrongpassword'")
        print(f"Expected Success: {expected_success}")
        print(f"Observed Success: {observed_success}")
        print(f"Expected Current User: {expected_current_user}")
        print(f"Observed Current User: {observed_current_user}")
        print(f"Message: {message}")
        
        # PyUnit assertions
        self.assertEqual(observed_success, expected_success, "Login should fail")
        self.assertEqual(observed_current_user, expected_current_user, "Current user should be None")
        
        print("TEST PASSED - Wrong password correctly rejected!")
    
    def test_failed_login_nonexistent_user(self):
        """TEST 3: Failed Login with Non-existent Username"""
        login_sys = LoginSystem()
        
        # Call login method with fake username
        success, message = login_sys.login('fakeuser', 'password123')
        
        # Expected values
        expected_success = False
        expected_current_user = None
        
        # Observed values
        observed_success = success
        observed_current_user = login_sys.current_user
        
        # Print expected vs observed
        print(f"Input: username='fakeuser', password='password123'")
        print(f"Expected Success: {expected_success}")
        print(f"Observed Success: {observed_success}")
        print(f"Expected Current User: {expected_current_user}")
        print(f"Observed Current User: {observed_current_user}")
        print(f"Message: {message}")
        
        # PyUnit assertions
        self.assertEqual(observed_success, expected_success, "Login should fail")
        self.assertEqual(observed_current_user, expected_current_user, "Current user should be None")
        
        print("TEST PASSED - Non-existent user correctly rejected!")


# Run the tests
if __name__ == '__main__':
    print("\nUNIT TESTING: LoginSystem Class - login() Method")
    unittest.main()
  