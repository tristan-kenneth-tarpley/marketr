import pandas as pd
import numpy as np
import json
######################### SUPER CLASS #########################

class MarketrIndex(object):
    def __init__(self, ltv):
        self.ltv = ltv
        self.social_columns = ['id', 'adset_id', 'campaign_id', '_cost',  pd.Grouper(key='date_start', freq='W-MON')]
        self.search_columns = ['adid', 'adgroupid', 'campaignid', '_cost', pd.Grouper(key='date_start', freq='W-MON')]
        self.agg_set = {
            'cpm': 'mean', 'cost': 'sum',
            'conversions': 'sum', 'ctr' : 'sum', 'clicks':'sum',
            'lcr': 'mean', 'impressions': 'sum'
        }
    
        self.assertion_error = 'dataset type required, e.g. search=True || social=True'

    def clean(self, df):
        df.fillna(0, inplace=True)
        df['lcr'] = df.conversions.sum() / df.clicks.sum() if df.clicks.sum() > 0 else .02
        df['ltv'] = self.ltv
        return df
    
    def pp1ki(self, ctr, lcr, spend, impressions):
        # translation: profit potential per 1,000 impressions

        try:
            formula = (self.ltv * ctr * lcr * 1000) - ((spend / impressions) * 1000)
        except Exception as e:
            print(e)
            formula = 0
        return formula
    
    def Prep(self, DF, search=False, social=False):
        assert search == True or social == True, self.assertion_error
        if search:
            columns = self.search_columns
        elif social:
            columns = self.social_columns
        
        df = self.clean(DF)
        df['cpm'] = 1000 * df.cost / df.impressions
        df['date_start'] = pd.to_datetime(df['date_start']) - pd.to_timedelta(7, unit='d')
        df['ctr'] = df.ctr.apply(lambda x: x / 100)

        df = df.groupby(columns).agg(self.agg_set).reset_index()
  
        df['pp1ki'] = self.pp1ki(df.ctr, df.lcr, df.cost, df.impressions)
        
        return df
    
    def IndexFormula(self, number):
        _base = 0.00077572178
        base = _base if _base > 0 else _base * -1
        exp = 1.3198878401
        
        formula = base * abs(number) ** exp
        return formula
    
    def Assign(self, df, column_selector, search=False, social=False):
        assert search or social, self.assertion_error

        df = df.groupby(column_selector).agg(self.agg_set).reset_index()
        
        df['pp1ki'] = self.pp1ki(df.ctr, df.lcr, df.cost, df.impressions)
        df['marketr_index'] = self.IndexFormula(df.pp1ki)
        
        mi_sum = df.marketr_index.sum()
        mi_mean = df.marketr_index.mean()
        mi_std = df.marketr_index.std()
        
        df['action'] = df.sort_values(by=['marketr_index'])['marketr_index'].apply(
            lambda x: self.eval_action(x, mi_sum, mi_mean, mi_std)
        )

        return df
    
    def reorder_m_index(self, x):
        return np.average(
            x['marketr_index'], weights=x['cost'] if x['cost'] > 0 else 1
        )
    
    def eval_action(self, index, sum, mean, std):   
        breakpoint = 1*std
#         print('std', std)
#         print('mean', mean)
#         print('index', index)
        if index > mean + breakpoint:
            _action = 'invest more'
        elif index <  mean - breakpoint:
            _action = 'kill it'
        else:
            _action = 'unclear'

        return _action




######################### TIER 5 #########################
"""
Tier 5 (ad level)
Output(s) Market(r) Index Tier 5 = Power function of Profit Potential per 1,000 Impressions

Input(s) - Required data inputs (either assumed, calculated, or input from the user):

Profit Potential per 1,000 Impressions (PP1KI)
Cost per 1,000 Impressions
LTV
CTR
LCR
NUMBER = [ PP1KI ]
PP1KI = ( [LTV] [CTR] [Lead Conversion Rate] 1,000 ) - ( ( [Total Spend ] / [ Impressions ] ) 1,000 )

Market(r) Index (T5) = IF( [NUMBER] > 0, 0.00077572178 ABS( [ NUMBER] ) ^ 1.3198878401, -0.00077572178 ABS( [NUMBER] ) ^ 1.3198878401)
"""


class AdIndex(MarketrIndex):
    def __init__(self, ltv):
        super().__init__(ltv)
    
    def PrepIndex(self, df, search=False, social=False):
        df = self.Prep(df, search=search, social=social)
        df['marketr_index'] = self.IndexFormula(df.pp1ki)
        
        mi_sum = df.marketr_index.sum()
        mi_mean = df.marketr_index.mean()
        mi_std = df.marketr_index.std()
        df['action'] = df.sort_values(by=['marketr_index'])['marketr_index'].apply(
            lambda x: self.eval_action(x, mi_sum, mi_mean, mi_std)
        )
        
        return df



