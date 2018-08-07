"""
test entries
"""
import unittest

import os
import sys
import json
import psycopg2

sys.path.insert(0, os.path.abspath(".."))
from run import APP

class TestCreateEntry(unittest.TestCase):
    def setUp(self):
        self.APP = APP.test_client()
        self.APP.post('/api/v2/users/register', json={"fname": "kibish",\
                                                      "username":"test", \
                                                      "password":"kev12345",\
                                                      "lname":"kipkoech",\
                                                      "cpassword":"kev12345",\
                                                      "email":"tests@gmail.com"
                                                      })       
 
    def test_post(self):
        """
test return status code for no provided token
"""
        res = self.APP.post('/api/v2/users/login', json={"username":"test", "password":"kev12345"})
        token = res.get_json()["token"]
        response = self.APP.post('/api/v2/entries', headers = {"x-access-token":token},\
        json={"title":"test", "entry":"successful"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "entry was successfully saved")
    def test_get(self):
        """
test return ok for no token provided
"""
        with APP.test_client() as test:
            response = test.get('/api/v2/entries?t')
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
class TestEntryId(unittest.TestCase):
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
test with entry id
"""
    def test_put(self):
        """
test wrong method modification
"""
        modify = APP.test_client().post\
        ('/api/v2/entries/3', json={"tittle":" "}).status_code
        self.assertEqual(modify, 405)
    def test_delete(self):
        """
test wrong entry route and method
"""
        with APP.test_client() as test:
            res = test.get('/api/v2/entries/delete_entry').status_code
            self.assertEqual(res, 404)
            response = test.delete('/api/v2/entries/3')
            self.assertEqual(response.status_code, 200)
    def test_get(self):
        """
test succesful response
"""
        test = APP.test_client()
        self.assertEqual(test.get('/api/v2/entries/8').status_code, 200)
if __name__ == '__main__':
    unittest.main()
