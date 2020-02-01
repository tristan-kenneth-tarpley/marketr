import data.db as db
# core imports
import urllib.request
import time
import requests
import pyodbc
import json
import pprint
import urllib
from services.attributes.TextAnalyzer import TextAnalyzer
from services.CompetitorService import CompetitorService
from services.Scraper import Scraper
#data science shtuff
import pandas as pd

# scraping libraries
from bs4 import BeautifulSoup


from random import choices



class SiteObj:
    def __init__(self, url=None, driver=None):
        self.url = url
        self.driver = driver
        self.site_string = ""
        self.struct = {
            'h1': [],
            'h2': [],
            'h3': [],
            'h4': [],
            'h5': [],
            'h6': [],
            'p': [],
            'button': []
        }

        self.concatenated_struct = {
            'h1': "", 'h2': "", 'h3': "", 'h4': "", 'h5': "", 'h6': "", 'p': "", 'button': ""
        } 
        
        
    def append_to_struct(self, key, array):
        for x in array:
            if len(x.text) > 0:
                self.struct[key].append(x.text)
                self.concatenated_struct[key] += (" " + x.text)

    def get_site_copy(self):
        for k, v in self.struct.items():
            self.append_to_struct(k, self.driver.find_all(k))

        for key, v in self.struct.items():
            for x in v:
                self.site_string += (" " + x)

        print(self.site_string)




class ColdAudit:
    def __init__(self, TextAnalyzer=None, competitors=None, scraper=None, url=None, run_competitors=True, requested=False):
        self.competitors = competitors
        self.scraper = scraper
        self.url = url 
        self.run_competitors = run_competitors
        self.requested = requested
        self.TextAnalyzer = TextAnalyzer
        
    def analyze_load_time(self):
        if self.load_time <= 1:
            improvement_headline = "Wow! Much fast. Very wow."
            improvement_copy = "Your site's load time is best in class. This can help website conversions by more than 123%! Make sure to keep an eye on this and figure out what other meat you can add to your website to further increase it."
            
        elif self.load_time > 1 <= 3:
            improvement_headline = "Consider me impressed!"
            improvement_copy = "The recommended site load time is less than 3 seconds... And guess what... You passed! If you wanted to really go Superman mode, try to get it under 1 second for a 21% reduction in bounce rate."
            
        elif self.load_time > 3 <= 5:
            improvement_headline = "The site better be good given how long you made us wait!"
            improvement_copy = "You can decrease the number of users that leave immediately by 32% if your site loaded in less than 3 seconds."
            
        elif self.load_time > 5 <= 6:
            improvement_headline = "The site better be good given how long you made us wait!"
            improvement_copy = "You can decrease the number of users that leave immediately by 90% if your site loaded in less than 5 seconds."
            
        elif self.load_time > 6 <= 10:
            improvement_headline = "Ah! The anticipation was KILLING me."
            improvement_copy = "You can decrease the number of users that leave immediately by 106% if your site loaded in less than 6 seconds."
            
        elif self.load_time > 10:
            improvement_headline = "Hold on, we're still waiting on... Oh wait. It just loaded."
            improvement_copy = "You can decrease the number of users that leave immediately by 123% if your site loaded in less than 10 seconds."
        
        analysis_struct = {
            'load_time': self.load_time,
            'improvement_headline': improvement_headline,
            'improvement_copy': improvement_copy
        }
        self.load_time = analysis_struct

        
    def get(self):   
        def site_data(scraper=self.scraper, url=self.url):
        
            driver = scraper.get(render=True)
            siteobj = SiteObj(url=url, driver=driver)
            load_time = scraper.load_time
            
            siteobj.get_site_copy()
            headlines = siteobj.struct['h1'] + siteobj.struct['h2'] + siteobj.struct['h3']
            for headline in headlines:
                headline.replace('\n', ' ')
            
            text_analyzer = self.TextAnalyzer
    
            assert siteobj.site_string is not None, "Site string wasn't populated"
      
            scent = text_analyzer.tone_analyzer(siteobj.site_string)
            
            return headlines, load_time, scent
        
        def get_ad_data(url=self.url):
            ads = self.competitors.GoogleAds(url)
            keywords = self.competitors.paid_kw(url)
            competitors = self.competitors.NewCompetitors(url)
            
            return ads, keywords, competitors
    
        self.headlines, self.load_time, self.scent = site_data()
        self.ads, self.keywords, self.competitors = get_ad_data()
        
    def analyze(self):
        self.get()
        self.analyze_load_time()
        
        ad_analysis = []
        text_analyzer = self.TextAnalyzer
        if self.ads:
            for i in range(len(self.ads)):
                if i < 3:
                    struct = text_analyzer.headline_analyzer(self.ads[i]['title'] + self.ads[i]['body'])
                    struct_w_ad = {
                        'ad_headline': self.ads[i]['title'],
                        'ad_body': self.ads[i]['body'],
                        'analysis': struct
                    }
                    ad_analysis.append(struct_w_ad)
        else:
            for i in range(len(self.headlines)):
                if i < 3:
                    struct = text_analyzer.headline_analyzer(self.headlines[i])
                    struct_w_ad = {
                        'headline': self.headlines[i],
                        'analysis': struct
                    }
                    ad_analysis.append(struct_w_ad)
                
                
        self.ad_analysis = ad_analysis
                
    def run(self):
        self.analyze()
        self.data = {
            'url': self.url.replace('https://', ''),
            'load_time': self.load_time,
            'scent': self.scent,
            'headlines': self.headlines,
            'keywords': self.keywords,
            'ads': self.ads,
            'competitors': self.competitors,
            'ad_analysis': self.ad_analysis
        }
            
        
    def save(self):
        query = "EXEC save_audit @audit_string = ?, @url = ?, @requested = ?"
        
        if self.requested == True:
            requested = 1
        else: 
            requested = 0
            
        db.execute(query, False, (json.dumps(self.data), self.url.replace('https://', ''), requested), commit=True)





