import unittest

from __init__ import *


class TestUsers(unittest.TestCase):
    def test_authorize(self):
        self.assertTrue(Users.authorize('dfghjjertyui.rffdd.eeas'), True)
       
    def test_valid_email(self):
        self.assertTrue(Users.valid_email('koechkevin@gmail.com'), True)
        self.assertFalse(Users.valid_email('koechkevingmail@.com'), False)
        
    def test_register(self):  
        self.assertEqual\
            (app.test_client().get('/api/v2/users/register').status_code, 405)
        self.assertEqual(app.test_client().post('/api/v2/register', json={\
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