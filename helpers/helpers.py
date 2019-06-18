from app import app, session
import time
import datetime
import zipcodes
from data.db import db, sql_to_df, execute
import pandas as pd

def validate_login(username, password):
    print('hi')

def get_trigger_val(val, table, user):
    tup = (user,)
    query = "SELECT %s FROM dbo.%s WHERE customer_id = ?" % (val, table)
    data, cursor = execute(query, True, tup)
    data = cursor.fetchone()
    data = data[0]
    cursor.close()
    
    return data
    
def get_biz_model(user):
    x = get_trigger_val("biz_model", "company", user)
    return x

def get_num_products(user):
    tup  = (user,)
    query = """SELECT COUNT(p_id)
                FROM dbo.product_list
                WHERE customer_id = ?"""
    data, cursor = execute(query, True, tup)
    data = cursor.fetchone()
    data = data[0]
    cursor.close()
    return data
    
def get_selling_to(user):
    x = get_trigger_val("selling_to", "company", user)
    return x


def update_for_home(query, user, tup):
    print('hi')


def last_modified(user):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    tup = (st, user)
    query = """UPDATE dbo.customer_basic
                SET last_modified = ?
                WHERE dbo.customer_basic.id = ?;commit;"""

    execute(query, False, tup)


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

            elif key == "biz_model":
                rename("biz_model", "Business Model")
            elif key == "rev_channel_freeform":
                rename("rev_channel_freeform", "Revenue Channels Notes")
            elif key == "storefront_perc":
                rename("storefront_perc", "% of revenue from storefront")
            elif key == "direct_perc":
                rename("direct_perc", "% of revenue from direct")
            elif key == "online_perc":
                rename("online_perc", "% of revenue from online")
            elif key == "tradeshows_perc":
                rename("tradeshows_perc", "% of revenue from tradeshows")
            elif key == "other_perc":
                rename("other_perc", "% of revenue from other channels")

            elif key.find("_") > 0: # if an underscore is found
                newkey = key.replace("_"," ") # convert underscores to space's
                df.rename(columns = {key: newkey}, inplace=True)

        return df

    return cycle_through()



def is_started(table, user):
    tup = (user,)
    query = "SELECT * FROM dbo.%s WHERE customer_id = ?" % (table,)
    data, cursor = execute(query, True, tup)
    data = cursor.fetchall()
    cursor.close()
    
    if len(data) > 0:
        print(data)
        print(len(data))
        return True
    else:
        return False


def load_last_page(user):
    steps = {'competitors': 'competitors',
             'company': 'company',
             'audience': 'audience',
             'product': 'product',
             'product_list': 'product_2',
             'awareness': 'salescycle',
             'goals': 'goals',
             'history': 'history',
             'platforms': 'platforms',
             'history_2': 'past',
             'the end': 'home'}
    
    def call_it(name):
        return steps[name]

    i = 0

    for step in steps:
        if step != 'the end':
            if step == "history_2":
                query = "SELECT history_freeform FROM dbo.history WHERE customer_id = %d" % (user,)
                def_query = sql_to_df(query)
            else:
                query = "SELECT customer_id FROM %s WHERE customer_id = %d" % (step, user)
                def_query = sql_to_df(query)
            i+=1
            if def_query.empty == True:
                perc_complete = str(i*10)
                tup = (perc_complete, user)
                query = """UPDATE dbo.customer_basic SET perc_complete = ? WHERE id = ?;commit;"""
                execute(query, False, tup)
                if step == "product":
                    return call_it(step)
                else:
                    print(step)
                    return call_it(step)
            else:
                return 'home'



