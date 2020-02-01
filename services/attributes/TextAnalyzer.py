from app import app
import urllib
import time
#AI imports
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput

import requests

class TextAnalyzer:
    def __init__(self, scraper):
        self.scraper = scraper
        app.config.from_pyfile('config.cfg')
        self.NLP_AUTH = IAMAuthenticator(app.config['NLP_AUTH'])
        self.TONE_AUTH = IAMAuthenticator(app.config['TONE_AUTH'])
        
    def tone_analyzer(self, text):
      
        service = ToneAnalyzerV3(
            version='2017-09-21',
            authenticator=self.TONE_AUTH)
        tone_input = ToneInput(text)
        tone = service.tone(tone_input=tone_input, content_type="application/json").get_result()
        
        tones = {}
        for tone in tone['document_tone']['tones']:
            if tone['tone_name'] not in tones:
                tones[tone['tone_name']] = {
                    'score': []
                }
                
            tones[tone['tone_name']]['score'].append(tone['score'])
            
        
        return tones
    
    def key_phrases(self, text):
        text_subscription_key = '45f31e1a295e414b8d71319b79a405e0'
        text_analytics_base_url = "https://southcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
        key_phrase_api_url = text_analytics_base_url + "keyPhrases"
        text_doc = {'documents' : [
            { 'id': '1', 'language': 'en', 'text': text },
        ]}

        key_phrases_headers   = {"Ocp-Apim-Subscription-Key": text_subscription_key}
        key_phrases_response  = requests.post(key_phrase_api_url, headers=key_phrases_headers, json=text_doc)
        key_phrases = key_phrases_response.json()

        return key_phrases
    
    def nlp_understanding(self, text=None, url=None):
        service = NaturalLanguageUnderstandingV1(
            version='2018-03-16',
            authenticator=self.NLP_AUTH)
        
        service.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

        if url:
            response = service.analyze(
                url=url,
                features=Features(entities=EntitiesOptions(),
                                  keywords=KeywordsOptions())).get_result()
        elif text:
            response = service.analyze(
                text=text,
                features=Features(entities=EntitiesOptions(),
                                  keywords=KeywordsOptions())).get_result()

        return response 
    
    def headline_analyzer(self, headline):
        headline_enc = f"headline={headline}"
        querystring = urllib.parse.quote(headline_enc)
        url = f'https://headlines.sharethrough.com/?headline={querystring}' 
        
        driver = self.scraper
        
        try:
            dom = driver.get(url=url)
            
            time.sleep(2)

            titles = dom.select('.suggestion-title')
            descriptions = dom.select('.suggestion-description')
            score = dom.select('.overall .score')
            print(score)
            struct = {
                'score': score,
                'recommendations': []
            }

            for i in range(len(titles)):
                new = {
                    'title': titles[i].text,
                    'description': descriptions[i].text.replace(', discovered by Sharethrough,', '')
                }
                struct['recommendations'].append(new)
            
            return struct
        
        except AssertionError:
            # print(e)
            return None