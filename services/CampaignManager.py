import json
import data.db as db
import pandas as pd

class CampaignMetaManager:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def get_reference(self):
        df = db.sql_to_df(f"select * from campaign_reference where customer_id = {self.customer_id}")
        
        return df

    def group(self, df_list):
        args = [df for df in df_list]
        df = pd.concat(args)
        df['campaign_id']= df['campaign_id'].astype(int)
        ref = self.get_reference()
        
        _df = df.merge(ref, on=['campaign_id'], how='outer')

        return _df.to_json(orient="records")

    def claim(self, campaign_name, customer_id, campaign_id, _type):
        query = """
        if not exists (select * from campaign_reference where customer_id = ? and campaign_id = ?)
        INSERT INTO campaign_reference (campaign_name, customer_id, campaign_id, type, claimed)
        values(?, ?, ?, ?, 1)
        """
        db.execute(query, False, (customer_id, campaign_id, campaign_name, customer_id, campaign_id, _type), commit=True)