def past_inputs(page, user, persona_id):
    intake_pages = ['begin', 'competitors', 'company', 'competitors', 'audience', 'product', 'product_2', 'salescycle', 'goals', 'history', 'platforms', 'past', 'creative']
    if page in intake_pages:
        if page == 'begin':
            query = "SELECT first_name, last_name, company_name, revenue, employees, zip, stage FROM dbo.customer_basic WHERE ID = %s" % (user,)
            result = sql_to_df(query)
        elif page == 'salescycle':
            awareness = sql_to_df("select * from dbo.awareness WHERE customer_id=%d" % (user,))
            awareness.insert(loc=0, column='stage', value='awareness')

            evaluation = sql_to_df("select * from dbo.evaluation WHERE customer_id=%d" % (user,))
            evaluation.insert(loc=0, column='stage', value='evaluation')

            conversion = sql_to_df("select * from dbo.conversion WHERE customer_id=%d" % (user,))
            conversion.insert(loc=0, column='stage', value='conversion')

            retention = sql_to_df("select * from dbo.retention WHERE customer_id=%d" % (user,))
            retention.insert(loc=0, column='stage', value='retention')

            referral = sql_to_df("select * from dbo.referral WHERE customer_id=%d" % (user,))
            referral.insert(loc=0, column='stage', value='referral')
            stages = [awareness, evaluation, conversion, retention, referral]

            result = pd.concat(stages)

        
        elif page == 'audience':
            query = "SELECT * FROM dbo.audience WHERE customer_id = %s and audience_id = %d" % (user, persona_id)
            result = sql_to_df(query)


        elif page == 'product_2':
            query = "SELECT * FROM dbo.product_list WHERE customer_id = %d" % (user,)
            result = sql_to_df(query)
        elif page == 'past':
            query = "SELECT history_freeform FROM dbo.history WHERE customer_id = %d" % (user,)
            result = sql_to_df(query)
        elif page == 'creative':
            result = 'nah'
        elif page == 'splash':
            result = 'nah'
        else:
            query = "SELECT * FROM dbo.%s WHERE customer_id = %d" % (page, user)
            result = sql_to_df(query)
    else:
        result = 'nah'

    return result




def init_audience(user):
    tup = (user,)
    first_query = """INSERT INTO dbo.audience
          (customer_id)
          VALUES(?);commit;"""

    execute(first_query, False, tup)


def clean_audience(user):
    load_company = sql_to_df("""SELECT * FROM dbo.audience WHERE customer_id = %d""" % (user,))
    if len(load_company) > 0:
        ages_dict = {}
        ages = ['age_group_1','age_group_2','age_group_3','age_group_4','age_group_5','age_group_6','age_group_7','age_group_8']
        before_dict = {}
        before = ['before_1','before_2','before_3','before_4','before_5','before_6','before_7','before_8','before_9','before_10','before_freeform']
        after_dict = {}
        after = ['after_1','after_2','after_3','after_4','after_5','after_6','after_7','after_8','after_9','after_10', 'after_freeform']

        keys = ['ages', 'before', 'after']
        
        if len(load_company) > 1:
            t = 0
            temp = []

            while t<len(load_company):
                temp.append(t)
                t+=1

            i = 0 
            audiences_dict = dict.fromkeys(temp)

            x=0
            while x<len(load_company):
                audiences_dict[x] = {'ages':None, 'before':None, 'after':None}
                x += 1 



            while i < len(load_company):
                for key, value in load_company.iloc[i].iteritems():
                    if value != '':
                        if key in ages:
                            ages_dict[key] = value
                        elif key in before:
                            before_dict[key] = value
                        elif key in after:
                            after_dict[key] = value


                audiences_dict[i]['ages'] = list(ages_dict.values())
                audiences_dict[i]['before'] = list(before_dict.values())
                audiences_dict[i]['after'] = list(after_dict.values())
                i += 1

                
        else:
            temp = [0]
            audiences_dict = dict.fromkeys(temp)
            for key, value in load_company.iloc[0].iteritems():
                if value != '':
                    if key in ages:
                        ages_dict[key] = value
                    elif key in before:
                        before_dict[key] = value
                    elif key in after:
                        after_dict[key] = value
            audiences_dict[0] = {'after': after_dict, 'ages': ages_dict, 'before': before_dict}
                
        return audiences_dict
    else:
        return False

def clean_product(user):
    load_company = sql_to_df("""SELECT * FROM dbo.product WHERE customer_id = %d""" % (user,))
    
    if len(load_company) > 0:
        segment_dict = {}
        segments = ['segment_1', 'segment_2', 'segment_3', 'segment_4', 'segment_5', 'segment_6', 'segment_7', 'segment_8', 'segment_9', 'segment_10']
        
        source_dict = {}
        sources = ['source_1','source_2','source_3','source_4']

        temp = [0]
        product_dict = dict.fromkeys(temp)
        for key, value in load_company.iloc[0].iteritems():
            if value != '':
                if key in segments:
                    segment_dict[key] = value
                elif key in sources:
                    source_dict[key] = value
            product_dict[0] = {'segment': list(segment_dict.values()), 'sources': list(source_dict.values())}
                
        return product_dict
    else:
        return False



    