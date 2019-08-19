import requests
from app import app
class CompetitorService:
    def __init__(self):
        self.init = True
        app.config.from_pyfile('config.cfg')
        self.spyfu = app.config['SPYFU']

    def intro(self, url):
        history_url = f'https://www.spyfu.com/apis/ad_history_api/domain_ad_history_json?d={url}&r=10&s=0&isUs=true&api_key={self.spyfu}'
        history = requests.get(history_url).json()
        core_url = f'https://www.spyfu.com/apis/core_api/get_domain_metrics_us?domain={url}&api_key={self.spyfu}'
        core = requests.get(core_url).json()
        url_url = f'https://www.spyfu.com/apis/url_api/paid_kws?q={url}&r=10&api_key={self.spyfu}'
        url = requests.get(url_url).json()

        ads = []
        for ad in history:
            struct = {
                'title': ad['title'],
                'body': ad['body'],
                'url': ad['url']
            }
            ads.append(struct)

        keywords = []
        for item in url:
            keywords.append(item['term'])

        struct = {
            'budget': core['monthly_adwords_budget'],
            'top_keywords': keywords,
            'clicks': core['paid_clicks_per_month'],
            'ads': ads
        }
        return struct