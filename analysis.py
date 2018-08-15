
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import pyodbc
import json
import colors
from urllib.error import HTTPError
from time import time, sleep
from watson_developer_cloud import ToneAnalyzerV3
from itertools import product


# In[3]:


server = 'tarpley.database.windows.net'
database = 'marketr'
username = 'tristan'
password = 'Fiverrtemp!'
driver= '{ODBC Driver 13 for SQL Server}'

connStr = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
db = pyodbc.connect(connStr)
cursor = db.cursor()


# In[4]:


def sql_to_df(x):
    return pd.read_sql_query(x, db, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

def get_customers():
    query = "SELECT * FROM dbo.customers"
    a = sql_to_df(query)
    return a

def debug(strSQL):
    print(strSQL)


# In[5]:


vision_subscription_key = '8359f1b134914ab1a1137c5a1d9d547c'
assert vision_subscription_key

text_subscription_key = '45f31e1a295e414b8d71319b79a405e0'
assert text_subscription_key

vision_base_url = "https://southcentralus.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"
image_url = 'https://images.wagwalkingweb.com/media/breed/dachshund/appearance/dachshund.png?auto=compress&fit=max'

vision_headers  = {'Ocp-Apim-Subscription-Key': vision_subscription_key }
vision_params   = {'visualFeatures': 'Categories,Description,Color'}


# In[7]:


def img_attr_to_memory():
    image_attr_query = "select * from dbo.image_attributes as dboi"
    image_attr_df = sql_to_df(image_attr_query)
    image_attr_df = image_attr_df.drop_duplicates(subset=['image_hash'], keep='last')
    
    return image_attr_df


# In[8]:


image_attr_df = img_attr_to_memory()


# In[9]:


def get_img_attr(img, row_select):
    vision_data     = {'url': img}
    try:
        vision_response = requests.post(vision_analyze_url, headers=vision_headers, params=vision_params, json=vision_data)
        vision_response.raise_for_status()

        analysis = vision_response.json()

        accent_color = analysis['color']['accentColor']
        dom_color_back = analysis['color']['dominantColorBackground']
        dom_color_fore = analysis['color']['dominantColorForeground']

        is_bw = analysis['color']['isBwImg']

        height = analysis['metadata']['height']
        width = analysis['metadata']['width']  

        try:
            confidence = analysis['description']['captions'][0]['confidence']
            caption = analysis['description']['captions'][0]['text']
            tags_1 = analysis['description']['tags'][0]
            dom_colors_1 = analysis['color']['dominantColors'][0]

            update_statement = """UPDATE dbo.image_attributes 
                                    SET accent_color = '""" + str(accent_color) + """',
                                    dominant_color_background = '""" + dom_color_back + """',
                                    dominant_color_foreground = '""" + dom_color_fore + """',
                                    dominant_color_1 = '""" + dom_colors_1 + """',
                                    is_bw_img = '""" + str(is_bw) + """',
                                    tags_1 = '""" + tags_1 + """',
                                    caption = '""" + caption + """',
                                    confidence = """ + str(confidence) + """,
                                    height = """ + str(height) + """,
                                    width = """ + str(width) + """
                                    WHERE id='""" + row_select + """';
                                  commit;"""

        except IndexError:
            try:
                #without tags
                confidence = analysis['description']['captions'][0]['confidence']
                caption = analysis['description']['captions'][0]['text']

                dom_colors_1 = analysis['color']['dominantColors'][0]

                update_statement = """UPDATE dbo.image_attributes 
                                        SET accent_color = '""" + str(accent_color) + """',
                                            dominant_color_background = '""" + dom_color_back + """',
                                            dominant_color_foreground = '""" + dom_color_fore + """',
                                            dominant_color_1 = '""" + dom_colors_1 + """',
                                            is_bw_img = '""" + str(is_bw) + """',
                                            caption = '""" + caption + """',
                                            confidence = """ + str(confidence) + """,
                                            height = """ + str(height) + """,
                                            width = """ + str(width) + """
                                            WHERE id='""" + row_select + """';
                                      commit;"""

            except IndexError:
                try:
                    #without caption, add tags
                    confidence = analysis['description']['captions'][0]['confidence']
                    tags_1 = analysis['description']['tags'][0]     
                    dom_colors_1 = analysis['color']['dominantColors'][0]

                    update_statement = """UPDATE dbo.image_attributes 
                                            SET accent_color = '""" + str(accent_color) + """',
                                                dominant_color_background = '""" + dom_color_back + """',
                                                dominant_color_foreground = '""" + dom_color_fore + """',
                                                dominant_color_1 = '""" + dom_colors_1 + """',
                                                is_bw_img = '""" + str(is_bw) + """',
                                                tags_1 = '""" + tags_1 + """',
                                                confidence = """ + str(confidence) + """,
                                                height = """ + str(height) + """,
                                                width = """ + str(width) + """
                                                WHERE id='""" + row_select + """';
                                          commit;"""

                except IndexError:
                    try:
                        #without caption and without tags 
                        dom_colors_1 = analysis['color']['dominantColors'][0]
                        confidence = analysis['description']['captions'][0]['confidence']
                        update_statement = """UPDATE dbo.image_attributes 
                                                SET accent_color = '""" + str(accent_color) + """',
                                                    dominant_color_background = '""" + dom_color_back + """',
                                                    dominant_color_foreground = '""" + dom_color_fore + """',
                                                    dominant_color_1 = '""" + dom_colors_1 + """',
                                                    is_bw_img = '""" + str(is_bw) + """',
                                                    confidence = """ + str(confidence) + """,
                                                    height = """ + str(height) + """,
                                                    width = """ + str(width) + """
                                                    WHERE id='""" + row_select + """';
                                              commit;"""

                    except IndexError:
                        try:
                            #without caption, tags, and dom_colors_1
                            confidence = analysis['description']['captions'][0]['confidence']

                            update_statement = """UPDATE dbo.image_attributes 
                                                    SET accent_color = '""" + str(accent_color) + """',
                                                        dominant_color_background = '""" + dom_color_back + """',
                                                        dominant_color_foreground = '""" + dom_color_fore + """',
                                                        is_bw_img = '""" + str(is_bw) + """',
                                                        confidence = """ + str(confidence) + """,
                                                        height = """ + str(height) + """,
                                                        width = """ + str(width) + """
                                                        WHERE id='""" + row_select + """';
                                                commit;"""
                        except IndexError:
                            try:
                                #without confidence, tags, caption, and dom_colors
                                update_statement = """UPDATE dbo.image_attributes 
                                                        SET accent_color = '""" + str(accent_color) + """',
                                                            dominant_color_background = '""" + dom_color_back + """',
                                                            dominant_color_foreground = '""" + dom_color_fore + """',
                                                            is_bw_img = '""" + str(is_bw) + """',
                                                            height = """ + str(height) + """,
                                                            width = """ + str(width) + """
                                                            WHERE id='""" + row_select + """';
                                                      commit;"""
                            except IndexError:
                                try:
                                    #same as above, add confidence and caption
                                    caption = analysis['description']['captions'][0]['text']
                                    confidence = analysis['description']['captions'][0]['confidence']
                                    update_statement = """UPDATE dbo.image_attributes 
                                                            SET accent_color = '""" + str(accent_color) + """', 
                                                            dominant_color_background = '""" + dom_color_back + """', 
                                                            dominant_color_foreground = '""" + dom_color_fore + """', 
                                                            is_bw_img = '""" + str(is_bw) + """', 
                                                            caption = '""" + caption + """', 
                                                            confidence = """ + str(confidence) + """, 
                                                            height = """ + str(height) + """, 
                                                            width = """ + str(width) + """ 
                                                            WHERE id='""" + row_select + """';
                                                          commit;"""
                                except IndexError:
                                    print('idk')

    except requests.exceptions.HTTPError as err:
        print(err)
        return
                    
    return update_statement


# In[10]:


def update_img_attr(df):
    counter = 0
    for index, row in df.iterrows(): 
        starttime = time()
        counter += 1
        if counter < 20:
            update_statement = get_img_attr(row['image_url'], row['id'])

            print(index)
            debug(update_statement)
            if update_statement == None:
                continue
            else:
                cursor.execute(update_statement)    
        else:
            counter = 0
            sleep(60.0 - ((time() - starttime) % 60.0))
        
        continue


# In[11]:


text_attr_query = "select * from dbo.text_attributes as dboi"
text_attr_df = sql_to_df(text_attr_query)
text_attr_df = text_attr_df.dropna(subset=["body"], how='any')
text_attr_df = text_attr_df.loc[660:]


# In[16]:


text_analytics_base_url = "https://southcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
language_api_url = text_analytics_base_url + "languages"
sentiment_api_url = text_analytics_base_url + "sentiment"
key_phrase_api_url = text_analytics_base_url + "keyPhrases"
tone_analyzer = ToneAnalyzerV3(
    version ='2017-09-21',
    username ='e4a9a55c-764e-4799-8c00-b0886bb6f019',
    password ='bMhV1vmUBzaq'
)


# In[13]:


def get_emotional(text, row_select):
    content_type = 'application/json'
    res = tone_analyzer.tone({"text": text},content_type)
    pos = 0
    
    try:

        while pos < (len(res['sentences_tone']) - 1):
            pos += 1
            i = 0
            if res['sentences_tone'][pos]['tones'] != []:
                while i <= (len(res['sentences_tone'][pos]['tones']) - 1):

                    score = res['sentences_tone'][pos]['tones'][i]['score']
                    tone_name = res['sentences_tone'][pos]['tones'][i]['tone_name']    
                    sample_text = res['sentences_tone'][pos]['text']

                    update_statement = """UPDATE dbo.text_attributes
                                            SET tone_""" + str(pos) + """ = '""" + str(tone_name) + """',
                                                text_sample_""" + str(pos) + """ = '""" + str(sample_text) + """',
                                                score_""" + str(pos) + """ = """ + str(score) + """
                                          WHERE id='""" + str(row_select) + """'; commit;""" 

                    debug(update_statement)
                    try:
                        cursor.execute(update_statement)
                    except:
                        break

                    i += 1
            else:
                continue



    except KeyError:
        while pos <= (len(res['document_tone']['tones']) - 1):
            score = res['document_tone']['tones'][pos]['score']
            tone_name = res['document_tone']['tones'][pos]['tone_name']


            pos += 1
            
            update_statement = """UPDATE dbo.text_attributes
                                    SET tone_""" + str(pos) + """ = '""" + str(tone_name) + """',
                                        score_""" + str(pos) + """ = """ + str(score) + """
                                  WHERE id='""" + str(row_select) + """'; commit;""" 
            
            debug(update_statement)
            try:
                cursor.execute(update_statement)
            except:
                break


# In[14]:


def update_emotions():
    for index, row in text_attr_df.iterrows():
        starttime = time()

        print(index)
        body_copy = row['body'].replace("'", "")
        get_emotional(body_copy, row['id'])


# In[17]:


def get_key_phrases(text, row_select, err):
    text_doc = {'documents' : [
        { 'id': '1', 'language': 'en', 'text': text },
    ]}
    
    key_phrases_headers   = {"Ocp-Apim-Subscription-Key": text_subscription_key}
    key_phrases_response  = requests.post(key_phrase_api_url, headers=key_phrases_headers, json=text_doc)
    key_phrases = key_phrases_response.json()
    phrase_len = len(key_phrases['documents'][0])
    
    try:
        if phrase_len == 1:
            key_1 = key_phrases['documents'][0]['keyPhrases'][0]
            
            update_statement = "UPDATE dbo.text_attributes SET key_phrases_1 = '" + str(key_1) + "' WHERE id='" + row_select + "'; commit;"
            
        elif phrase_len == 2:
            key_1 = key_phrases['documents'][0]['keyPhrases'][0]
            key_2 = key_phrases['documents'][0]['keyPhrases'][1]
            
            update_statement = "UPDATE dbo.text_attributes SET key_phrases_1 = '" + str(key_1) + "', key_phrases_2 = '" + str(key_2) + "' WHERE id='" + row_select + "'; commit;"
            
            
        elif phrase_len == 3:
            key_1 = key_phrases['documents'][0]['keyPhrases'][0]
            key_2 = key_phrases['documents'][0]['keyPhrases'][1]
            key_3 = key_phrases['documents'][0]['keyPhrases'][2]
            
            update_statement = "UPDATE dbo.text_attributes SET key_phrases_1 = '" + str(key_1) + "', key_phrases_2 = '" + str(key_2) + "', key_phrases_2 = '" + str(key_3) + "' WHERE id='" + row_select + "'; commit;"
            
        elif phrase_len == 4:
            key_1 = key_phrases['documents'][0]['keyPhrases'][0]
            key_2 = key_phrases['documents'][0]['keyPhrases'][1]
            key_3 = key_phrases['documents'][0]['keyPhrases'][2]
            key_4 = key_phrases['documents'][0]['keyPhrases'][3]
            
            update_statement = "UPDATE dbo.text_attributes SET key_phrases_1 = '" + str(key_1) + "', key_phrases_2 = '" + str(key_2) + "', key_phrases_2 = '" + str(key_3) + "', key_phrases_4 = '" + str(key_4) + "' WHERE id='" + row_select + "'; commit;"
            
        elif phrase_len == 5:
            key_1 = key_phrases['documents'][0]['keyPhrases'][0]
            key_2 = key_phrases['documents'][0]['keyPhrases'][1]
            key_3 = key_phrases['documents'][0]['keyPhrases'][2]
            key_4 = key_phrases['documents'][0]['keyPhrases'][3]
            key_5 = key_phrases['documents'][0]['keyPhrases'][4]
            
            update_statement = "UPDATE dbo.text_attributes SET key_phrases_1 = '" + str(key_1) + "', key_phrases_2 = '" + str(key_2) + "', key_phrases_2 = '" + str(key_3) + "', key_phrases_4 = '" + str(key_4) + "', key_phrases_5 = '" + str(key_5) + "' WHERE id='" + row_select + "'; commit;"
        
        else:
            return
        
    except IndexError:
        print(key_phrases)
        print(err)
        update_statement = str(key_phrases) + " " + str(err)
    except KeyError:
        print(key_phrases)
        print(err)
        update_statement = str(key_phrases) + " " + str(err)
        
    return update_statement


# In[18]:


def update_key_phrases_attr():
    counter = 0
    for index, row in text_attr_df.iterrows():
        starttime = time()
        counter += 1
        if counter < 20:
            update_statement = get_key_phrases(row['body'], row['id'], index)
            print(index)
            debug(update_statement)

            if update_statement == None:
                continue
            else:
                try:
                    cursor.execute(update_statement)
                except:
                    continue

        else:
            counter = 0
            sleep(60.0 - ((time() - starttime) % 60.0))


# In[19]:


def get_sentiment_attr(text, row_select, err):
    text_doc = {'documents' : [
        { 'id': '1', 'language': 'en', 'text': text },
    ]}
    a = json.dumps(text_doc)
    
    sentiment_headers   = {"Ocp-Apim-Subscription-Key": text_subscription_key}
    sentiment_response  = requests.post(sentiment_api_url, headers=sentiment_headers, json=text_doc)
    sentiments = sentiment_response.json()
    
    try:
        sentiment_score = sentiments['documents'][0]['score']    
        update_statement = "UPDATE dbo.text_attributes SET sentiment = " + str(sentiment_score) + " WHERE id='" + row_select + "'; commit;"
        
    except IndexError:
        print(sentiments)
        print(err)
        update_statement = str(sentiments) + " " + str(err)
    except KeyError:
        print(sentiments)
        print(err)
        update_statement = str(sentiments) + " " + str(err)
    
    return update_statement


# In[20]:


def update_text_attr():
    counter = 0
    for index, row in text_attr_df.iterrows():
        starttime = time()
        counter += 1
        if counter < 20:
            update_statement = get_sentiment_attr(row['body'], row['id'], index)
            print(index)
            debug(update_statement)
            
            if update_statement == None:
                continue
            else:
                cursor.execute(update_statement)
        
        else:
            counter = 0
            sleep(60.0 - ((time() - starttime) % 60.0))


# In[23]:


actions_query = """
                    SELECT  ad_id,
                            clicks,
                            cost_per_10_sec_video_view_value,
                            cpc,
                            cpp,
                            cpm,
                            ctr,
                            impressions,
                            reach,
                            relevance_score_score,
                            relevance_score_status
                            
                            
                    FROM    dbo.ad_insights
                """
actions_df = sql_to_df(actions_query)


# In[24]:


actions_df['cpa'] = actions_df[['cost_per_10_sec_video_view_value', 'cpc', 'cpp', 'cpm']].mean(axis=1)


# In[25]:


attr_query = """SELECT ia.*, ta.*, body, image_url, ads.id as ad_id
                FROM   dbo.image_attributes as ia,
                       dbo.text_attributes as ta,
                       dbo.ads as ads
                WHERE  ta.creative_id = ia.creative_id
                   AND ads.creative_id = ta.creative_id
                   AND ads.creative_id = ia.creative_id"""
attr_df = sql_to_df(attr_query)


# In[26]:


actions_attr_df = pd.merge(actions_df, attr_df, on='ad_id')
actions_attr_df.drop_duplicates(subset=['ad_id'], keep='last', inplace=True)
actions_attr_df.sort_values(by='cpa', inplace=True)
actions_attr_df['confidence'].fillna(actions_attr_df.confidence.mean(), inplace=True)


# # Colors

# In[27]:


def hex_to_hsv(h):
    r, g, b = (tuple(int(h[i:i+2], 16) for i in (0, 2 ,4)))
    h, s, v = colors.rgb_to_hsv(r, g, b)
    
    return h*360, s*100, v/255


# In[28]:


def color_name(h):
    
    h, s, v = hex_to_hsv(h)
    
    if h < 60:
        h = 'red'
    elif h >= 60 and h < 120:
        h = 'yellow'
    elif h >= 120 and h < 180:
        h = 'green'
    elif h >= 180 and h < 240:
        h = 'cyan'
    elif h >= 240 and h < 300:
        h = 'blue'
    elif h >= 300 and h <= 360:
        h = 'magenta'
        
    return h


# In[29]:


def color_saturation(h): 
    h, s, v = hex_to_hsv(h)
    
    if s < 25:
        s = 'dim saturation'
    elif s >= 25 and s < 50:
        s = 'low saturation'
    elif s >= 50 and s < 75:
        s = 'moderate saturation'
    elif s >= 75 and s <= 100:
        s = 'high saturation'
        
    return s


# In[30]:


def color_brightness(h):
    h, s, v = hex_to_hsv(h)
    
    if v < 25:
        v = 'dim brightness'
    elif v >= 25 and v < 50:
        v = 'low brightness'
    elif v >= 50 and v < 75:
        v = 'moderate brightness'
    elif v >= 75 and v <= 100:
        v = 'high brightness'
    
    return v


# In[32]:


actions_attr_df['accent_color_name'] = actions_attr_df['accent_color'].apply(color_name)
actions_attr_df['color_saturation'] = actions_attr_df['accent_color'].apply(color_saturation)
actions_attr_df['color_brightness'] = actions_attr_df['accent_color'].apply(color_brightness)
actions_attr_df['accent_color'] = actions_attr_df['accent_color'].fillna(actions_attr_df['accent_color'].mode()[0])


# In[33]:


def back_analysis(df):
    df.sort_values(by='cpa', inplace=True)
    df = df[df['relevance_score_status'] == 'OK']
    df = df[0:4]

    new_df = df[['sentiment', 'key_phrases_1', 'tone_1', 'tone_2', 'accent_color_name', 'color_saturation', 'color_brightness', 'dominant_color_background', 'body', 'image_url']].copy()


# In[34]:


color_var_list = ['accent_color_name', 'color_saturation', 'color_brightness', 'dominant_color_background', 'dominant_color_foreground', 'dominant_color_1']
text_var_list = ['sentiment', 'tone_1']


# In[36]:


color_variables = pd.DataFrame(actions_attr_df.groupby(color_var_list).cpa.mean())
color_variables.reset_index(level=color_var_list, inplace=True)
color_variables.set_index('cpa', inplace=True)
color_variables.sort_values(by='cpa', inplace=True)


# In[38]:


text_variables = pd.DataFrame(actions_attr_df.groupby(text_var_list).cpa.mean())
text_variables.reset_index(level=text_var_list, inplace=True)
text_variables.set_index('cpa', inplace=True)
text_variables.sort_values(by='cpa', inplace=True)


# In[39]:


text_and_color = pd.merge(text_variables, color_variables, on='cpa')

def get_top_cpas():
    b = text_and_color
    cpa_trends = b.index.values

    return cpa_trends


# In[40]:


def avg_cpa(df, var, attr):
    df = df[df[var] == attr]
    indices = df.index.values
    index_avg = indices.mean()
    return index_avg


# In[41]:


def cpa_lookup(df):
    rows, columns = df.shape
    i = 0
    lookup_table = {}
    col_val = df.columns.values
    while i < columns:
        col_sel = df.iloc[:, i]
        for row in col_sel:
            col_header = col_val[i]
            avg = avg_cpa(df, col_header, row)
            lookup_table[row] = avg
            #print("attr: " + str(row) + "\n avg_cpa: $" + str(avg) + "\n\n")
        i += 1
    return lookup_table


# In[42]:


def find_in_lookup(val):
    data = cpa_lookup(text_and_color)
    
    for key, value in data.items():
        if key == val:
            return value


# In[43]:


def est_cpa(df, row_set):
    rows, columns = df.shape
    i = 0
    temp = {}
    row_sel = df.iloc[row_set, :]

    for val in row_sel:
        if i < 7:
            temp[i] = find_in_lookup(val)
            i+=1
        else:
            break
                      
    mean = float(sum(temp.values())) / len(temp)
    return mean


# In[44]:


def petri_dish():
    accent_color_name = text_and_color['accent_color_name']
    color_saturation = text_and_color['color_saturation']
    color_brightness = text_and_color['color_brightness']
    dominant_color_background = text_and_color['dominant_color_background']
    dominant_color_foreground = text_and_color['dominant_color_foreground']
    dominant_color_1 = text_and_color['dominant_color_1']
    sentiment = text_and_color['sentiment']
    tone_1 = text_and_color['tone_1']
    test_combos = list(product(accent_color_name, color_saturation, color_brightness, dominant_color_background, dominant_color_foreground, dominant_color_1, tone_1))
    blah = pd.DataFrame(test_combos)
    
    rows, columns = blah.shape
    blah = blah.drop_duplicates(subset=[0,1,2,3,4,5,6], keep='first')
#     blah = blah[:10]
    blah_indeces = blah.index.values
    blah['est_cpa'] = ""
    
    def update_cpa():
        i=0
        for row in blah_indeces:
            blah['est_cpa'][row] = est_cpa(blah, i)
            i += 1
            
    update_cpa()

    blah.sort_values(by='est_cpa', inplace=True)
    #blah.drop_duplicates(subset=['est_cpa'], keep='last', inplace=True)
    
    return blah

