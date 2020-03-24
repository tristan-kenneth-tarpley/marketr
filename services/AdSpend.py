import math
import data.db as db
import pandas as pd
import json

class GetRec:
    def __init__(self, revenue, stage, model, sales_model, growth_needs):
        self.revenue = revenue
        self.stage = stage.lower()
        self.model = model
        self.sales_model = sales_model
        self.growth_needs = growth_needs.lower()

    def get(self):
        stage_table = {
            'launch': 2.50,
            'growth': 1.75,
            'shake-out': 1.40,
            'maturity': 1.00,
            'decline / recession': .8
        }
        tag_table = {
            'B2B - product': 1.26,
            'B2B - services': 1.38,
            'B2C - product': 1.92,
            'B2C - services': 2.36
        }
        sales_table = {
            'ecommerce': 4,
            'saas': 8,
            'other': 1
        }
        growth_needs_table = {
            'low': .5,
            'medium': 1,
            'high': 2
        }
        
        base = .05
        sales_multiplier = 2 if self.sales_model != 'other' else 1
        avg = (stage_table.get(self.stage) + (sales_table.get(self.sales_model) * sales_multiplier) + tag_table.get(self.model)) / 3 + (growth_needs_table.get(self.growth_needs) - 1)
        formula = self.revenue * base * avg / 12
        return formula



