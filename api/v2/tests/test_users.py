import unittest
import json

import os,sys
sys.path.insert(0, os.path.abspath(".."))
from users import *
from __init__ import *


class TestUsers(unittest.TestCase):
    def test_register(self):  
        self.assertEqual\
            (app.test_client().get('/api/v2/users/register').status_code, 405)
        self.assertEqual(app.test_client().post('/api/v2/users/register', json={\
            "fname":"kevin", "lname":"koech", "email":"kkkoech",\
        "username":"kibitok", "password":"1234", "cpassword":\
        "1234"}).status_code, 409)
        t = app.test_client()
        res = t.post('/api/v2/users/register', json={"fname":"kevin",\
        "lname":"koech", "email":"kkkoech", "username":"kibitoks",\
        "password":"1234", "cpassword":"1234"})
        self.assertEqual(json.loads(res.get_data(as_text=True)), 'please enter a valid email')
        self.assertEqual(res.status_code, 403)
    def test_login(self):
        tester = app.test_client()
        response = tester.post('/api/v2/users/login', json={"username":"kiprop", "password":"1234"})
        self.assertEqual(response.status_code, 401)
    def test_logout(self):
        t = app.test_client().get('/api/v2/users/logout').status_code
        self.assertEqual(t, 422)
        te = app.test_client().get('/api/v2/logou').status_code
        self.assertEqual(te, 404)
        
if __name__ == '__main__':
            unittest.main()        