from app import app
import time
import datetime
import zipcodes
from db import db, sql_to_df

def last_modified(user):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    query = """UPDATE dbo.customer_basic
                SET last_modified = '""" + st + """'
                WHERE dbo.customer_basic.id = '""" + user + """';commit;"""

    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()


def clean_for_display(df):

	def rename(old, new):
		df.rename(columns = {old: new}, inplace=True)

	def cycle_through():
	    for key, value in df.iteritems():
	        if key == "ID":
	            rename("ID", "Customer ID")

	        elif key == "perc_complete":
	            rename("perc_complete", "% of onboarding completed")

	        elif key == "zip":
	        	rename("zip", "Zip Code")

	        elif key.find("_") > 0: # if an underscore is found
	            newkey = key.replace("_"," ") # convert underscores to space's
	            df.rename(columns = {key: newkey}, inplace=True)

	    return df

	return cycle_through()



def load_past_inputs(page):
	print('hi')


	# load values
	# check if complete
	# pass values to javascript and cycle through elements while populating || adding class
















    