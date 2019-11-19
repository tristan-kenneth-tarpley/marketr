import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from app import app

class CampaignData:
    def __init__(self):
        app.config.from_pyfile('config.cfg')
        postgres_str = f'postgresql://{app.config['POSTGRES_USERNAME']}:{app.config['POSTGRES_PASSWORD']}@{app.config['POSTGRES_ADDRESS']}:{app.config['POSTGRES_PORT']}/{app.config['POSTGRES_DBNAME']}'
        self.cnx = create_engine(postgres_str)

    