class SpendAllocation:
    def __init__(self, customer_id, revenue, budget, brand_strength, growth_needs, competitiveness, biz_type, biz_model):
        self.customer_id = customer_id
        self.revenue = revenue
        self.budget = budget
        self.brand_strength = brand_strength
        self.growth_needs = growth_needs
        self.competitiveness = competitiveness
        self.biz_type = biz_type
        self.biz_model = biz_model
    
        self.base_mix = {
            'awareness': .55,
            'evaluation': .25,
            'conversion': .2
        }

        if self.growth_needs or self.competitiveness or self.brand_strength:
            self.update_considerations()

    def update_considerations(self):
        query = "UPDATE customer_basic SET brand_strength = ?, growth_needs = ?, competitiveness = ? WHERE id = ?"
        db.execute(query, False, (self.brand_strength, self.growth_needs, self.competitiveness, self.customer_id), commit=True)

    def adjustments(self):
        adjustments = {}
        considerations = ['brand_strength', 'growth_needs', 'competitiveness']
        levels = ['low', 'medium', 'high']
        stages = ['awareness', 'evaluation', 'conversion']
        
        brand_values = [
            [.1, -.05, -.05],
            [0,0,0],
            [-.1, .05, .05]
        ]
        growth_values = [
            [-.1, .03, .07],
            [0,0,0],
            [.07, -.04, -.03]
        ]
        competitiveness_values = [
            [-.1, .03, .07],
            [0,0,0],
            [0, .05, -.05]
        ]
        
        def pack_values():
            for consideration in enumerate(considerations):
                adjustments[consideration[1]] = {}
                for level in enumerate(levels):
                    adjustments[consideration[1]][level[1]] = {}
                    for stage in enumerate(stages):
                        if consideration[1] == 'brand_strength':
                            lookup = brand_values[level[0]][stage[0]]
                        elif consideration[1] == 'growth_needs':
                            lookup = growth_values[level[0]][stage[0]]
                        elif consideration[1] == 'competitiveness':
                            lookup = competitiveness_values[level[0]][stage[0]]
                        
                        adjustments[consideration[1]][level[1]][stage[1]] = lookup
                    
        pack_values()
                    
        awareness = (
            adjustments['brand_strength'][self.brand_strength]['awareness']
            + adjustments['growth_needs'][self.growth_needs]['awareness']
            + adjustments['competitiveness'][self.competitiveness]['awareness']
        )
        evaluation = (
            adjustments['brand_strength'][self.brand_strength]['evaluation']
            + adjustments['growth_needs'][self.growth_needs]['evaluation']
            + adjustments['competitiveness'][self.competitiveness]['evaluation']
        )
        conversion = (
            adjustments['brand_strength'][self.brand_strength]['conversion']
            + adjustments['growth_needs'][self.growth_needs]['conversion']
            + adjustments['competitiveness'][self.competitiveness]['conversion']
        )
        return awareness, evaluation, conversion
        
    def num_tactics(self):
        if self.budget <= 1000:
            tactics = 2
            campaigns = 3
        elif self.budget > 1000 and self.budget <= 2000:
            tactics = 3
            campaigns = 4
        elif self.budget > 2000 and self.budget <= 3500:
            tactics = 3
            campaigns = 5
        elif self.budget > 3500 and self.budget <= 5500:
            tactics = 3
            campaigns = 6
        elif self.budget > 5500 and self.budget <= 10000:
            tactics = 4
            campaigns = 9
        elif self.budget > 10000:
            tactics = 5
            campaigns = 12
            
        return math.floor(tactics), math.floor(campaigns)

    def get_tags(self):
        # db = db_obj()
        tags_db, cursor = db.execute("exec get_spend_tags @customer_id = ?", True, (self.customer_id,))
        tags_db = cursor.fetchall()
        cursor.close()
        tags = []
        for tag in tags_db:
            tags.append({
                'tag': tag[0],
                'tactic': tag[1],
                'bucket': tag[2],
                'priority_scale': tag[3]
            })

        return pd.DataFrame(tags).sort_values(by=['priority_scale'], ascending=False)

    def allocation(self):
        num_tactics, num_campaigns = self.num_tactics()
        tags = self.get_tags()
        df = tags[:num_tactics]
        priority_sum = df['priority_scale'].sum()
        df['spend_per_tactic'] = self.budget * df['priority_scale'] / priority_sum
        df['spend_percent'] = df['spend_per_tactic'] / self.budget
        df = df.fillna(0)
        df['num_campaigns'] = (df['spend_percent'] * num_campaigns).apply(lambda x: 1 if x < 1 else math.floor(x))

        return df.to_json(orient='records')
    
    def campaign_allocation(self):
        buckets = json.loads(self.allocation())
        campaigns = [{
                'bucket': 'search',
                'biz_type': ['all'],
                'campaigns': [
                    'Activity-based',
                    'Product / service',
                    'Your brand(s)',
                    'Landing page a/b testing campaign'
            ]}, {
                'bucket': 'social',
                'biz_type': ['b2b'],
                'campaigns': [
                    'LinkedIn role-focused',
                    'LinkedIn retargeting display',
                    'LinkedIn career-focused targeting',
                    'Complimentary product targeting',
                    'Facebook retargeting campaign',
                    'Facebook awareness video campaign',
                    'Youtube awareness video campaign',
                    'Landing page a/b testing campaign'
            ]},  {
                'bucket': 'social',
                'biz_type': ['b2c'],
                'campaigns': [
                    'Facebook demographic targeting',
                    'Facebook retargeting display',
                    'Youtube awareness video campaign',
                    'Youtube retargeting campaign',
                    'Instagram awareness campaign'
            ]},  {
                'bucket': 'seo',
                'biz_type': ['all'],
                'campaigns': [
                    'Primary issue(s) + solution content',
                    'Lead magnet content',
                    'Long-tail keyword content'
            ]},  {
                'bucket': 'outbound email',
                'biz_type': ['all'],
                'campaigns': [
                    'Lead nurturing drip',
                    'Inactive customer campaign'
            ]}, {
                'bucket': 'display networks',
                'biz_type': ['all'],
                'campaigns': [
                    'Display Retargeting',
                    'Demographic targeting',
                    'Keyword-based awareness campaign',
                    'Landing page retargeting campaign',
                    'Landing page a/b testing campaign'
            ]}]
        
        
        def added_campaigns(campaign_list, bucket_name):
            def add(added, campaign_list=campaign_list):
                return campaign_list.append(added)
            
            if self.budget > 1000:
                if self.competitiveness in ['high', 'medium']:
                    if bucket_name == 'search':
                        add('Direct competitor brand(s)')
                
                if self.biz_type == 'b2b':
                    if bucket_name == 'search':
                        add('Industry keywords')
                    
                if self.brand_strength == 'low' and self.biz_type == 'b2c':
                    if bucket_name == 'social':
                        add('Additional Facebook Display Campaign')
                    
                if self.brand_strength == 'low' and self.biz_type == 'b2b':
                    if bucket_name == 'social':
                        add('Additional LinkedIn Display Campaign')
                if self.brand_strength in ['high', 'medium']:
                    if bucket_name == 'search':
                        add('Branded search campaign')
                    
            return campaign_list

        allocation = list()
        
        for bucket in buckets:
            num_campaigns = bucket['num_campaigns']
            bucket_name = bucket['bucket'].lower()
            sets = [campaign for campaign in campaigns if campaign['bucket'] == bucket_name]

            for set in sets:
                if self.biz_type.lower() in set.get('biz_type') or set.get('biz_type')[0] == 'all':
                    campaignset = added_campaigns(set.get('campaigns')[:num_campaigns], bucket_name)
                    allocation.append({
                        'bucket': bucket_name,
                        'spend': bucket['spend_per_tactic'],
                        'spend_percent': bucket['spend_percent'],
                        'num_campaigns': len(campaignset),
                        'campaigns': campaignset
                    }) 

        
                    
        return json.dumps(allocation)
        