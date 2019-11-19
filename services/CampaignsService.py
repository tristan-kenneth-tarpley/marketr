import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from app import app

class CampaignData:
    def __init__(self):
        app.config.from_pyfile('config.cfg')
        username = app.config['POSTGRES_USERNAME']
        password = app.config['POSTGRES_PASSWORD']
        address = app.config['POSTGRES_ADDRESS']
        port = app.config['POSTGRES_PORT']
        name = app.config['POSTGRES_DBNAME']
        postgres_str = f'postgresql://{username}:{password}@{address}:{port}/{name}'
        self.cnx = create_engine(postgres_str)

    