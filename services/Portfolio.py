import pandas as pd
import json
from services.UserService import UserService
from datetime import date, datetime, timedelta

class Portfolio:
    def __init__(self, agg=None, google=None, facebook=None):
        self.agg = agg
        self.google_df = google
        self.facebook_df = facebook

    def last_sunday(self, d):
        offset = (d.weekday() - 6) % 7
        start = d - timedelta(days=offset)

        end_offset = (6-d.weekday()) % 7
        next_sunday = timedelta(days=end_offset)
        end = d + next_sunday

        
        return start, end

    def clean(self, start_date):
        year, month, day = (int(x) for x in start_date.split('-'))
        d = date(year, month, day)

        df = self.agg.drop_duplicates(keep='first')
        start, end = self.last_sunday(d)
        mask = (df['week'] >= str(start)) & (df['week'] <= str(end))
        df = df[mask]
        self.agg = df

    def group(self, start_date):
        self.clean(start_date)
        impressions = self.agg.impressions.sum()
        ctr = self.agg.ctr.mean()
        cost = self.agg.cost.sum()
        clicks = self.agg.clicks.sum()
        cpc = cost/clicks
        interactions = self.agg.interactions.sum()
        conversions = self.agg.conversions.sum()
        d = UserService.now()
        year, month, day = (int(x) for x in start_date.split('-'))
        d = date(year, month, day)
        start, end = self.last_sunday(d)
        returned = {
            'range': {
                'start': str(start),
                'end': str(end)
            },
            'cost': cost,
            'awareness': {
                'engagement': impressions/interactions,
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