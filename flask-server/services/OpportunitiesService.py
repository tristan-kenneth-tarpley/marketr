import pandas as pd
import numpy as np
import json

## super class

class OpportunityScore (object):
    def __init__(self, ltv: float=None, lcr: float=None):
        self.ltv = ltv
        self.lcr = lcr
    
    def ParsePI(self, pi):
        if pi == 'neutral':
            returned = 5
        elif pi == 'high':
            returned = 10
        else:
            returned = 1
        return returned
         
    # pp100_range is not actually a list, it's a pd series...but I  don't feel like finding a type library with that
    def mi_q_opp_score(self, pp100_range: list) -> int:
        """
        = ( [PP100 Value] - QUARTILE( [PP100 Range] , 1 ) )
          / (( QUARTILE(  VV 7: VV 47, 3) - QUARTILE( [PP100 Range] , 1) ) )
          * (10-1) + 1 )
        """
        first_q = pp100_range.quantile([.25]).iloc[0]
        third_q = pp100_range.quantile([.75]).iloc[0]
        
        score = pp100_range.apply(lambda x: (
            ( x - first_q ) \
            / ((third_q) - first_q) \
            * (10 - 1) \
            + 1
        ))

        def constrain(score) -> int:
            if score < 1:
                returned = 1
            elif score > 10:
                returned = 10
            else:
                returned = score
            return returned

        score = score.apply(lambda x: constrain(x))

        return score
    
    
## topical (search) opportunities
    
class TopicalOpps(OpportunityScore):
    def __init__(self, ltv: float=10, lcr: float=.03):
        super().__init__(ltv=ltv, lcr=lcr)
    
    def prep(self, df):
        df['cpc'] = df['cost'] / df['clicks']
        #df['firstpagecpc'] = df['firstpagecpc'].apply(lambda x: round(x / 1000000, 2))
        df['searchimprshare'] = df['searchimprshare'].apply(lambda x: x / 100)
        df['purchase_intent'] = 'neutral'
        df['ctr'] = df.ctr.apply(lambda x: x / 100)
        
        agg_set = {
            'impressions': 'sum',
            'clicks': 'sum',
            'ctr': 'mean',
            'cpc': 'mean',
            'cost': 'sum',
            'qualityscore': 'mean',
            'searchimprshare': 'mean',
            'searchtopis': 'mean',
            'searchlosttopisrank': 'mean'
        }
        
        df = df.groupby(['keyword', 'purchase_intent']).agg(agg_set).reset_index()
        
        return df
    
    def ExtractOpps(self, df, indexobj):
        df = self.prep(df)
        
        df['pp100'] = df.apply(lambda x: indexobj.pp100(x['ctr'], self.lcr, x['cost'], x['impressions']), axis=1)

        df['qs_opp_score'] = df.qualityscore.apply(lambda x: 10 - x)
        df['is_opp_score'] = df.searchimprshare.apply(lambda x: (1 - x) * 10)
        df['top_is_opp_score'] = df.searchtopis.apply(lambda x: (1 - x) * 10)
        df['lost_is_opp_score'] = df.searchlosttopisrank.apply(lambda x: x * 10)
        df['pi_opp_score'] = df.purchase_intent.apply(lambda x: self.ParsePI(x))
        
        df['constrained_mi'] = self.mi_q_opp_score(df.pp100)
        
        return df
    
    def AggOppScore(self, df, indexobj):
        df = self.ExtractOpps(df, indexobj)
        
        """
        Base Scores = Range of scores for ( [Quality Score Opp. Score], [Search impr. share Opp. Score], [Search top IS Opp. Score], [Search lost IS (rank) Opp. Score], [Purchase Intent Opp. Score] )

        Topical Opportunity Score = AVERAGE( [Base Scores] ) * 0.5 + [ Constrained Marketr Index Opp. Score] * 0.5
        
        NOTE:  IF Impressions < 50 or ctr == 0, Do not calculate or display
        """
        
        # syntax: np.average(x['marketr_index'], weights=x['cost'] if x['cost'] > 0 else 1)

        
        def opp_score(x):                
            base_scores = (
                x.qs_opp_score + x.is_opp_score + x.top_is_opp_score + x.lost_is_opp_score + x.pi_opp_score
            )
            exp = ((base_scores / 5) * .5 + x.constrained_mi * .5)
            return exp if (x.impressions > 50 and x.ctr > 0) else 0
        
        df['opp_score'] = df.apply(lambda x: opp_score(x), axis=1)
        
        df['cleaned_keywords'] = df.keyword.apply(lambda x: x.replace("+", "").replace('"', "").replace("[", "").replace("]", ""))
        
        df = df.sort_values(by='opp_score', ascending=False)
        
        return {
            'aggregate': json.loads(df.groupby('cleaned_keywords').agg({'opp_score': 'mean'}).sort_values(by='opp_score', ascending=False).reset_index().to_json(orient='records')),
            'raw': json.loads(df.to_json(orient='records'))
        }


def compile_topics(_df, index, lcr, ltv):
    opps = TopicalOpps(ltv=ltv, lcr=lcr)
    dfs = opps.AggOppScore(_df, index)
    
    return dfs