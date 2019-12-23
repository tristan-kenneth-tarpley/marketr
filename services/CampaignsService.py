import data.db as db

class CampaignService(object):
    def __init__(self, customer_id=None):
        self.customer_id = customer_id

    def struct(self, row):
        returned = {
            'campaign_id': row[0],
            'customer_id': row[1],
            'active': row[2],
            'platform': row[3],
            'category': row[4],
            'stage': row[5],
            'selling': row[6],
            'spend_rate': row[7],
            'seasonality': row[8],
            'creative_id': row[9],
            'ad_copy_id': row[10]
        }
        return returned

    def get_one(self, campaign_id=None):
        campaign, cursor = db.execute("SELECT * FROM user_campaigns WHERE campaign_id = ?", True, (campaign_id))
        campaign = cursor.fetchone()
        returned = self.struct(campaign)
        return returned

    def get_all(self):
        campaigns, cursor = db.execute("SELECT * FROM user_campaigns WHERE customer_id = ?", True, (self.customer_id,))
        campaigns = cursor.fetchall()
        campaign_list = list()
        for campaign in campaigns:
            campaign_list.append(self.struct(campaign))

        return campaign_list

    def new(self, platform=None, category=None, stage=None, selling=None, spend_rate=None):
        db.execute(
            "exec new_campaign @customer_id=?, @platform=?, @category=?, @stage=?, @selling=?, @spend_rate=?",
            False,
            (self.customer_id, platform, category, stage, selling, spend_rate),
            commit=True
        )


class Campaign(CampaignService):
    def __init__(self, customer_id=None, campaign_id=None):
        super().__init__(customer_id=customer_id)
        self.customer_id = customer_id
        self.campaign_id = campaign_id
        self.meta = self.get_one(campaign_id=campaign_id)

    def performance(self, df=None):
        pass

    def modify(self):
        pass

    def strategy(self):
        pass