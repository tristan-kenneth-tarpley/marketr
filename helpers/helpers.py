from app import app, session
import time
import datetime
import zipcodes
from data.db import *
import pandas as pd
import math



def intake_page_map():
    pages = {
            0: 'begin',
            1: 'competitors',
            2: 'company',
            3: 'audience',
            4: 'product',
            5: 'product_2',
            6: 'salescycle',
            7: 'goals',
            8: 'history',
            9: 'platforms',
            10: 'past',
            11: 'home'
            }

    return pages


def test_query(query, tup):
    test_query = query.replace("?", "%s")
    test_query = test_query % tup

    return test_query

def dirty_mask_handler(hides, biz_model, ind):
    for row in hides:
        if row[0] == ind:
            if row[2] == biz_model:
                return True
    return False

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
        return True
    else:
        return False


def perc_complete(page, user):
    pages = intake_page_map()

    def get_perc(target_page):
        for step in pages:
            if step == target_page:
                return math.ceil(int((pages.index(step) + 1)/len(pages) * 100))

    perc = get_perc(page)
    tup = (perc, user)
    query = """UPDATE dbo.customer_basic SET perc_complete = ? WHERE id = ?;commit;"""
    execute(query, False, tup)

def load_last_page(user):
    pages = intake_page_map()
    tup = (user,)
    data, cursor = execute('SELECT perc_complete FROM customer_basic WHERE id = ?', True, tup)
    data = cursor.fetchall()
    data = int(data[0][0])
    data = int(data/(len(pages)-1))
    cursor.close()
    return pages[data]




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




    