class GetRec:
    def __init__(self, revenue, stage, model):
        clean_rev = float(revenue.replace(',', '')) if revenue else 0
        self.revenue = clean_rev if clean_rev > 99999 else 100000
        self.stage = stage
        self.model = model

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