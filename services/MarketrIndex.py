import pandas as pd
import numpy as np
import json


######################### SUPER CLASS #########################

class MarketrIndex(object):
    def __init__(self, ltv):
        self.ltv = ltv
        self.social_columns = ['id', 'adset_id', 'campaign_id',  pd.Grouper(key='date_start', freq='W-MON')]
        self.search_columns = ['adid', 'adgroupid', 'campaignid', pd.Grouper(key='date_start', freq='W-MON')]
        self.agg_set = {
            'cpm': 'mean', 'cost': 'sum', 'cpc': 'mean',
            'conversions': 'sum', 'ctr' : 'mean', 'clicks':'sum',
            'lcr': 'mean', 'impressions': 'sum', '_cost': 'mean'
        }
    
        self.assertion_error = 'dataset type required, e.g. search=True || social=True'

    def clean(self, df):
        df.fillna(0, inplace=True)
        df.drop_duplicates(subset=['cost', 'clicks'], inplace=True)
            
        df['lcr'] = df.apply(lambda x: self.lcr(x['conversions'], x['clicks']), axis=1)
        df['ltv'] = self.ltv
        
        return df
    
    def lcr(self, conversions, clicks):
        if clicks > 0:
            return conversions / clicks
        else:
            return 0
    
    def pp100(self, ctr, lcr, cpc, impressions):        
        # translation: profit potential per 1,000 spent: PP100 = ( [LTV] * [LCR] * (100 / Total Spend)  - 100 )
        try:
            formula = (self.ltv * lcr * (100 / cpc) - 100)
        except:
            formula = 0

        return formula
    
    
    def IndexFormula(self, pp100):
        def formula(pp100):
            _base = 0.00077572178
            base = _base if pp100 > 0 else _base * -1
            exp = 1.3198878401

            formula = base * abs(pp100) ** exp
            return formula

        returned = pp100.apply(formula)
        
        return returned
    
    def Comparisons(self, df):
        if df.pp100.mean() != 0:
#             df['pp100_comp'] = (df['pp100'] - df.pp100.mean()) / df.pp100.mean() * 100
            df['pp100_comp'] = (df['pp100'] - df.pp100.mean()) / abs( df.pp100.mean() )* 100

        if df.marketr_index.mean() != 0:
            df['index_comp'] = (df['marketr_index'] - df.marketr_index.mean()) / df.marketr_index.mean() * 100

        if df.cost.mean() != 0:
            df['cost_comp'] = (df['cost'] - df.cost.mean()) / df.cost.mean() * 100

        if df.conversions.mean() != 0:
            df['cpl_comp'] = (
                ((df['cost'] / df['conversions'])
                - (df.cost.mean() / df.conversions.mean()))
                / (df.cost.mean() / df.conversions.mean())
                * 100
            )

        return df
    
    def get_perc_change(self, _id, df, column_selector, google=True):
        mi_perc_change = df[df[column_selector[0]] == _id] \
            .sort_values(by='date_start', ascending=False) \
            .groupby([column_selector[0], pd.Grouper(key='date_start', freq='W-MON')]) \
            .agg({'marketr_index': 'mean'}).marketr_index.pct_change().reset_index()

        returned = mi_perc_change.loc[mi_perc_change['date_start'] == mi_perc_change['date_start'].max()]['marketr_index']

        return returned.iloc[0]

    
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
          
        df['pp100'] = self.pp100(df.ctr, df.lcr, df.cpc, df.impressions)
        
        def clean_impressions(imp):
            if imp < 20:
                penalty = .1
            elif imp >= 20 and imp < 40:
                penalty = .3
            elif imp >= 40 and imp < 60:
                penalty = .6
            elif imp >= 60 and imp < 100:
                penalty = .8
            else:
                penalty = 1
                
            return penalty
        
        df['pp100'] = df.apply(lambda x: x['pp100'] * clean_impressions(x['impressions']), axis=1)
                

        return df.sort_values(by="date_start")

    
    def Assign(self, df, column_selector, search=False, social=False):
        assert search or social, self.assertion_error
        
        group_columns = [column_selector]

        if 'campaign_id' in df.columns:
            group_columns.append('campaign_id')
        if 'campaignid' in df.columns:
            group_columns.append('campaignid')

        group_columns = [item for sublist in group_columns for item in sublist]
        
        try:
            df = df.groupby(group_columns).agg(self.agg_set).reset_index()
        except:
            df = df.groupby(column_selector).agg(self.agg_set).reset_index()
        
        df['pp100'] = self.pp100(df.ctr, df.lcr, df.cpc, df.impressions)
        df['marketr_index'] = self.IndexFormula(df.pp100)

        mi_sum = df.marketr_index.sum()
        mi_mean = df.marketr_index.mean()
        mi_std = df.marketr_index.std()
        
        df['action'] = df.sort_values(by=['marketr_index'])['marketr_index'].apply(
            lambda x: self.eval_action(x, mi_sum, mi_mean, mi_std)
        )
        
        df = self.Comparisons(df)

        return df
    
    def reorder_m_index(self, x):
        return np.average(
            x['marketr_index'], weights=x['cost'] if x['cost'] > 0 else 1
        )
    
    def eval_action(self, index, sum, mean, std):   
        breakpoint = 1*std
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

