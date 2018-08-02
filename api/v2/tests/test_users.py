"""
test user functions
"""
import unittest
import os
import sys

from common import Common

sys.path.insert(0, os.path.abspath(".."))


from __init__ import APP

class TestUsers(unittest.TestCase):
    """
    test validity
    """
    def test_authorize(self):
        """
    test validity of a token
    """
        test = Common()
        self.assertFalse(test.authorize(''), False)
        #self.assertTrue(test.authorize('qwsdfgiujhgfde'), True)
    def test_valid_email(self):
        """
    test validity of an email
    """
        test = Common()
        self.assertTrue(test.valid_email('koechkevin92@gmail.com'), True)
        self.assertFalse(test.valid_email('koechkevin92@gmailcom'), False)
class TestUserLogin(unittest.TestCase):
    """
    test validity of login function when empty parameters provided
    """
    def setUp(self):
        self.APP = APP.test_client()
    def test_post(self):
        """
    test validity of login function when empty parameters provided
    """
        response = self.APP.post('/api/v2/users/login', json={})
        self.assertEqual(response.status_code, 422)
class TestUserLogout(unittest.TestCase):
    """
    test validity of logout function when wrong method provided
    """
    def test_get(self):
        """
    test validity of logout function when wrong method provided
    """
        self.APP = APP.test_client()
        response = self.APP.post('/api/v2/users/logout')
        self.assertEqual(response.status_code, 405)
        test = APP.test_client().get('/api/v2/logout').status_code
        self.assertEqual(test, 404)
class TestRegister(unittest.TestCase):
    """
    test register and get account details
    """
    def test_post(self):
        """
    test for wrong routes and wrong credentials provided on registration
    """
        self.assertEqual\
            (APP.test_client().get('/api/v2/users/register/').status_code, 404)
        self.assertEqual(APP.test_client().post('/api/v2/users/register', json={\
             "lname":"koech", "email":"kkkoech",\
        "username":"kibitok", "password":"1234", "cpassword":\
        "1234"}).status_code, 422)
    def test_get(self):
        """
    test for status code when the get register function gets called.
    """
        with APP.test_client()as self.APP:
            response = self.APP.get('/api/v2/users/register')
            self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()
