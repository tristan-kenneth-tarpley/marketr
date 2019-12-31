import pandas as pd
import json
from datetime import date, datetime

class Portfolio:
    def __init__(self, agg=None, google=None, facebook=None):
        self.agg = agg
        self.google_df = google
        self.facebook_df = facebook

    def clean(self, start_date):
        year, month, day = (int(x) for x in start_date.split('-'))
        d = date(year, month, day)

        def last_sunday(d):
            d = d.toordinal()
            last = d - 6
            start = last - (last % 7)
            end = start + 7
            start = date.fromordinal(start)
            end = date.fromordinal(end)
            
            return start, end
        
        df = self.agg.drop_duplicates(keep='first')
        start, end = last_sunday(d)
        mask = (df['week'] >= str(start)) & (df['week'] <= str(end))
        df = df[mask]
        self.agg = df

    def group(self):
        self.clean('2019-12-15')
        impressions = self.agg.impressions.sum()
        ctr = self.agg.ctr.mean()
        cost = self.agg.cost.sum()
        clicks = self.agg.clicks.sum()
        cpc = cost/clicks
        interactions = self.agg.interactions.sum()
        conversions = self.agg.conversions.sum()
        
        returned = {
            'cost': cost,
            'awareness': {
                'engagement': interactions,
                'impressions': impressions
            },
            'evaluation': {
                'ctr': ctr,
                'cpc': cpc
            },
            'conversion': {
                'cta': conversions,
                'site_visits': clicks
            }
        }

        return json.dumps(returned)