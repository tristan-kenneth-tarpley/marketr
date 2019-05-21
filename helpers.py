from main import app
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