######################### TIER 4 #########################

"""
Tier 4 (ad group level)
Output(s)

Weighted Average of Market(r) Index of Tier 5 Ads within specific Ad Groups.
Total spend of Ad Group
Input(s)

Market(r) Index for all Tier 5 ads within a specific Ad Group
Spend per Ad
Spend T5 = Spend for that period per Ad Market(r) Index for Ad Group (T4) = AVERAGE.WEIGHTED ( [RANGE OF MARKETR T5 INDICES], [RANGE OF SPEND T5] )
"""

class AdGroupIndex(MarketrIndex):
    def __init__(self, ltv):
        super().__init__(ltv)
        
    def PrepIndex(self, df, search=False, social=False):
        
        if search:
            column_selector = self.search_columns[1:]
        elif social:
            column_selector = self.social_columns[1:]
            
        df = self.Assign(df, column_selector, search=search, social=social)
        df['marketr_index'] = df.apply(self.reorder_m_index, axis=1)
        
        return df





######################### TIER 3 #########################
"""
Tier 3 (campaign level)
Output(s)

Weighted Average of Market(r) Index of Tier 4 Ad Groups within specific Campaigns
Input(s)

Market(r) Index for all Tier 4 Ad Groups within a specific Campaign
Spend per Ad Group
Spend T4 = Spend for that period per Ad Group
Market(r) Index for Campaign (T3) = AVERAGE.WEIGHTED ( [RANGE OF MARKETR T4 INDICES], [RANGE OF SPEND T4] )
"""

class CampaignIndex(MarketrIndex):
    def __init__(self, ltv):
        super().__init__(ltv)
        
    def PrepIndex(self, df, search=False, social=False):
        
        if search:
            column_selector = self.search_columns[2:]
        elif social:
            column_selector = self.social_columns[2:]
        
        df = self.Assign(df, column_selector, search=search, social=social)
        df['marketr_index'] = df.apply(self.reorder_m_index, axis=1)

        return df

######################### TIER 2 #########################
"""
Tier 2 (bucket level)
Output(s)

Aggregate value of Market(r) Index for specific Bucket
Input(s)

Market(r) Index for all Tier 3 Campaigns within a specific Bucket
% of spend allocated to that particular Bucket
Spend T3 = Spend for that period per Campaign
Market(r) Index for Bucket (T2) = AVERAGE.WEIGHTED ( [RANGE OF MARKETR T3 INDICES ], [RANGE OF SPEND T3] )
"""

class BucketIndex(MarketrIndex):
    def __init__(self, ltv):
        super().__init__(ltv)
        
    def PrepIndex(self, df):
        cost = df.head(1)['_cost'][0]
        index = np.average(df.marketr_index, weights=df.cost)
        df = df.groupby('date_start').agg(self.agg_set).reset_index()
        df['pp1ki'] = self.pp1ki(df.ctr, df.lcr, df.cost, df.impressions)
        return {
            'cost': cost,
            'index': index,
            'raw': df
        }


######################### TIER 1 #########################
"""
Tier 1 (portfolio level)
Output(s)

Account level Market(r) Index value
Input(s)

Market(r) Index for all Tier 2 Buckets within a given Account
% of spend allocated to that particular Bucket
Spend % T2 = [Spend per T2] / [Total Spend]
T1 array = [MARKETR INDEX T2] ^ .5 * [Spend % T2] Market(r) Index (T1) = SUM( T1 array )
"""

class PortfolioIndex(MarketrIndex):
    def __init__(self, ltv, total_spent):
        super().__init__(ltv)
        self.total_spent = total_spent
        
    def PrepIndex(self, *args):
        def condition(index, cost):
            if index < 0:
                return (-1 * (abs(index) ** .5) * (cost / self.total_spent))
            else:
                return index ** .5 * (cost / self.total_spent)
            
        dfs = list()
        arr = list()
        for arg in args:
            if arg is not None:
                arr.append(condition(arg['index'], arg['cost']))
                dfs.append(arg['raw'])
            
        df = pd.concat(dfs).groupby('date_start').agg(self.agg_set).reset_index()
        df['pp1ki'] = self.pp1ki(df.ctr, df.lcr, df.cost, df.impressions)
            
        return {
            'index': sum(arr),
            'raw': df
        }



