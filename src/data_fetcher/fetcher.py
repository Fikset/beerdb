import requests
import json
import os

DATA_URL = 'https://api.punkapi.com/v2/beers'
DATA_DIR = 'data'
PAGE_BEGIN = 1
PAGE_END = 5


class Fetcher:
    def __init__(self, data_url, data_dir, page_number):
        self.data_url = data_url
        self.data_dir = data_dir
        self.page_number = page_number

    def get_beers_page(self, per_page=80):
        response = requests.get(f"{self.data_url}?page={self.page_number}&per_page={per_page}")
        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            return None
        else:
            return response.json()

    def save_to_file(self, response_result):
        with open(os.path.join(self.data_dir, f'raw_data_page={self.page_number}.json'), 'w', encoding="utf-8") as f:
            json.dump(response_result, f)

    def run(self):
        data = self.get_beers_page()
        self.save_to_file(data)


if __name__ == "__main__":
    for page_number in range(max(1, PAGE_BEGIN), PAGE_END + 1):
        fetcher = Fetcher(DATA_URL, DATA_DIR, page_number)
        fetcher.run()
