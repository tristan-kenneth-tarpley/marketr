import requests
from app import app

class Blog:
    def __init__(self):
        self.endpoint = "https://api.storyblok.com/v1/cdn/stories"
        app.config.from_pyfile('config.cfg')
        self.key = app.config['BLOG']

    def single_story(self, slug):
        url = f"{self.endpoint}/posts/{slug}"
        querystring = {"token":self.key, "version": "published"}
        return self.fetch(url, querystring)

    def all_stories(self):
        url = self.endpoint
        querystring = {"token":self.key, "starts_with":"posts/","cv": 1}
        return self.fetch(url, querystring)

    def fetch(self, url, querystring):
        payload = ""
        headers = {}
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        return response.json()

