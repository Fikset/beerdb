import unittest
from unittest.mock import Mock, patch, MagicMock
from src.data_fetcher.fetcher import Fetcher
from src.database.db_manager import DatabaseManager

class TestWithMocks(unittest.TestCase):
    
    @patch('src.data_fetcher.fetcher.requests.get')
    def test_fetcher_with_mock(self, mock_get):
        """Test fetcher with mocked HTTP requests"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Test Beer', 'abv': 5.0}
        ]
        mock_get.return_value = mock_response
        
        fetcher = Fetcher('http://test-api.com', './test_data', 1)
        data = fetcher.get_beers_page()
        
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Beer')
        mock_get.assert_called_once()
    
    @patch('src.database.db_manager.sqlite3.connect')
    def test_database_with_mock(self, mock_connect):
        """Test database operations with mocked SQLite"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        db = DatabaseManager('test.db')
        db.save_beer({'id': 1, 'name': 'Mock Beer'})
        
        self.assertTrue(mock_connect.called)
        self.assertTrue(mock_conn.__enter__.return_value.execute.called)
        self.assertTrue(mock_conn.__enter__.return_value.commit.called)
    
    @patch('src.data_fetcher.fetcher.os.path.join')
    @patch('builtins.open')
    def test_save_to_file_with_mock(self, mock_open, mock_join):
        """Test file saving with mocked file operations"""
        mock_join.return_value = '/fake/path/test.json'
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        fetcher = Fetcher('http://test.com', './test_data', 1)
        test_data = [{'id': 1, 'name': 'Test'}]
        fetcher.save_to_file(test_data)
        
        mock_open.assert_called_once()
        mock_file.write.assert_called()

if __name__ == '__main__':
    unittest.main()
