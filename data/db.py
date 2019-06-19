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
except pyodbc.Error as ex:
    # sqlstate = ex.args[0]
    # if sqlstate == '08001':
    #     pass
    print("DB didn't connect")
    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count <5:
    	try:
    		del db
    		db = pyodbc.connect(connStr)
    		try_flag = False
    	except:
    		retry_count = retry_count + 1
    		time.sleep(1)

def sql_to_df(x):
	retry_flag = True
	retry_count = 0
	while retry_flag and retry_count <5:
		if retry_count == 4:
			return "can you try again, please?"
		try:
			retry_flag = False
			return pd.read_sql_query(x, db, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)
		except:
			retry_count = retry_count + 1
			time.sleep(1)


def execute(query, returned, tup):

	cursor = db.cursor()
	debug_query = query.replace("?", "%s")
	# debug_query = query % tup
	retry_flag = True
	retry_count = 0
	while retry_flag and retry_count < 5:
		if retry_count == 4:
			return "Can you try again, please?"

		try:
			if returned == True:
				cursor.execute(query, tup)
				data = cursor.execute(query, tup)
				retry_flag = False
				return data, cursor
			else:
				cursor.execute(query, tup)
				cursor.close()
				retry_flag = False

		except AssertionError:
		# except:
			retry_count = retry_count + 1
			time.sleep(1)