######### compile ##########
def compile_master(ltv=None, search_df=None, social_df=None):

    if search_df is not None and social_df is not None:
        total_spent = search_df.head(1)['_cost'][0] + social_df.cost.sum()
    elif search_df is not None and social_df is None:
        total_spent = search_df.head(1)['_cost'][0]
    elif social_df is not None and search_df is None:
        total_spent = social_df.cost.sum()
 

    # init objects
    ad_index_obj = AdIndex(ltv) 
    group_index_obj = AdGroupIndex(ltv)
    campaign_index = CampaignIndex(ltv)
    bucket_index = BucketIndex(ltv)
    index = PortfolioIndex(ltv, total_spent)

    def compile_search(ltv=ltv, search_df=search_df, ad_index_obj=ad_index_obj, group_index_obj=group_index_obj, campaign_index=campaign_index, bucket_index=bucket_index, index=index):
        try:
            # initialize at ad level
            search_index = ad_index_obj.PrepIndex(search_df, search=True)
            new_search_index = search_df[['campaign_name', 'imageadurl', 'adid', 'headline1', 'headline2', 'finalurl', 'description', 'daily_budget']].drop_duplicates(subset ="adid")
     
            # export to view performance metrics by creative
            search_index = pd.merge(new_search_index, search_index, left_on='adid', right_on='adid')
         
            # ad group level
            search_t4 = group_index_obj.PrepIndex(search_index, search=True)
            # campaign level
            search_t3 = campaign_index.PrepIndex(search_t4, search=True)

            # bucket level
            search_t2 = bucket_index.PrepIndex(search_t3)
            id_map = search_df[['campaign_name', 'campaignid']].drop_duplicates(subset = 'campaign_name')
            _id_map = {}
            for row, value in id_map.iterrows():
                name = (search_df.iloc[row]['campaign_name'])
                _id = (search_df.iloc[row]['campaignid'])
                _id_map[_id] = name

            search_t3['campaign_name'] = search_t3.campaignid.apply(lambda x: _id_map[x])
        except Exception as e:
            print(e)
            search_index=search_t2=search_t3=search_t4 = None

        return search_index, search_t2, search_t3, search_t4

    def compile_social(ltv=ltv, social_df=social_df, ad_index_obj=ad_index_obj, group_index_obj=group_index_obj, campaign_index=campaign_index, bucket_index=bucket_index, index=index):
        try:
            # initialize at ad level
            social_index = ad_index_obj.PrepIndex(social_df, social=True)

            new_social_index = social_df[['campaign_name', 'id', 'thumbnail_url', 'body', 'daily_budget']].drop_duplicates(subset = 'id')
            # export to view performance metrics by creative
            social_index = pd.merge(new_social_index, social_index, left_on='id', right_on='id')

            # ad group level
            social_t4 = group_index_obj.PrepIndex(social_index, social=True)
            # campaign level
            social_t3 = campaign_index.PrepIndex(social_t4, social=True)

            social_t2 = bucket_index.PrepIndex(social_t3)

            id_map = social_df[['campaign_name', 'campaign_id']].drop_duplicates(subset = 'campaign_name')
            _id_map = {}
            for row, value in id_map.iterrows():
                name = (social_df.iloc[row]['campaign_name'])
                _id = (social_df.iloc[row]['campaign_id'])
                _id_map[_id] = name

            social_t3['campaign_name'] = social_t3.campaign_id.apply(lambda x: _id_map[x])
        # bucket level
        # portfolio level
        except:
            social_index=social_t2=social_t3=social_t4 = None
        return social_index, social_t2, social_t3, social_t4


    social_index, social_t2, social_t3, social_t4 = compile_social()
    search_index, search_t2, search_t3, search_t4 = compile_search()
    
    t1 = index.PrepIndex(social_t2, search_t2)
    
    def export(df):
        if df is not None:
            df['date_start'] = df.date_start.dt.strftime('%Y-%m-%d')
            return json.loads(df.to_json(orient='records'))
        else:
            return None



    struct = {
        'total_spent': total_spent,
        'buckets': [],
        'campaigns': {
            'social': export(social_t3),
            'search': export(search_t3)
        },
        'ad_groups': {
            'social': export(social_t4),
            'search': export(search_t4)
        },
        'ads': {
            'social': export(social_index),
            'search': export(search_index)
        },
        'aggregate': {
            'index': t1.get('index'),
            'raw': export(t1.get('raw'))
        }
    }

    if search_df is not None:
        struct['buckets'].append({
            'type': 'search',
            'cost': search_t2.get('cost'),
            'index': search_t2.get('index'),
            'raw': export(search_t2.get('raw'))
        })
    if social_df is not None:
        struct['buckets'].append({
            'type': 'social',
            'cost': social_t2.get('cost'),
            'index': social_t2.get('index'),
            'raw': export(social_t2['raw'])
        })

    return struct