import pandas as pd
import numpy as np
import json
import math
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

        if self.agg is not None:
            df = self.agg.drop_duplicates(keep='first')
            start, end = self.last_sunday(d)
            mask = (df['week'] >= str(start)) & (df['week'] <= str(end))
            df = df[mask].fillna(0)
            self.agg = df

    def trendline(self):
        if self.agg is not None:
            df = self.agg.fillna(0)
    
            df['cpc'] = df.cost/df.clicks
            df['visits_per_thousand'] = 1000 / df['cpc']
            df = df.replace([np.inf, -np.inf], 0).drop_duplicates(keep='first').fillna(0)
            
            df['range'] = pd.to_datetime(df['week']) - pd.to_timedelta(7, unit='d')
            df = df.groupby(['week', pd.Grouper(key='range', freq='W-MON')])['visits_per_thousand'].sum().reset_index().sort_values('range')

            df['range'] = df.range.dt.strftime('%Y-%m-%d')
            df = df.groupby(['range'])['visits_per_thousand'].mean().reset_index().sort_values('range')

            return df.to_json(orient='records')
        else:
            return json.dumps([
                {'range': "0000-00-00", "visits_per_thousand": 0}
            ])


    def group(self):#, start_date):
        # self.clean(start_date)

        # d = UserService.now()
        # year, month, day = (int(x) for x in start_date.split('-'))
        # d = date(year, month, day)
        # start, end = self.last_sunday(d)

        if self.agg is not None:
            impressions = int(self.agg.impressions.sum())
            ctr = float(self.agg.ctr.mean()) if not math.isnan(self.agg.ctr.mean()) else 0
            cost = float(self.agg.cost.sum())
            clicks = int(self.agg.clicks.sum())
            interactions = int(self.agg.interactions.sum())
            conversions = int(self.agg.conversions.sum())

            cpc = cost/clicks if clicks > 0 else 0
            engagement = impressions/interactions if interactions > 0 else 0
            
            returned = {
                # 'range': {
                #     'start': str(start),
                #     'end': str(end)
                # },
                'cost': cost,
                'awareness': {
                    'engagement': engagement,
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
        else:
            returned = {
            #     'range': {
            #         'start': str(start),
            #         'end': str(end)
            #     },
                'cost': 0,
                'awareness': {
                    'engagement': 0,
                    'impressions': 0
                },
                'evaluation': {
                    'ctr': 0,
                    'cpc': 0
                },
                'conversion': {
                    'cta': 0,
                    'site_visits': 0
                }
            }

        return json.dumps(returned)