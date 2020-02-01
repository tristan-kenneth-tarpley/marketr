from app import app
from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, url=None, measure=False):
        app.config.from_pyfile('config.cfg')
        self.key = app.config['SCRAPER_KEY']
        if 'https://' or 'http://' not in url:
            self.url = f'https://{url}'
        else:
            self.url = url

        self.measure = measure

    def get(self, url=None):
        payload = {
            'api_key': self.key,
            'url': self.url if not url else url,
            'render': 'true'
        }

        r = requests.get('http://api.scraperapi.com', params=payload)
        if self.measure:
            self.load_time = r.elapsed.total_seconds()
        

        soup = BeautifulSoup(r.text, 'html.parser')
        return soup