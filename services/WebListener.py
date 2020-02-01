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
import random


class Listener:
    def __init__(self, keyword, length=100):
        self.keywords = keyword
        self.length = length

    def listen(self):
        reddit = praw.Reddit(client_id='oy-mmNuzOc9-vA',
                     client_secret='iYEjlEIHrL4rv5ikxfACQn8cSEg', password='uVF32x*PxMf3yL8ooYvx',
                     user_agent='marketr', username='marketr_life')

        async def fetch(keyword):
            response = reddit.subreddit('all').search(keyword)
            returned = list()
            for submission in response:
                if not submission.stickied and submission.is_self:
                    returned.append({
                        'title': submission.title,
                        'url': submission.url,
                        'created_at': submission.created_utc
                    })

            return returned


        async def run():
            returned = list()
            comp_list = list()

            for item in self.keywords:
                for keyword in item.get('keywords'): 
                    task = asyncio.ensure_future(fetch(keyword))
                    returned.append(task)
                
            for comp in self.keywords:
                task = asyncio.ensure_future(fetch(comp.get('comp_name')))
                comp_list.append(task)

            responses = await asyncio.gather(*returned)
            returned = [item for sublist in responses for item in sublist]

            comps = await asyncio.gather(*comp_list)
            comps_ = [item for sublist in random.sample(comps, len(comps)) for item in sublist]
        
            return comps_ + returned
        
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run())
        posts = loop.run_until_complete(future)
 
        return posts[:self.length] if len(posts) > self.length else posts