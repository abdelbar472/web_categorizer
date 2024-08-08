import unittest
from main import *
from models import *

class TestResources(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_space_resource(self):
        # Test POST method
        response = self.app.post('/space', data=dict(space_name='Test Space', space_description='This is a test space'))
        self.assertEqual(response.status_code, 200)

        # Test GET method
        response = self.app.get('/space/Test Space')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Space', response.data)

    def test_category_resource(self):
        # Test POST method
        response = self.app.post('/space/Test Space/category', data=dict(category_name='Test Category'))
        self.assertEqual(response.status_code, 200)

        # Test GET method
        response = self.app.get('/space/Test Space/category')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Category', response.data)

    def test_subcategory_resource(self):
        # Test POST method
        response = self.app.post('/space/Test Space/category/Test Category/subcategory', data=dict(subcategory_name='Test Subcategory'))
        self.assertEqual(response.status_code, 200)

        # Test GET method
        response = self.app.get('/space/Test Space/category/Test Category/subcategory')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Subcategory', response.data)

if __name__ == "__main__":
    unittest.main()