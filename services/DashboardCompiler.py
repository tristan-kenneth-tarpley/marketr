import pandas as pd
import numpy as np
import json
from services.BigQuery import GoogleORM
import asyncio
import data.db as db

def compile_data_view(run_social: bool=False, run_search: bool=True, company_name: str=None, start_date: str=None, end_date: str=None, demo: bool=False, ltv: float=None, get_opps: bool=True):
    orm = GoogleORM(company_name)
    if not demo:
        async def dataframes(run_social, run_search):
            if run_search:
                search_df = loop.run_in_executor(None, orm.search_index, start_date, end_date)
                search = await search_df
                if get_opps:
                    _opportunities = loop.run_in_executor(None, orm.keywords)
                    opps = await _opportunities
                else:
                    opps = None
 
            else:
                search_df = None
                search = None
                opps = None

            if run_social:
                social_df = loop.run_in_executor(None, orm.social_index, start_date, end_date)
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
        new_start = start_date.replace(" UTC", ".000")
        new_end = end_date.replace(" UTC", ".000")

        search_query = f"SELECT * FROM demo_data_search where date_start between '{new_start}' and '{new_end}'"
        social_query = f"SELECT * FROM demo_data_social where date_start between '{new_start}' and '{new_end}'"
        search_df = db.sql_to_df(search_query)
        social_df = db.sql_to_df(social_query)
        opps = orm.keywords()


    return {
        'search_df': search_df,
        'social_df': social_df,
        'topic_opps': opps
    }

    
