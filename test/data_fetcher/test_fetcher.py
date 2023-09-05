import unittest
from src.data_fetcher.fetcher import Fetcher


class TestFetcher(unittest.TestCase, Fetcher):

    @classmethod
    def setUpClass(cls):
        data_url = 'https://api.punkapi.com/v2/beers'
        data_dir = './test_rawdata'
        page_number = 1
        cls.fetcher = Fetcher(data_url, data_dir, page_number)

    def test_getter(self):
        data = self.fetcher.get_beers_page()
        self.assertIsNotNone(data)

    def test_save(self):
        data = self.fetcher.get_beers_page()
        self.fetcher.save_to_file(data)
        self.assertIsNotNone(data)


if __name__ == "__main__":
    unittest.main()
