import unittest
import json
import json
import os,sys
sys.path.insert(0, os.path.abspath(".."))
from entries import *
from __init__ import *

class TestEntries(unittest.TestCase):
    def test_post_entry(self):
        with app.test_client() as test:
            response = test.post('/api/v2/entries/create_entry?token=', json={"title":"kevins first", "entry":"its awesome"})
            self.assertEqual(response.status_code, 401)
            self.assertEqual(test.get('/api/v2/entries/create_entry?token=').status_code, 405)
    def test_entries(self):
        t = app.test_client()
        r = t.get('/api/v2/entries')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(t.post('/api/v2/entries').status_code, 405)
   
    def test_delete_entry(self):
        with app.test_client() as test:
            r = test.get('/api/v2/entries/delete_entry').status_code
            self.assertEqual(r, 404)
    def test_modify_entry(self):
        modify = app.test_client().post('/api/v2/entries/modify_entry/3', json={"tittle":" "}).status_code
        self.assertEqual(modify, 405)
    def test_view_entry(self):
        te = app.test_client().get('/api/v2/entries/view_entry/8').status_code
        self.assertEqual(te, 401) 
        response = app.test_client().get('/api/v2/view_entry/8')
        #self.assertEqual(json.loads(response.get_data(as_text=True)), "you are out of session")
            
            
            
if __name__ == '__main__':
    unittest.main()    