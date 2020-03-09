import pandas as pd
import numpy as np
import json
from services.BigQuery import GoogleORM
import asyncio
import data.db as db

def compile_data_view(run_social: bool=False, run_search: bool=True, company_name: str=None, date_range: int=30, demo: bool=False, ltv: float=None):
    orm = GoogleORM(company_name)
    if not demo:
        async def dataframes(run_social, run_search):
            if run_search:
                search_df = loop.run_in_executor(None, orm.search_index, date_range)
                search = await search_df
                _opportunities = loop.run_in_executor(None, orm.keywords)
                opps = await _opportunities
            else:
                search_df = None
                search = None
                opps = None

            if run_social:
                social_df = loop.run_in_executor(None, orm.social_index, date_range)
                social = await social_df
            else:
                social_df = None
                social = None

            return search, social, opps

        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        search_df, social_df, opps = loop.run_until_complete(dataframes(run_social, run_search))

    else:
        ltv = 5000
        search_df = db.sql_to_df(f"SELECT * FROM demo_data_search where datediff(day, date_start, getdate()) < {date_range}")
        social_df = db.sql_to_df(f"SELECT * FROM demo_data_social where datediff(day, date_start, getdate())  < {date_range}")
        opps = orm.keywords()

    return {
        'search_df': search_df,
        'social_df': social_df,
        'topic_opps': opps
    }

    
