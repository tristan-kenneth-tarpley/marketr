import pandas as pd
from DataModels.PlatformModel import PlatformModel
import data.db as db

class google_ads(PlatformModel):   
    def __init__(self, df, start_range=None, end_range=None) -> None:
        self.filters = {
            'Ad type': ['Expanded text ad'],
            'Ad status': ['Enabled']
        }
        self.qualifications = {
            'Impr.': [
                (lambda col, df: df[col] > 100)
            ]
        }
        
        self.start_range = start_range
        self.end_range = end_range
        
        PlatformModel.__init__(
            self,
            df=df,
            start_range = start_range,
            end_range = end_range,
            filters=self.filters,
            qualifications=self.qualifications
        )
        
        self.raw_df = df
        df = self.clean(df)
        self.df = self.qualify(df)
        
    def clean(self, df) -> dict:
        self.raw_df.drop(df.tail(5).index,inplace=True)
        
        for key in self.filters:
            for approved in self.filters[key]:
                df = df[df[key] == approved]
        
        df['Impr.'].replace({',':''}, regex=True, inplace=True)
        df['Impr.'] = df['Impr.'].astype('int64')
        
        df['Interaction rate'].replace({'--':'0'}, regex=True, inplace=True)
        df['Interaction rate'].replace({'%':''}, regex=True, inplace=True)
        df['Interaction rate'] = df['Interaction rate'].astype('float')

        df.sort_values(by='Interaction rate', ascending=False, inplace=True)
        return df

    def packJSON(self):
        #   pos 1 to get best ad, 0 to get worst ad
        def ad_metrics(df, pos=0):
            ad = {
                'campaign': df['Campaign'].iloc[0] if pos == 0 else df['Campaign'].iloc[-1],
                'clicks': df['Interactions'].iloc[0] if pos == 0 else df['Interactions'].iloc[-1],
                'ad_group': df['Ad group'].iloc[0] if pos == 0 else df['Ad group'].iloc[-1],
                'cost': df['Cost'].iloc[0] if pos == 0 else df['Cost'].iloc[-1],
                'ctr': df['Interaction rate'].iloc[0] if pos == 0 else df['Interaction rate'].iloc[-1],
                'headline_1': df['Headline 1'].iloc[0] if pos == 0 else df['Headline 1'].iloc[-1],
                'headline_2': df['Headline 2'].iloc[0] if pos == 0 else df['Headline 2'].iloc[-1],
                'description': df['Description'].iloc[0] if pos == 0 else df['Description'].iloc[-1],
                'impressions': df['Impr.'].iloc[0] if pos == 0 else df['Impr.'].iloc[-1]
            }
            return ad

        struct = {
            'start_range': self.start_range,
            'end_range': self.end_range,
            'spend': self.raw_df['Cost'].sum(),
            'ctr': self.df['Interaction rate'].mean(),
            'best_ad': ad_metrics(self.df),
            'worst_ad': ad_metrics(self.df, pos=1)
        }
        
        return struct

    def save(self, customer_id):
        struct = self.packJSON()
        query = """
                exec store_ad_upload
                    @customer_id = ?,
                    @campaign = ?,
                    @ad_group = ?,
                    @cost = ?,
                    @click_through = ?,
                    @clicks = ?,
                    @impressions = ?,
                    @headline_1 = ?,
                    @headline_2 = ?,
                    @best_worst_binary = ?,
                    @description = ?
                """
        base = struct['best_ad']
        tup = (
            int(customer_id),
            base['campaign'],
            base['ad_group'],
            float(base['cost']),
            float(base['ctr']),
            int(base['clicks']),
            int(base['impressions']),
            base['headline_1'],
            base['headline_2'],
            int(1),
            base['description']
        )

        best_id, cursor = db.execute(query, True, tup)
        best_id = cursor.fetchone()[0]

        base = struct['worst_ad']
        tup = (
            int(customer_id),
            base['campaign'],
            base['ad_group'],
            float(base['cost']),
            float(base['ctr']),
            int(base['clicks']),
            int(base['impressions']),
            base['headline_1'],
            base['headline_2'],
            int(0),
            base['description']
        )

        worst_id, cursor = db.execute(query, True, tup)
        worst_id = cursor.fetchone()[0]

        query = """
                INSERT INTO ad_history
                (start_range, end_range, cost, best_id, worst_id, customer_id, agg_ctr)
                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """
        tup = (
            self.start_range,
            self.end_range,
            struct['spend'],
            best_id,
            worst_id,
            customer_id,
            struct['ctr']
        )
        db.execute(query, False, tup, commit=True)

