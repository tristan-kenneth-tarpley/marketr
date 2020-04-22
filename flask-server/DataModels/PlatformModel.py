import pandas as pd

class PlatformModel:
    def __init__(self, df=None, start_range=None, end_range=None, qualifications:dict=None, filters:dict=None) -> None:
        self.raw_df = df
        self.df = df
        self.filters = filters
        self.qualifications = qualifications
      
    def qualify(self, df) -> dict:
        for qual in self.qualifications:
            for expression in self.qualifications[qual]:
                df = df[expression(qual, df)]
                
        return df  
    
    def get(self):
        return self.df