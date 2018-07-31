import unittest
import json

import os,sys
sys.path.insert(0, os.path.abspath(".."))
#from entries import *
from __init__ import *

class TestCreateEntry(unittest.TestCase):
    def test_post(self):
        with app.test_client() as test:
            response = test.post('/api/v2/entries', json={})
            self.assertEqual(response.status_code, 200)
            
    def test_get(self):
        with app.test_client() as test:
            response = test.get('/api/v2/entries?token= ')
            self.assertEqual(response.status_code, 200)
     
class TestEntryId(unittest.TestCase):
    def test_put(self):
        modify = app.test_client().post\
        ('/api/v2/entries/3', json={"tittle":" "}).status_code
        self.assertEqual(modify, 405)
        
    def test_delete(self):
        with app.test_client() as test:
            r = test.get('/api/v2/entries/delete_entry').status_code
            self.assertEqual(r, 404)    
            response = test.delete('/api/v2/entries/3')
            self.assertEqual(response.status_code, 200)
            
    def test_get(self):
        test = app.test_client()
        self.assertEqual(test.get('/api/v2/entries/8').status_code, 200)        
    
    
            
            
if __name__ == '__main__':
    unittest.main()    