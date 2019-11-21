
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from collections import Counter
import spacy
import en_core_web_sm as English


# In[2]:


class KeywordService:
    def __init__(self, *args):
#         app.config.from_pyfile('config.cfg')
#         self.spyfu = app.config['SPYFU']
        self.spyfu = 'UV9UVYUQ'
        self.csv = ", ".join([arg for arg in args])
    
    def get(self, url):
        return pd.DataFrame(requests.get(url).json())

    def related_keywords(self):
        url = f'https://www.spyfu.com/apis/kss_api/kss_kws?q={self.csv}&r=40&api_key={self.spyfu}'
        res = self.get(url)
        
        response = res.filter(['keyword', 'advertisers','broad_cpc','phrase_cpc', 'exact_cpc', 'costperday'], axis=1)
        response['keyword'] = response['keyword'].apply(lambda x: x.replace('%20', ' '))
        return response


# In[3]:


class AdGrouper:
    def __init__(self, keywords):
        self.keywords = keywords
        
    def common(self):
        counts = dict()
        words = " ".join(self.keywords).split(" ")

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        print(counts)


# In[4]:


# keywords = KeywordService("hr software", "benefits software", "employee management software", "online employee management", "online hr management")
# related = keywords.related_keywords()


# In[5]:


# grouper = AdGrouper(list(related['keyword']))
# grouper.common()


# In[6]:


# nlp = English.load()
# tokens = nlp("hr software human resources")
# for token in tokens:
#     print(" {:<8} : {:<5} : {:<7} : {}".format(token.orth_,token.pos_,token.dep_,token.head))
    
# print(" {:<8} : {:<5} : {:<7} : {}".format("token","POS","dep.","head"))