class AuditService:
    def __init__(self, url=None):
        self.url = url

    def get(self):
        query = """SELECT
            audit_string,
            (select audit_string from audit_results WHERE url = ar.comp_1) as comp_1,
            (select audit_string from audit_results WHERE url = ar.comp_2) as comp_2,
            (select audit_string from audit_results WHERE url = ar.comp_3) as comp_3,
            (select top 3 title, description from join_tactics where tag_val like '%any%' ORDER BY NEWID() for json path, root('tactics'))
            as tactics

            FROM audit_results as ar WHERE url = ?
        """
        results, cursor = db.execute(query, True, (self.url,))
        results = cursor.fetchone()
        page = eval(results[0])
        if results[1]:
            competitors = [eval(results[1]), eval(results[2]), eval(results[3])]
        else:
            competitors = None
        tactics = eval(results[4])

        return page, competitors, tactics




### compile

def run_audit(url=None, requested=True):
    url = url.replace('www.', '')
    url = url[:-1] if url[-1] == '/' else url
    print(url)

    competitors = CompetitorService(None)
    scraper = Scraper(url=url, measure=True)
    text_analyzer = TextAnalyzer(scraper)

    audit = ColdAudit(
        url=url,
        TextAnalyzer=text_analyzer,
        run_competitors=True,
        requested=True,
        competitors=competitors,
        scraper=scraper
    )
    
    audit.run()
    audit.save()
    
    base_url = url.replace('https://', '').replace('http://', '')
    completed_comps = []
    for count, competitor in enumerate(audit.competitors):
        if competitor['domainName'].replace('www.', '') != base_url and count < 4:
            try:
                url = competitor['domainName']
               
                scraper = Scraper(url=url, measure=True)
                text_analyzer = TextAnalyzer(scraper)
                audit = ColdAudit(
                    url=url,
                    TextAnalyzer=text_analyzer,
                    run_competitors=False,
                    requested=False,
                    competitors=competitors,
                    scraper=scraper
                )

                audit.run()
                audit.save()
                completed_comps.append(competitor['domainName'])

                query = f"UPDATE audit_results SET comp_{count} = '{competitor['domainName']}' WHERE url = '{url}'"
                db.execute(query, False, (), commit=True)

            except AssertionError:
                continue
            
    if len(completed_comps) > 1:       
        for competitor in completed_comps:
            comps_not_current = []
            for comp_temp in completed_comps:
                if comp_temp != competitor:
                    comps_not_current.append(comp_temp)

            query = f"UPDATE audit_results SET comp_1 = ?, comp_2 = ?, comp_3 = ?, comp_4 = ?, comp_5 = ? WHERE url = '{competitor}'"
            
            if len(comps_not_current) == 5:
                tup = (comps_not_current[0], comps_not_current[1], comps_not_current[2], comps_not_current[3], comps_not_current[4])
                db.execute(query, False, tup, commit=True)
                
            elif len(comps_not_current) == 4: 
                tup = (comps_not_current[0], comps_not_current[1], comps_not_current[2], comps_not_current[3], None)
                db.execute(query, False, tup, commit=True)
            elif len(comps_not_current) == 3: 
                tup = (comps_not_current[0], comps_not_current[1], comps_not_current[2], None, None)
                db.execute(query, False, tup, commit=True)
            elif len(comps_not_current) == 2:
                tup = (comps_not_current[0], comps_not_current[1], None, None, None)
                db.execute(query, False, tup, commit=True)
            elif len(comps_not_current) == 1:
                tup = (comps_not_current[0], None, None, None, None)
                db.execute(query, False, tup, commit=True)
      