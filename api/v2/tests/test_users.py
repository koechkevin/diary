import unittest

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
from common import Common

from __init__ import app

class TestUsers(unittest.TestCase):
    def test_authorize(self):
        test = Common()
        self.assertFalse(test.authorize(''), False)
        #self.assertTrue(test.authorize('qwsdfgiujhgfde'), True)
    def test_valid_email(self):
        test = Common()
        self.assertTrue(test.valid_email('koechkevin92@gmail.com'), True)
        self.assertFalse(test.valid_email('koechkevin92@gmailcom'), False)
class TestUserLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_post(self):
        response = self.app.post('/api/v2/users/login', json={})
        self.assertEqual(response.status_code, 422) 
class TestUserLogout(unittest.TestCase):
    def test_get(self):
        self.app = app.test_client()
        response = self.app.post('/api/v2/users/logout')
        self.assertEqual(response.status_code, 405)
        test = app.test_client().get('/api/v2/logout').status_code
        self.assertEqual(test, 404)
class TestRegister(unittest.TestCase):
    def test_post(self):
        self.assertEqual\
            (app.test_client().get('/api/v2/users/register/').status_code, 404)
        self.assertEqual(app.test_client().post('/api/v2/users/register', json={\
             "lname":"koech", "email":"kkkoech",\
        "username":"kibitok", "password":"1234", "cpassword":\
        "1234"}).status_code, 422)
    def test_get(self):
        with app.test_client()as self.app:
            response = self.app.get('/api/v2/users/register')
            self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
            unittest.main()
