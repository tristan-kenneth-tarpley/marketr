
# coding: utf-8

# In[288]:

from app import app
import requests
import pandas as pd
from collections import Counter
import spacy
import en_core_web_sm as English
import nlglib
import markovify



# In[289]:


class MarketResearch:
    def __init__(self):
        app.config.from_pyfile('config.cfg')
        self.spyfu = app.config['SPYFU']
#         self.spyfu = 'UV9UVYUQ'
    
    def related_keywords(self, csv=None):
        url = f'https://www.spyfu.com/apis/kss_api/kss_kws?q={csv}&r=40&api_key={self.spyfu}'
        res = pd.DataFrame(requests.get(url).json())
        response = res.filter(['keyword', 'advertisers','broad_cpc','phrase_cpc', 'exact_cpc', 'costperday'], axis=1)
        response['keyword'] = response['keyword'].apply(lambda x: x.replace('%20', ' '))
        return response
    
    def ad_history(self, term):
        url = f"https://www.spyfu.com/apis/ad_history_api/term_ad_history_json?t={term}&api_key={self.spyfu}"
        print(url)
        res = pd.DataFrame(requests.get(url).json())
        return res


# In[316]:


class AdGrouper:
    def __init__(self, market_obj, keywords:list):
        self.market = market_obj
        self.args = keywords
        self.csv = ", ".join(keywords)
        
    def nlp(self):
        return English.load()
    
    def common(self, keywords):
        counts = dict()
        words = " ".join(keywords).split(" ")

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
                
        return pd.Series(counts).to_frame('count').reset_index(level=0).rename(columns={"index": "word"})
    
    def filter_common(self):
        related = self.market.related_keywords(csv=self.csv)
        common = self.common(related['keyword'])
        
        nlp = self.nlp()
        tokens = nlp(" ".join(list(common['word'])))
        
        tokenized = list()
        for token in tokens:
            tokenized.append({
                'word': token.lemma_,
                'part_of_speech': token.pos_,
                'dependency': token.dep_,
                'head': token.head
            })


        tokenized_df = pd.DataFrame(tokenized)
        common = common.merge(tokenized_df, on='word').sort_values(by=['count'], ascending=False)
        common = common[(common['count'] > common['count'].sum()*.02) & (common['part_of_speech'] != 'ADP')]
        common['prominent'] = common['count'].apply(lambda x: x > common['count'].sum()*.3)
        removed_words = ['for', 'in', 'the', 'of']
        common['head'] = common['head'].apply(lambda x: x if str(x) not in removed_words else common['word'].iloc[0])
        common['head'] = common['head'].apply(lambda x: nlp(str(x))[0].lemma_)
        
        return common
        
    def group(self):
        df = self.filter_common()
        return [f"{key[1]} {list(df['head'])[key[0]]}" for key in enumerate(list(df['word']))]
    
    def full_groups(self):
        groups = self.group()
        
        returned = list()
        for group in groups:
            returned.append({
                'group': group,
                'keywords': self.market.related_keywords(group).to_dict('records')
                }
            )
        
        return returned


# # Ad generation

# In[374]:


class CopyWriter():
    def __init__(self):
        pass
        
    def Google(self, history):
        headlines = markovify.NewlineText(history.title, state_size = 2)
        body_copy = markovify.NewlineText(history.body, state_size = 2)

        if headlines and body_copy:
            ads = list()
            i=0
            while i < 20:
                ad_headline = headlines.make_sentence()
                ad_body = body_copy.make_sentence()
                if ad_headline and ad_body:
                    ads.append({
                        'headline': ad_headline,
                        'body': ad_body
                    })
                i += 1

        return ads if ads else None

