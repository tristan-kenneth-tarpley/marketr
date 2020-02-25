import json
import data.db as db
import pandas as pd
import numpy as np

class CampaignMetaManager:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def get_reference(self):
        df = db.sql_to_df(f"select * from campaign_reference where customer_id = {self.customer_id} order by claimed desc")
        
        return df

    def group(self, df_list):
        args = [df for df in df_list]
        df = pd.concat(args)
        df['campaign_id'] = df['campaign_id'].astype(int)
        df.state = df.state.astype(str)

        ref = self.get_reference()

        _df = pd.merge(df, ref, on=['campaign_id', 'type', 'campaign_name'], how='left')
        _df['claimed'] = _df['claimed'].apply(lambda x: False if np.isnan(x) else True)
        _df = _df.sort_values(by='claimed', ascending=False)
        return _df.to_json(orient='records')

    def claim(self, campaign_name, customer_id, campaign_id, _type):
        query = """
        if not exists (select * from campaign_reference where customer_id = ? and campaign_id = ?)
        INSERT INTO campaign_reference (campaign_name, customer_id, campaign_id, type, claimed)
        values(?, ?, ?, ?, 1)
        """
        db.execute(query, False, (customer_id, campaign_id, campaign_name, customer_id, campaign_id, _type), commit=True)