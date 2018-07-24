import unittest
import json

from app import authorize, valid_email, register, login, account, post_entry, entries, view_entry, delete_entry, modify_entry, app

class Test_app(unittest.TestCase):
    def test_authorize(self):
        self.assertTrue(authorize('dfghjjertyui.rffdd.eeas'), True)
    def test_valid_email(self):
        self.assertTrue(valid_email('koechkevin@gmail.com'), True)
        self.assertFalse(valid_email('koechkevingmail@.com'), False)
    def test_home(self):
        test = app.test_client()
        response = test.get('/')
        response2 = test.get('/api/v2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), 'welcome to my diary')
    def test_register(self):  
        self.assertEqual\
            (app.test_client().get('/api/v2/register').status_code, 405)
        self.assertEqual(app.test_client().post('/api/v2/register', json={\
            "fname":"kevin", "lname":"koech", "email":"kkkoech",\
        "username":"kibitok", "password":"1234", "cpassword":\
        "1234"}).status_code, 409)
        t = app.test_client()
        res = t.post('/api/v2/register', json={"fname":"kevin",\
        "lname":"koech", "email":"kkkoech", "username":"kibitoks",\
        "password":"1234", "cpassword":"1234"})
        self.assertEqual(json.loads(res.get_data(as_text=True)), 'please enter a valid email')
        self.assertEqual(res.status_code, 403)
    def test_login(self):
        tester = app.test_client()
        response = tester.post('/api/v2/login', json={"username":"kiprop", "password":"1234"})
        self.assertEqual(response.status_code, 401)
    def test_post_entry(self):
        with app.test_client() as test:
            response = test.post('/api/v2/create_entry?token=', json={"title":"kevins first", "entry":"its awesome"})
            self.assertEqual(response.status_code, 401)
            self.assertEqual(test.get('/api/v2/create_entry?token=').status_code, 405)
    def test_entries(self):
        t = app.test_client()
        r = t.get('/api/v2/entries')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(t.post('/api/v2/entries').status_code, 405)
    def test_logout(self):
        t = app.test_client().get('/api/v2/logout').status_code
        self.assertEqual(t, 422)
        te = app.test_client().get('/api/v2/logou').status_code
        self.assertEqual(te, 404)
    def test_delete_entry(self):
        with app.test_client() as test:
            r = test.get('/api/v2/delete_entry').status_code
            self.assertEqual(r, 404)
    def test_modify_entry(self):
        modify = app.test_client().post('/api/v2/modify_entry/3', json={}).status_code
        self.assertEqual(modify, 405)
    def test_view_entry(self):
        te = app.test_client().get('/api/v2/view_entry/8').status_code
        self.assertEqual(te, 401) 
        response = app.test_client().get('/api/v2/view_entry/8')
        self.assertEqual(json.loads(response.get_data(as_text=True)), "you are out of session")
            
            
            
if __name__ == '__main__':
    unittest.main()