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

class Listener:
    def __init__(self, driver, keyword):
        self.driver = driver
        self.keyword = keyword

    def listen(self):
#         csv = ', '.join([arg for arg in args])
        headline_enc = f"{self.keyword}"
        querystring = urllib.parse.quote(headline_enc)
        reddit_base = f'https://www.reddit.com/search/?q={querystring}'
        
        self.driver.get(reddit_base)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        posts = self.driver.find_elements_by_css_selector('.Post div:nth-of-type(2) h3')
        
        listened = {
            'phrases': [],
            'link': reddit_base
        }
        for post in posts:
            if post.text.strip() != "" and len(post.text.strip()) > 0:
                listened['phrases'].append(post.text)
        
        self.driver.quit()
        
        return listened