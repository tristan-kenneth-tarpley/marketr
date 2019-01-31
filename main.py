from flask import Flask, render_template, flash, request, url_for, flash, redirect, session, abort
import numpy as np
import pandas as pd
import urllib
import os
import pyodbc
import json
from flask_socketio import SocketIO

import analysis as an


app = Flask(__name__)
socketio = SocketIO(app)

server = 'tarpley.database.windows.net'
database = 'marketr'
username = 'tristan'
password = 'Fiverrtemp!'
driver= '{ODBC Driver 13 for SQL Server}'

connStr = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
db = pyodbc.connect(connStr)

def sql_to_df(x):
    return pd.read_sql_query(x, db, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)


#########################
#########################
#########################
#####INTAKE ROUTES#######
#########################
#########################
#########################


@app.route('/new')
def new():
    if not session.get('logged_in'):
        return render_template('create.html')
    else:
        return begin()


@app.route('/begin')
def begin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('intake/init_setup.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    session['logged_in'] = True 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    print(POST_USERNAME + " " + POST_PASSWORD)

    cursor = db.cursor()

    query = """INSERT INTO dbo.customer_basic (
                                    email,
                                    password)
                VALUES ('""" + POST_USERNAME + """',
                        '""" + POST_PASSWORD + """'); commit;"""

    cursor.execute(query)

    cursor.close()

    result = sql_to_df("SELECT * from dbo.customer_basic WHERE email = '" + POST_USERNAME + "' AND password = '" + POST_PASSWORD + "'")

    if result['ID'][0] != None:
        session['logged_in'] = True
        session.permanent = True
        uid = result['ID'][0]
        session['user'] = int(uid)
        return begin()





@app.route('/competitors', methods=['POST'])
def competitors():
    POST_first_name = str(request.form['first_name'])
    POST_last_name = str(request.form['last_name'])
    POST_company_name = str(request.form['company_name'])
    POST_revenue = str(request.form['revenue'])
    POST_city = str(request.form['city'])
    POST_state = str(request.form['state'])
    POST_stage = str(request.form['one'])
    POST_employees = str(request.form['employees'])


    query = """UPDATE dbo.customer_basic 
                SET first_name = '""" + POST_first_name + """', last_name = '""" + POST_last_name + """', company_name = '""" + POST_company_name + """', revenue = '""" + POST_revenue + """', city = '""" + POST_city + """', state = '""" + POST_state + """', stage = '""" + POST_stage + """', employees = '""" + POST_employees + """' 
                WHERE dbo.customer_basic.ID = '""" + str(session['user']) + """'; commit;"""

    if POST_first_name:
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
    else:
        print('nothing to see here')


    print(POST_stage + " " + POST_first_name + " " + POST_last_name + " " + POST_company_name + " " + POST_revenue + " " + POST_city + " " + POST_state)

    return render_template('intake/competitors.html')




@app.route('/competitors/company', methods=['POST'])
def company():
    POST_industry = str(request.form['industry'])
    POST_comp_1_name = str(request.form['competitor_1_name'])
    POST_comp_1_website = str(request.form['competitor_1_site'])
    POST_comp_1_type = str(request.form['comp_1_type'])
    POST_comp_2_name = str(request.form['competitor_2_name'])
    POST_comp_2_website = str(request.form['competitor_2_site'])
    POST_comp_2_type = str(request.form['comp_2_type'])


    query = """INSERT INTO dbo.competitors 
                (customer_id, industry, comp_1_name, comp_1_website, comp_1_type, comp_2_name, comp_2_website, comp_2_type)
                VALUES ('""" + str(session['user']) + """','""" + POST_industry + """','""" + POST_comp_1_name + """','""" + POST_comp_1_website + """','""" + POST_comp_1_type + """','""" + POST_comp_2_name + """','""" + POST_comp_2_website + """','""" + POST_comp_2_type + """');commit;""" 

    print(query)

    if POST_comp_1_name:
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
    else:
        print('nothing to see here')

    return render_template('intake/company.html')

@app.route('/competitors/company/audience', methods=['POST'])
def audience():
    POST_b2b = str(request.form['b2b'])
    POST_b2c = str(request.form['b2c'])
    POST_c2c = str(request.form['c2c'])
    POST_other = str(request.form['other'])
    POST_biz_model = str(request.form['biz_model'])
    POST_storefront = str(request.form['storefront'])
    POST_direct = str(request.form['direct'])
    POST_online = str(request.form['online'])
    POST_tradeshows = str(request.form['tradeshows'])
    POST_other = str(request.form['other'])
    POST_freeform = str(request.form['freeform'])

    query = """INSERT INTO dbo.company_info
                (customer_id, selling_to, selling_to_2, selling_to_3, selling_to_4, biz_model, rev_channel_1, rev_channel_2, rev_channel_3, rev_channel_4, rev_channel_5, rev_channel_freeform)
                VALUES ('""" + str(session['user']) + """','""" + POST_b2b + """','""" + POST_b2c + """','""" + POST_c2c + """','""" + POST_other + """','""" + POST_biz_model + """','""" + POST_storefront + """','""" + POST_direct + """','""" + POST_online + """','""" + POST_tradeshows + """','""" + POST_other + """','""" + POST_freeform + """');commit;"""
    print(query)
    if POST_b2b:
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
    else:
        print('nothing to see here')

    return render_template('intake/audience.html')

@app.route('/competitors/company/audience/product', methods=['POST'])
def product():
    POST_gender = str(request.form['gender'])
    POST_age_group_1 = str(request.form['age_group_1'])
    POST_age_group_2 = str(request.form['age_group_2'])
    POST_age_group_3 = str(request.form['age_group_3'])
    POST_age_group_4 = str(request.form['age_group_4'])
    POST_age_group_5 = str(request.form['age_group_5'])
    POST_age_group_6 = str(request.form['age_group_6'])
    POST_age_group_7 = str(request.form['age_group_7'])
    POST_age_group_8 = str(request.form['age_group_8'])
    POST_location = str(request.form['location'])
    POST_why = str(request.form['why'])
    POST_before_1 = str(request.form['before_1'])
    POST_before_2 = str(request.form['before_2'])
    POST_before_3 = str(request.form['before_3'])
    POST_before_4 = str(request.form['before_4'])
    POST_before_5 = str(request.form['before_5'])
    POST_before_6 = str(request.form['before_6'])
    POST_before_7 = str(request.form['before_7'])
    POST_before_8 = str(request.form['before_8'])
    POST_before_9 = str(request.form['before_9'])
    POST_before_10 = str(request.form['before_10'])
    POST_before_freeform = str(request.form['before_freeform'])
    POST_after_1 = str(request.form['after_1'])
    POST_after_2 = str(request.form['after_2'])
    POST_after_3 = str(request.form['after_3'])
    POST_after_4 = str(request.form['after_4'])
    POST_after_5 = str(request.form['after_5'])
    POST_after_6 = str(request.form['after_6'])
    POST_after_7 = str(request.form['after_7'])
    POST_after_8 = str(request.form['after_8'])
    POST_after_9 = str(request.form['after_9'])
    POST_after_10 = str(request.form['after_10'])
    POST_after_freeform = str(request.form['after_freeform'])

    query = """INSERT INTO dbo.audience
                (customer_id, gender, age_group_1, age_group_2, age_group_3, age_group_4, age_group_5, age_group_6, age_group_7, age_group_8, location, why, before_1, before_2, before_3, before_4, before_5, before_6, before_7, before_8, before_9, before_10, before_freeform, after_1, after_2, after_3, after_4, after_5, after_6, after_7, after_8, after_9, after_10, after_freeform)
                VALUES ('""" + str(session['user']) + """','""" + POST_gender + """','""" + POST_age_group_1 + """','""" + POST_age_group_2 + """','""" + POST_age_group_3 + """','""" + POST_age_group_4 + """','""" + POST_age_group_5 + """','""" + POST_age_group_6 + """','""" + POST_age_group_7 + """','""" + POST_age_group_8 + """','""" + POST_location + """','""" + POST_why + """','""" + POST_before_1 + """','""" + POST_before_2 + """','""" + POST_before_3 + """','""" + POST_before_4 + """','""" + POST_before_5 + """','""" + POST_before_6 + """','""" + POST_before_7 + """','""" + POST_before_8 + """','""" + POST_before_9 + """','""" + POST_before_10 + """','""" + POST_before_freeform + """','""" + POST_after_1 + """','""" + POST_after_2 + """','""" + POST_after_3 + """','""" + POST_after_4 + """','""" + POST_after_5 + """','""" + POST_after_6 + """','""" + POST_after_7 + """','""" + POST_after_8 + """','""" + POST_after_9 + """','""" + POST_after_10 + """','""" + POST_after_freeform + """');commit;"""

    if POST_gender:
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
    else:
        print('nothing to see here!')

    return render_template('/intake/product.html')


@app.route('/competitors/company/audience/product/product_2', methods=['POST'])
def product_2():
    POST_gen_description = str(request.form['gen_description'])
    POST_quantity = str(request.form['quantity'])
    POST_sku = str(request.form['sku'])
    POST_link = str(request.form['link'])
    POST_segment_1 = str(request.form['segment_1'])
    POST_segment_2 = str(request.form['segment_2'])
    POST_segment_3 = str(request.form['segment_3'])
    POST_segment_4 = str(request.form['segment_4'])
    POST_segment_5 = str(request.form['segment_5'])
    POST_segment_6 = str(request.form['segment_6'])
    POST_segment_7 = str(request.form['segment_7'])
    POST_segment_8 = str(request.form['segment_8'])
    POST_segment_9 = str(request.form['segment_9'])
    POST_segment_10 = str(request.form['segment_10'])
    POST_source_1 = str(request.form['source_1'])
    POST_source_2 = str(request.form['source_2'])
    POST_source_3 = str(request.form['source_3'])
    POST_source_4 = str(request.form['source_4'])
    POST_source_freeform = str(request.form['source_freeform'])



    query = """INSERT INTO dbo.product_gen
                (uid,gen_description,quantity,sku,link,segment_1,segment_2,segment_3,segment_4,segment_5,segment_6,segment_7,segment_8,segment_9,segment_10,source_1,source_2,source_3,source_4,source_freeform)
                VALUES ('""" + str(session['user']) + """','""" + POST_gen_description + """','""" + POST_quantity + """','""" + POST_sku + """','""" + POST_link + """','""" + POST_segment_1 + """','""" + POST_segment_2 + """','""" + POST_segment_3 + """','""" + POST_segment_4 + """','""" + POST_segment_5 + """','""" + POST_segment_6 + """','""" + POST_segment_7 + """','""" + POST_segment_8 + """','""" + POST_segment_9 + """','""" + POST_segment_10 + """','""" + POST_source_1 + """','""" + POST_source_2 + """','""" + POST_source_3 + """','""" + POST_source_4 + """','""" + POST_source_freeform + """');commit;"""
       


    if POST_sku:
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()

    else:
        print("seriously...NOTHING TO SEE HERE") 

    d = request.form

    new_df = pd.DataFrame(list(d.items()))
    new_df = new_df[20:]
    
    print(new_df.head(40))

    for

    POST_product_len = request.form['product_len']
    
    # q = 1
    # while q < POST_product_len:
    #     #cursor = db.cursor()
    #     working = "INSERT INTO dbo.product_list (name, category, cogs, sales_price, qty_sold, est_unique_buyers) VALUES ('" + 
    #                                                                                                                                             """name="product_` + i + `"_name"""

    return render_template('/intake/product_2.html')

@app.route('/competitors/company/audience/product/product_2/salescycle', methods=['POST'])
def salescycle():
    return render_template('/intake/salescycle.html')

@app.route('/company_info', methods=['POST'])
def company_info():
    return nice()

@app.route('/nice')
def nice():
    return render_template('intake/nice.html')

@app.route('/nice/')
def red_nice():
    return redirect('/nice', code=302)






@app.route('/goals')
def goals():
    return render_template('intake/2/goals.html')









@app.route('/begin/')
def red_begin():
    return redirect("/begin", code=302)

@app.route('/competitors/')
def red_competitors():
    return redirect("/competitors", code=302)

@app.route('/competitors/company/')
def red_company():
    return redirect('/competitors/company', code=302)

@app.route('/competitors/company/audience/')
def red_audience():
    return redirect('/competitors/company/audience', code=302)

@app.route('/competitors/company/audience/product/')
def red_product():
    return redirect('/competitors/company/audience/product', code=302)

@app.route('/competitors/company/audience/product/salescycle/')
def red_salescycle():
    return redirect('/competitors/company/audience/product/salescycle', code=302)


@app.route('/nice')


@app.route('/goals/')
def red_goals():
    return redirect('/goals', code=302)


#########################


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    result = an.sql_to_df("SELECT * from dbo.customer_basic WHERE email = '" + POST_USERNAME + "' AND password = '" + POST_PASSWORD + "'")
    try:    
        if result['ID'][0] != None:
            session['logged_in'] = True
            uid = result['ID'][0]
            session['user'] = int(uid)
            session.permanent = True
            return begin()

    except IndexError:
        flash('wrong password!')
        return index()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()












@app.route('/onload')
def onload():
	a = an.get_customers()
	name = a['first_name'][0]
	last = a['last_name'][0]
	full_name = name + " " + last

	# cpas = an.get_top_cpas()
	# one = cpas[0]

	return full_name #, cpas

@app.route('/data-pop')
def onload_2():
	cpas = an.get_top_cpas()
	cpas = np.round(cpas, 2)
	#cpas = cpas.astype(str)
	cpas = cpas.tolist()
	cpas = json.dumps(cpas)

	return cpas





@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/recommendations/')
def red_rec():
    return redirect("/recommendations", code=302)
@app.route('/getrecs')
def get_rec():
    print('hi from the client')
    a = an.petri_dish()
    petri = a.head(5)
    petjson = petri.to_json(orient='split')

    return petjson





@app.route('/campaigns')
def campaigns():
    return render_template('campaigns.html')


@app.route('/campaigns/')
def red_campaigns():
    return redirect("/campaigns", code=302)


@app.route('/integrations')
def integrations():
    return render_template('integrations.html')


@app.route('/integrations/')
def red_integrations():
    return redirect("/integrations", code=302)


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/settings/')
def red_settings():
    return redirect("/settings", code=302)


@app.route('/campaigns/newcampaign')
def create_campaign():
    return render_template('newcampaign.html')


@app.route('/campaigns/newcampaign')
def red_newcampaigns():
    return redirect("/campaigns/newcampaign", code=302)


#UPLOAD_FOLDER = '../marketr/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/create_campaign', methods=['POST'])
def exe_campaign():
    campaign_name = request.form['campaign_name']

    file = request.files['files[]']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    dog = request.form['dog']
    beer = request.form['beer']

    print(campaign_name + " " + filename + " " + beer)

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.urandom(12)
    app.run(debug=True)





