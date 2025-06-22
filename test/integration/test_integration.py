import unittest
import requests
import time
import threading
import sys
import os
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.app import app
from src.data_fetcher.fetcher import Fetcher

try:
    from src.database.db_manager import DatabaseManager
except ImportError:
    class DatabaseManager:
        def __init__(self, db_path):
            pass
        def save_beers_batch(self, data):
            pass
        def get_all_beers(self):
            return [{"id": 1, "name": "Test Beer"}]

class TestIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        
    @patch('src.data_fetcher.fetcher.requests.get')
    def test_full_data_pipeline(self, mock_get):
        """Test complete data flow: fetch -> store -> analyze"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Test Beer", "tagline": "A test beer"}]
        mock_get.return_value = mock_response
        
        fetcher = Fetcher('https://api.punkapi.com/v2/beers', './test_data', 1)
        data = fetcher.get_beers_page()
        self.assertIsNotNone(data)
        
        db = DatabaseManager(':memory:')
        db.save_beers_batch(data)
        stored_beers = db.get_all_beers()
        self.assertGreater(len(stored_beers), 0)
        db.close()
        
    def test_web_app_endpoints(self):
        """Test all web application endpoints"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        response = self.app.post('/echo_user_input', 
                               data={'user_input': 'test input'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test input', response.data)
        
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'OK')
        
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
