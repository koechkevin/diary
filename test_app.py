import unittest
from app import *
class Test_app(unittest.TestCase):
    def test_authorize(self):
        self.assertTrue(authorize('dfghjjertyui.rffdd.eeas'),True)
    def test_validEmail(self):
        self.assertTrue(validEmail('koechkevin@gmail.com'),True)
        self.assertFalse(validEmail('koechkevingmail@.com'),False)
    def test_home(self):
        test = app.test_client()
        response = test.get('/')
        response2 = test.get('/api/v2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)
    def test_register(self):  
        self.assertEqual\
            (app.test_client().get('/api/v2/register').status_code,405)
        self.assertEqual(app.test_client().post('/api/v2/register',json={\
            "fname":"kevin","lname":"koech","email":"kkkoech",\
        "username":"kibitok","password":"1234","cpassword":\
        "1234"}).status_code,409)
        t=app.test_client()
        res=t.post('/api/v2/register',json={"fname":"kevin",\
        "lname":"koech","email":"kkkoech","username":"kibitoks",\
        "password":"1234","cpassword":"1234"})
        self.assertEqual(res.status_code,403)
    def test_login(self):
        tester=app.test_client()
        response=tester.post('/api/v2/login',json={"username":"kiprop","password":"1234"})
        self.assertEqual(response.status_code,401)
    def test_post_entry(self):
        with app.test_client() as test:
            response=test.post('/api/v2/create_entry?token=',json={"title":"kevins first","entry":"its awesome"})
            self.assertEqual(response.status_code,401)
            self.assertEqual(test.get('/api/v2/create_entry?token=').status_code,405)
            
if __name__=='__main__':
    unittest.main()