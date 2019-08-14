import pandas as pd
from DataModels.PlatformModel import PlatformModel
import data.db as db

class ab_test(PlatformModel):
    def __init__(self, df, start_range=None, end_range=None) -> None:
        self.filters = {

        }
        self.qualifications = {
            'views a': [
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
#         self.df = self.qualify(df)

    def clean(self, df):
        df['Conversion rate a'].replace({'%':''}, regex=True, inplace=True)
        df['Conversion rate b'].replace({'%':''}, regex=True, inplace=True)
        df['Conversion rate a'] = df['Conversion rate a'].astype('float')
        df['Conversion rate b'] = df['Conversion rate b'].astype('float')
        
        df['best_conversion'] = df[['Conversion rate a', 'Conversion rate b']].max(axis=1)
        df['worst_conversion'] = df[['Conversion rate a', 'Conversion rate b']].min(axis=1)
        
        def best_views(row):
            if row['Conversion rate a'] == row['best_conversion']:
                val = row['views a']
            elif row['Conversion rate b'] == row['best_conversion']:
                val = row['views b']
            return val
        
        def worst_views(row):
            if row['Conversion rate a'] == row['worst_conversion']:
                val = row['views a']
            elif row['Conversion rate b'] == row['worst_conversion']:
                val = row['views b']
            return val
        
        def best_variant(row):
            if row['Conversion rate a'] == row['best_conversion']:
                val = row['Test A']
            elif row['Conversion rate b'] == row['best_conversion']:
                val = row['Test B']
            return val
        def worst_variant(row):
            if row['Conversion rate a'] == row['worst_conversion']:
                val = row['Test A']
            elif row['Conversion rate b'] == row['worst_conversion']:
                val = row['Test B']
            return val

        df['best_variant'] = df.apply(best_variant, axis=1)
        df['worst_variant'] = df.apply(worst_variant, axis=1)
        df['best_views'] = df.apply(best_views, axis=1)
        df['worst_views'] = df.apply(worst_views, axis=1)
        df['views a'] = df['views a'].astype('int64')
        df['views b'] = df['views b'].astype('int64')
        
        
    def packJSON(self):
        def get_struct(df):
            struct = {
                'hypothesis': df['Hypothesis'],
                'best': {
                    'conversion': df['best_conversion'],
                    'views': df['best_views'],
                    'variant': df['best_variant']
                },
                'worst': {
                    'conversion': df['worst_conversion'],
                    'views': df['worst_views'],
                    'variant': df['worst_variant']
                }
            }
            return struct
        
        return_data = {}
        index = 0
        for key, val in self.df.iterrows():
            return_data[index] = get_struct(val)
            index += 1
        
        return return_data

    def save(self, customer_id):
        struct = self.packJSON()
        for s in struct:
            best_tup = [
                struct[s]['best']['variant'],
                struct[s]['best']['views'],
                struct[s]['best']['conversion'],
                customer_id,
                1,
                struct[s]['hypothesis'],
                self.start_range,
                self.end_range
            ]
            best_query = """
                    EXEC store_test_upload
                    @variant = ?, @views = ?, @conversion = ?,
                    @customer_id = ?, @best_worst_binary = ?, @hypothesis = ?,
                    @start_date = ?, @end_date = ?
                    """

            worst_tup = [
                struct[s]['worst']['variant'],
                struct[s]['worst']['views'],
                struct[s]['worst']['conversion'],
                customer_id,
                0,
                struct[s]['hypothesis'],
                self.start_range,
                self.end_range
            ]
            worst_query = """
                    EXEC store_test_upload
                    @variant = ?, @views = ?, @conversion = ?,
                    @customer_id = ?, @best_worst_binary = ?, @hypothesis = ?,
                    @start_date = ?, @end_date = ?
                    """

            query = f"{best_query} {worst_query}"

            db.execute(query, False, tuple(best_tup + worst_tup), commit=True)