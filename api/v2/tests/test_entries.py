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
from models import *

def tear():
    #reverts the changes made in the database -gets called in tearDown()
    DBNAME = os.getenv('DBNAME')
    DBPWD = os.getenv('DBPWD')
    DBUSER = os.getenv('DBUSER')
    connection = psycopg2.connect(dbname=DBNAME, user=DBUSER, \
    host='localhost', password=DBPWD, port="5432")
    cursor = connection.cursor()
    cursor.execute("delete from users where username = 'test';")
    cursor.execute("delete from entries where title = 'test' and entry = 'successful';")
    connection.commit()

data = {"fname": "kibish",\
        "username":"test", \
        "password":"kev12345",\
        "lname":"kipkoech",\
        "cpassword":"kev12345",\
        "email":"tests@gmail.com"\
        }

class TestCreateEntry(unittest.TestCase):
    def setUp(self):
        #creates table and test user
        DatabaseModel.create_table()
        self.APP = APP.test_client()
        self.APP.post('/api/v2/users/register', json=data)       
 
    def test_post(self):
        #test return status code for no provided token
        res = self.APP.post('/api/v2/users/login', json={"username":"test", "password":"kev12345"})
        token = res.get_json()["token"]
        response = self.APP.post('/api/v2/entries', headers = {"x-access-token":token},\
        json={"title":"test", "entry":"successful"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "entry was successfully saved")

    def test_get(self):
        #test message when no token provided
        res = self.APP.post('/api/v2/users/login', json={"username":"test", "password":"kev12345"})
        token = res.get_json()["token"]
        response = self.APP.get('/api/v2/entries')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "you are out of session")
        response2 = self.APP.get('/api/v2/entries', headers = {"x-access-token":token})
        self.assertEqual(response2.status_code, 200)

    def tearDown(self):
        tear()

class TestEntryId(unittest.TestCase):
    def setUp(self):
        self.APP = APP.test_client()
        self.APP.post('/api/v2/users/register', json=data)   

    def test_put(self):
        #test wrong method modification
        res = self.APP.post('/api/v2/users/login', json={"username":"test", "password":"kev12345"})
        token = res.get_json()["token"]        
        modify = self.APP.post\
        ('/api/v2/entries/3', json={"title":"test","entry":"successful" }).status_code
        self.assertEqual(modify, 405)
        response = self.APP.post\
        ('/api/v2/entries/3', json={"title":""}, headers = {"x-access-token":token}).status_code
        self.assertEqual(modify, 405)

    def test_delete(self):
        #test wrong entry route and method
        res = self.APP.get('/api/v2/entries/delete_entry').status_code
        self.assertEqual(res, 404)
        response = self.APP.delete('/api/v2/entries/3')
        self.assertEqual(response.get_json()["message"], "you are out of session")

    def test_get(self):
        #test succesful response
        res = self.APP.post('/api/v2/users/login', json={"username":"test", "password":"kev12345"})
        token = res.get_json()["token"]
        self.assertEqual(self.APP.get('/api/v2/entries/8').get_json()["message"], "you are out of session")
        response = self.APP.get('/api/v2/entries/8p', headers = {"x-access-token":token})
        self.assertEqual(response.status_code, 404)
            
    def tearDown(self):
        tear()

if __name__ == '__main__':
    unittest.main()