Profit Potential per 1,000 Impressions (pp100)
Cost per 1,000 Impressions
LTV
CTR
LCR
NUMBER = [ pp100 ]
pp100 = ( [LTV] [CTR] [Lead Conversion Rate] 1,000 ) - ( ( [Total Spend ] / [ Impressions ] ) 1,000 )

Market(r) Index (T5) = IF( [NUMBER] > 0, 0.00077572178 ABS( [ NUMBER] ) ^ 1.3198878401, -0.00077572178 ABS( [NUMBER] ) ^ 1.3198878401)
"""


class AdIndex(MarketrIndex):
    def __init__(self, ltv):
        super().__init__(ltv)
    
    def PrepIndex(self, df, search=False, social=False):
        df = self.Prep(df, search=search, social=social)
        
        df['marketr_index'] = self.IndexFormula(df.pp100)
        
        df = self.Comparisons(df)

        mi_sum = df.marketr_index.sum()
        mi_mean = df.marketr_index.mean()
        mi_std = df.marketr_index.std()


        df['action'] = df.sort_values(by=['marketr_index'])['marketr_index'].apply(
            lambda x: self.eval_action(x, mi_sum, mi_mean, mi_std)
        )

        agg = dict(self.agg_set)
        agg['marketr_index'] = 'mean'


        if search and not social:
            column_selector = ['adid']
        if social and not search:
            column_selector = ['id']

        agg_df = self.Assign(df, column_selector[0], search=search, social=social)
        
        agg_df['perc_change'] = agg_df[column_selector[0]].apply(lambda x: self.get_perc_change(x, df, column_selector, google=search))
        
        return {
            'range': df,
            'agg': agg_df
        }



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
        
        agg = self.agg_set
        agg['marketr_index'] = 'mean'

        grouped = df.groupby(column_selector[0])
        agg_df = grouped.agg(agg).reset_index()
        agg_df = self.Assign(agg_df, column_selector[0], search=search, social=social)
        agg_df['perc_change'] = agg_df[column_selector[0]].apply(lambda x: self.get_perc_change(x, df, column_selector))
    
        return {
            'range': df,
            'agg': agg_df
        }
    

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
        
    def PrepIndex(self, ranged_df, agg_df):
        cost = agg_df.head(1)['_cost'][0]
        index = np.average(agg_df.marketr_index, weights=agg_df.cost)
        
        ranged_df = ranged_df.groupby('date_start').agg(self.agg_set).reset_index()
        ranged_df['pp100'] = self.pp100(ranged_df.ctr, ranged_df.lcr, ranged_df.cpc, ranged_df.impressions)

        return {
            'cost': cost,
            'index': index,
            'raw': ranged_df
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
        
        df = pd.concat(dfs, sort=True)
        df['pp100'] = self.pp100(df.ctr, df.lcr, df.cpc, df.impressions)
            
        return {
            'index': sum(arr),
            'raw': df
        }



######### compile ##########
def compile_master(ltv=None, search_df=None, social_df=None):
    if search_df is not None and social_df is not None:
        total_spent = search_df.head(1)['_cost'][0] + social_df.head(1)['_cost'][0]
    elif search_df is not None and social_df is None:
        total_spent = search_df.head(1)['_cost'][0]
    elif social_df is not None and search_df is None:
        total_spent = social_df.head(1)['_cost'][0]

    # init objects
    ad_index_obj = AdIndex(ltv) 
    group_index_obj = AdGroupIndex(ltv)
    campaign_index = CampaignIndex(ltv)
    bucket_index = BucketIndex(ltv)
    index = PortfolioIndex(ltv, total_spent)

    def _compile(ltv=ltv, search_df=search_df, social_df=social_df, ad_index_obj=ad_index_obj, group_index_obj=group_index_obj, campaign_index=campaign_index, bucket_index=bucket_index, index=index):
        
        search_columns = ['campaign_name', 'imageadurl', 'adid', 'headline1', 'headline2', 'finalurl', 'description', 'daily_budget']
        social_columns = ['campaign_name', 'ad_name', 'id', 'thumbnail_url', 'body', 'daily_budget']
        
        def trickle(active_df, active_columns, subset, id_key, search=False, social=False):
            try:
                index = ad_index_obj.PrepIndex(active_df, search=search, social=social)
                new_index = active_df[active_columns].drop_duplicates(subset = subset)

                # export to view performance metrics by creative
                index_agg = pd.merge(new_index, index['agg'], left_on=subset, right_on=subset)
                index = pd.merge(new_index, index['range'], left_on=subset, right_on=subset)

                t4 = group_index_obj.PrepIndex(index, search=search, social=social)
                t3 = campaign_index.PrepIndex(t4, search=search, social=social)
                t2 = bucket_index.PrepIndex(t3['range'], t3['agg'])

                id_map = active_df[['campaign_name', id_key]].drop_duplicates(subset = 'campaign_name')
                _id_map = {}
                for row, value in id_map.iterrows():
                    name = (active_df.loc[row]['campaign_name'])
                    _id = (active_df.loc[row][id_key])
                    _id_map[_id] = name

                t3['agg']['campaign_name'] = t3['agg'][id_key].apply(lambda x: _id_map[x])
                t3['range']['campaign_name'] = t3['range'][id_key].apply(lambda x: _id_map[x])
                
            except Exception as e:
                print(e)
                index_agg=index=t2=t3=t4 = None
            
            return index_agg, index, t2, t3, t4
        
        social_index_agg, social_index, social_t2, social_t3, social_t4 = trickle(
            social_df, social_columns, 'id', 'campaign_id', search=False, social=True 
        )
        
        search_index_agg, search_index, search_t2, search_t3, search_t4 = trickle(
            search_df, search_columns, 'adid', 'campaignid', search=True, social=False 
        )
        
        returned = {
            'social': {
                'social_index_agg': social_index_agg,
                'social_index': social_index,
                'social_t2': social_t2,
                'social_t3': social_t3,
                'social_t4': social_t4
            },
            'search': {
                'search_index_agg': search_index_agg,
                'search_index': search_index,
                'search_t2': search_t2,
                'search_t3': search_t3,
                'search_t4': search_t4
            }
        }
        return returned
    
    sets = _compile()
    t1 = index.PrepIndex(sets['social']['social_t2'], sets['search']['search_t2'])
    
    def export(df):
        if df is not None:
            try:
                df['date_start'] = df.date_start.dt.strftime('%Y-%m-%d')
            except Exception as e:
                print(e)
            return json.loads(df.to_json(orient='records'))
        else:
            return None

    if search_df is not None:
        search_conversions = int(search_df.conversions.sum())
        search_clicks = int(search_df.clicks.sum())
    else:
        search_conversions=search_clicks=0

    if social_df is not None:
        social_conversions = int(social_df.conversions.sum())
        social_clicks = int(social_df.clicks.sum())
    else:
        social_conversions=social_clicks = 0
        

    struct = {
        'total_conversions': social_conversions + search_conversions,
        'total_clicks': search_clicks + social_clicks,
        'total_spent': total_spent,
        'buckets': [],
        'campaigns': {},
        'ranged_campaigns': {},
        'ad_groups': {
            'social': export(sets['social']['social_t4']),
            'search': export(sets['search']['search_t4'])
        },
        'ads': {
            'social': export(sets['social']['social_index_agg']),
            'search': export(sets['search']['search_index_agg'])
        },
        'ranged_ads': {
            'social': export(sets['social']['social_index']),
            'search': export(sets['search']['search_index'])
        },
        'aggregate': {
            'index': t1.get('index'),
            'raw': export(t1.get('raw'))
        }
    }

    if search_df is not None:
        struct['buckets'].append({
            'type': 'search',
            'cost': sets['search']['search_t2'].get('cost'),
            'index': sets['search']['search_t2'].get('index'),
            'raw': export(sets['search']['search_t2'].get('raw'))
        })
        struct['campaigns']['search'] = export(sets['search']['search_t3'].get('agg'))
        struct['ranged_campaigns']['search'] = export(sets['search']['search_t3'].get('range'))
        
    if social_df is not None:
        struct['buckets'].append({
            'type': 'social',
            'cost': sets['social']['social_t2'].get('cost'),
            'index': sets['social']['social_t2'].get('index'),
            'raw': export(sets['social']['social_t2']['raw'])
        })     
        
        struct['campaigns']['social'] = export(sets['social']['social_t3'].get('agg'))
        struct['ranged_campaigns']['social'] = export(sets['social']['social_t3'].get('range')) 
        

    return struct