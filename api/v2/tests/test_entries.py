"""
test entries
"""
import unittest

import os
import sys

from __init__ import APP

sys.path.insert(0, os.path.abspath(".."))

class TestCreateEntry(unittest.TestCase):
    """
test entries
"""
    def test_post(self):
        """
test return status code for no provided token
"""
        with APP.test_client() as test:
            response = test.post('/api/v2/entries', \
            json={"tittle":"", "entry":""})
            self.assertEqual(response.status_code, 200)
    def test_get(self):
        """
test return ok for no token provided
"""
        with APP.test_client() as test:
            response = test.get('/api/v2/entries?t')
            self.assertEqual(response.status_code, 200)
class TestEntryId(unittest.TestCase):
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
