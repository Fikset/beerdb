import unittest
import sys
import os
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data_fetcher.fetcher import Fetcher


class TestFetcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_url = 'https://api.punkapi.com/v2/beers'
        data_dir = './test/data_fetcher/test_rawdata'
        page_number = 1
        cls.fetcher = Fetcher(data_url, data_dir, page_number)

    @patch('src.data_fetcher.fetcher.requests.get')
    def test_getter(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Buzz", "tagline": "A Real Bitter Experience."}]
        mock_get.return_value = mock_response
        
        data = self.fetcher.get_beers_page()
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Buzz")

    @patch('src.data_fetcher.fetcher.requests.get')
    def test_save(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Buzz", "tagline": "A Real Bitter Experience."}]
        mock_get.return_value = mock_response
        
        data = self.fetcher.get_beers_page()
        self.fetcher.save_to_file(data)
        self.assertIsNotNone(data)
        
        import os
        expected_file = os.path.join(self.fetcher.data_dir, f'raw_data_page={self.fetcher.page_number}.json')
        self.assertTrue(os.path.exists(expected_file))


if __name__ == "__main__":
    unittest.main()
