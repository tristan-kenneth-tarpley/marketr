import requests
from app import app
import asyncio
import data.db as db
from bs4 import BeautifulSoup



class CompetitorService(object):
    def __init__(self, customer_id):
        self.customer_id = customer_id
        app.config.from_pyfile('config.cfg')
        self.spyfu = app.config['SPYFU']

    def get_all(self):
        query = "SELECT * FROM view_competitors(?)"
        returned, cursor = db.execute(query, True, (self.customer_id,))
        returned = cursor.fetchall()
        empty = list()
        for comp in returned:
            empty.append({
                'comp_id': comp[0],
                'customer_id': comp[1],
                'comp_name': comp[2],
                'comp_website': comp[3],
                'comp_type': comp[4]
            })

        return empty

    def NewCompetitors(self, url):
        url = f'https://www.spyfu.com/apis/core_api/get_domain_competitors_us?domain={url}&isOrganic=true&r=10&api_key={self.spyfu}'
        return requests.get(url).json()

    def paid_kw(self, url):
        url = f'https://www.spyfu.com/apis/url_api/paid_kws?q={url}&r=10&api_key={self.spyfu}'
        return requests.get(url).json()
   
    def SpyfuCore(self, url):
        url = f"https://www.spyfu.com/apis/leads_api/get_contact_card?domain={url}&api_key={self.spyfu}"
        try:
            return requests.get(url).json()
        except:
            return None
    
    def GoogleAds(self, url):
        url = f'https://www.spyfu.com/apis/ad_history_api/domain_ad_history_json?d={url}&r=10&s=0&isUs=true&api_key={self.spyfu}'
        
        return requests.get(url).json()
    
    def DisplayAds(self, url):      
        display_creative_url = f'https://www.adbeat.com/free/profile-search/{url}'
        response = requests.get(display_creative_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ads = list()
        
        ad_parent = soup.find_all('div', 'ad-category')
        for parent in enumerate(ad_parent):
            img = parent[1].find_all('img')[0]['src']
            ads.append(img)
            
        return ads

    def competitor_card(self):
        async def compile(competitors):
            def Struct(name, site, Type, res_1, res_2, res_3, res_4):
                res_3 = res_3[:5] if len(res_3) > 5 else res_3
                keywords = list()
                if res_2:
                    organic = float(res_2.get('seo_clicks')) if res_2.get('seo_clicks') else 0
                    paid = float(res_2.get('ppc_clicks')) if res_2.get('ppc_clicks') else 0
                    budget = float(res_2.get('ppc_budget')) if res_2.get('ppc_budget') else 0
                else:
                    organic = 0
                    paid = 0
                    budget = 0
                for item in res_3:
                    for keyword in item['keywords']:
                        keywords.append(keyword)

                core = {
                    'total_traffic': organic + paid,
                    'ppc_budget': budget,
                    'ppc_clicks': paid,
                    'seo_clicks': organic,
                    'keywords': keywords
                }
                return {
                    'comp_name': name,
                    'site': site,
                    'type': Type,
                    'competitors': res_1,
                    'core': core,
                    'google_ads': res_3[:5] if len(res_3) > 5 else res_3,
                    'display_ads': res_4
                }
            
            returned = list()
            for competitor in competitors:
                website = competitor['comp_website'].replace("http://", "").replace("https://", "").replace("/", "")
                competitors = loop.run_in_executor(None, self.NewCompetitors, website)
                core = loop.run_in_executor(None, self.SpyfuCore, website)
                google_ads = loop.run_in_executor(None, self.GoogleAds, website)
                display_ads = loop.run_in_executor(None, self.DisplayAds, website)

                res_1 = await competitors
                res_2 = await core
                res_3 = await google_ads
                res_4 = await display_ads
                
                struct = Struct(
                    competitor['comp_name'], competitor['comp_website'], competitor['comp_type'],
                    res_1, res_2, res_3, res_4
                )
                returned.append(struct)
                
            return returned

        competitors = self.get_all()
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(compile(competitors))
        
        return results

    