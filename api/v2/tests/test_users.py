"""
test user functions
"""
import unittest
import os
import sys
import psycopg2
import json

sys.path.insert(0, os.path.abspath(".."))

from flask import jsonify
from common import Common
from run import APP

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
        self.APP = APP.test_client()
        response = self.APP.post('/api/v2/users/login', \
        json={"username":"koechk", "password":""})
        self.assertEqual(response.get_json()["message"], "invalid credentials")
        self.assertEqual(response.status_code, 200)

class TestUserLogout(unittest.TestCase):
    def setUp(self):
        self.APP = APP.test_client()
        self.APP.post('/api/v2/users/register', json={"fname": "kibish",\
                                                      "username":"test", \
                                                      "password":"kev12345",\
                                                      "lname":"kipkoech",\
                                                      "cpassword":"kev12345",\
                                                      "email":"tests@gmail.com"
                                                      })        
    
    """
    test validity of logout function when wrong method provided
    """
    def test_get(self):
        """
    test validity of logout function when wrong method provided
    """
        res = self.APP.post('/api/v2/users/login', json={"username":"test", "password":"kev12345"})
        token = res.get_json()["token"]
        response = self.APP.post('/api/v2/users/logout')
        self.assertEqual(response.status_code, 405)
        tester = APP.test_client().get('/api/v2/users/logout', headers={"x-access-token":token})
        test = tester.status_code
        self.assertEqual(test, 200)
        self.assertEqual(tester.get_json()["message"], "you have been successfully logged out.Token invalidated")
    
    def tearDown(self):
        DBNAME = os.getenv('DBNAME')
        DBPWD = os.getenv('DBPWD')
        DBUSER = os.getenv('DBUSER')
        connection = psycopg2.connect(dbname=DBNAME, user=DBUSER, \
        host='localhost', password=DBPWD, port="5432")
        cursor = connection.cursor()
        cursor.execute("delete from users where username = 'test';")
        connection.commit()        
class TestRegister(unittest.TestCase):
    def setUp(self):
        self.APP = APP.test_client()
        self.APP.post('/api/v2/users/register', json={"fname": "kibish",\
                                                      "username":"test", \
                                                      "password":"kev12345",\
                                                      "lname":"kipkoech",\
                                                      "cpassword":"kev12345",\
                                                      "email":"tests@gmail.com"
                                                      })                                          
    """
    test register and get account details
    """
   
    def test_post(self):
        """
    test for wrong routes and wrong credentials provided on registration
    """ 
        self.assertEqual\
            (self.APP.get('/api/v2/users/register/').status_code, 404)
        
        self.assertEqual(\
        self.APP.post('/api/v2/users/register', json={"fname": "kibish",\
                                                      "username":"test", \
                                                      "password":"kev12345",\
                                                      "lname":"kipkoech",\
                                                      "cpassword":"kev12345",\
                                                      "email":"tests@gmail.com"
                                                      }).status_code, 409)
        
    def test_get(self):
        """
    test for status code when the get register function gets called.
    """
        resp = self.APP.post('/api/v2/users/login', json={"username":"test", "password":"kev12345"})
        token = resp.get_json()["token"] 
        print(token)
        response = self.APP.get('/api/v2/users/register', headers = {'x-access-token':token})
        self.assertEqual(response.get_json()["name"], "kibish kipkoech")
        self.assertEqual(response.get_json()["username"], "test")
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        DBNAME = os.getenv('DBNAME')
        DBPWD = os.getenv('DBPWD')
        DBUSER = os.getenv('DBUSER')
        connection = psycopg2.connect(dbname=DBNAME, user=DBUSER, \
        host='localhost', password=DBPWD, port="5432")
        cursor = connection.cursor()
        cursor.execute("delete from users where username = 'test';")
        connection.commit()

if __name__ == '__main__':
    unittest.main()