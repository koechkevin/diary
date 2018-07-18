import unittest
import json
from myClass import ExternalFunctions
from myDiary_dataStructures import *
#from flask import *
from myClass import ExternalFunctions
class Test_ExternalFunctions(unittest.TestCase):
    def test_home(self):
        with app.test_client() as test:
            response = test.get('/api/v1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(test.post('/api/v1',json={}).status_code,405)
    def test_passwordVerify(self):
        self.assertTrue(ExternalFunctions.passwordVerify("kevin","kevin"),True)
        self.assertFalse(ExternalFunctions.passwordVerify("kevin","kevins"),False)
    def test_register(self):
        t= app.test_client()
        response = t.get('/api/v1/register')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(t.post('/api/v1/register',json={\
            "fname":"kevin","lname":"koech","email":"kkkoech",\
        "username":"kibitok","password":"1234","cpassword":\
        "1234"}).status_code,200)
    def test_login(self):
        with app.test_client() as tester:
            response = tester.get('/api/v1/login')
            self.assertEqual(response.status_code, 405)
            self.assertEqual(tester.post('/api/v1/login',json={\
            "username":"kibitok","password":"1234"}).status_code,200) 
            
    def test_entries(self):
        with app.test_client() as tester:
            response = tester.get('/api/v1/entries')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(tester.post('/api/v1/entries',json={}).status_code,405)
            self.assertEqual(tester.get('/api/v1/entry').status_code,404)
            
    def test_logout(self):
        with app.test_client() as tester:
            response = tester.get('/api/v1/logout')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(tester.post('/api/v1/entries',json={}).status_code,405)
    def test_delete_entry(self):
        response = app.test_client().get('/api/v1/delete_entry/3')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(app.test_client().post('/api/v1/delete_entry/3',json={}).status_code,405)
    def test_create_entry(self):
        with app.test_client() as test:
            response = test.get('/api/v1/create_entry')
            self.assertEqual(response.status_code, 405) 
    def test_modify_entry(self):
        with app.test_client() as tester:
            response = tester.get('/api/v1/modify_entry/1')
            self.assertEqual(response.status_code, 405)  
    def test_view_entry(self):
        tester= app.test_client()
        response = tester.get('/api/v1/view_entry/1')
        self.assertEqual(response.status_code, 200) 
        
if __name__=='__main__':
        unittest.main()
        
     