import math
import data.db as db
import pandas as pd

class GetRec:
    def __init__(self, revenue, stage, model):
        self.revenue = revenue if revenue > 99999 else 100000
        self.stage = stage
        self.model = model
        print(self.revenue)
        print(self.stage)
        print(self.model)

    def get(self):
        table_1 = {
            'Launch': 2.00,
            'Growth': 1.60,
            'Shake-out': 1.40,
            'Maturity': 1.00,
            'Decline / Recession': .8
        }
        table_2 = {
            'B2B - product': 1.72,
            'B2B - services': 1.74,
            'B2C - product': 1.96,
            'B2C - services': 3.12
        }
        base = .05
        avg = (table_1.get(self.stage) + table_2.get(self.model)) / 2

        formula = self.revenue * base * avg /12
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
            tactics = 3
        elif self.budget > 1000 and self.budget <= 3000:
            tactics = 4
        elif self.budget > 3000 and self.budget <= 5000:
            tactics = 6
        elif self.budget > 5000 and self.budget <= 10000:
            tactics = 8
        elif self.budget > 10000:
            tactics = 10
            
        return math.floor(tactics)

    def get_tags(self):
        tags_db, cursor = db.execute("exec get_spend_tags @customer_id = ?", True, (self.customer_id,))
        tags_db = cursor.fetchall()
        cursor.close()
        tags = []
        for tag in tags_db:
            tags.append({
                'tag': tag[0],
                'tactic': tag[1],
                'category': tag[2],
                'priority_scale': tag[3]
            })

        return pd.DataFrame(tags).sort_values(by=['priority_scale'], ascending=False)

    def allocation(self):
        base_table = self.base_mix
        awareness_adj, evaluation_adj, conversion_adj = self.adjustments()
        
        awareness, evaluation, conversion = (
            (base_table['awareness'] + awareness_adj),
            (base_table['evaluation'] + evaluation_adj),
            (base_table['conversion'] + conversion_adj)
        )
        awareness_spend, evaluation_spend, conversion_spend = (
            awareness * self.budget,
            evaluation * self.budget,
            conversion * self.budget
        )
        
        tactics = self.num_tactics()
        awareness_tactics, evaluation_tactics, conversion_tactics = (
            math.floor(base_table['awareness'] * tactics),
            round(base_table['evaluation'] * tactics),
            round(base_table['conversion'] * tactics)
        )
        
        tags = self.get_tags()
        awareness = tags[tags['category'] == 'Awareness'][:awareness_tactics]
        evaluation = tags[tags['category'] == 'Evaluation'][:evaluation_tactics]
        conversion = tags[tags['category'] == 'Conversion'][:conversion_tactics]
        
        def tactic_spend(priority, cat_spend, sum):
            return round(cat_spend*priority/sum)
        
        for tup in [(awareness, awareness_spend), (evaluation, evaluation_spend), (conversion, conversion_spend)]:
            df = tup[0]
            spend = tup[1]
            df['spend_per_tactic'] = df['priority_scale'].apply(
                lambda x: tactic_spend(x, spend, df['priority_scale'].sum())
            )

        return (awareness.to_json(orient='records'), evaluation.to_json(orient='records'), conversion.to_json(orient='records'))
