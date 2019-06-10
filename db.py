import pandas as pd
import pyodbc
import time

server = 'tarpley.database.windows.net'
database = 'marketr'
username = 'tristan'
password = 'Fiverrtemp!'
driver= '{ODBC Driver 17 for SQL Server}'

connStr = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
try:
	db = pyodbc.connect(connStr)
except:
	print('uh oh')

def sql_to_df(x):
    return pd.read_sql_query(x, db, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

def execute(query, returned):
	cursor = db.cursor()
	retry_flag = True
	retry_count = 0
	while retry_flag and retry_count < 5:
		try:
			if returned == True:
				cursor.execute(query)
				data = cursor.execute(query)
				retry_flag = False
				return data, cursor
			else:
				cursor.execute(query)
				cursor.close()
				retry_flag = False

		except:
			retry_count = retry_count + 1
			time.sleep(1)