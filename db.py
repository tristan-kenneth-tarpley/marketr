import pandas as pd
import pyodbc

server = 'tarpley.database.windows.net'
database = 'marketr'
username = 'tristan'
password = 'Fiverrtemp!'
driver= '{ODBC Driver 17 for SQL Server}'

connStr = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
db = pyodbc.connect(connStr)

def sql_to_df(x):
    return pd.read_sql_query(x, db, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)