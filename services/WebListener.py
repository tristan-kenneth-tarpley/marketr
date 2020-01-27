# scraping libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import asyncio
import requests
import pandas as pd
import hashlib
import urllib
import hmac
from pprint import pprint
from xml.etree import ElementTree
import praw

class Listener:
    def __init__(self, keyword):
        
        self.keyword = keyword

    def listen(self):
        reddit = praw.Reddit(client_id='oy-mmNuzOc9-vA',
                     client_secret='iYEjlEIHrL4rv5ikxfACQn8cSEg', password='uVF32x*PxMf3yL8ooYvx',
                     user_agent='marketr', username='marketr_life')
        returned = list()
        for submission in reddit.subreddit('all').search(self.keyword):
            returned.append({
                'title': submission.title,
                'url': submission.url,
                'created_at': submission.created_utc
            })
        
        return returned[:10]