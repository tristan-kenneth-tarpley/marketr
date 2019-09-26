import pandas as pd
import pyodbc
import time
from passlib.hash import sha256_crypt
from app import app

app.config.from_pyfile('config.cfg')

DB_SERVER = app.config['DB_SERVER']
DATABASE = app.config['DATABASE']
USERNAME = app.config['USERNAME']
DB_PASSWORD = app.config['DB_PASSWORD']
DRIVER= app.config['DB_DRIVER']

connStr = 'DRIVER='+DRIVER+';SERVER='+DB_SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ DB_PASSWORD


def init_db():
	try:
		db = pyodbc.connect(connStr)
		return db
	except pyodbc.OperationalError as ex:
	    print("DB didn't connect")
	    retry_flag = True
	    retry_count = 0
	    while retry_flag and retry_count <5:
	    	try:
	    		del db
	    		db = pyodbc.connect(connStr)
	    		try_flag = False
	    		return db
	    	except:
	    		retry_count = retry_count + 1
	    		time.sleep(1)


def execute(query, returned, tup, commit=False):

	db = init_db()

	cursor = db.cursor()
	cursor.commit()
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

	if commit == True:
		db.commit()

		

def sql_to_df(x):
	retry_flag = True
	retry_count = 0
	db = init_db()
	while retry_flag and retry_count <5:
		if retry_count == 4:
			return False
		try:	
			return pd.read_sql_query(x, db, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)
			retry_flag = False 
		except:
			retry_count = retry_count + 1
			time.sleep(1)




		

	# def update_password(oldpassword, newpassword)









