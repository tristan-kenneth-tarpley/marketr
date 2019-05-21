from main import *

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def customer_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    result = an.sql_to_df("SELECT * from dbo.customer_basic WHERE email = '" + POST_USERNAME + "' AND password = '" + POST_PASSWORD + "'")
    
    try:    
        if result['ID'][0] != None:
            session['logged_in'] = True
            uid = result['ID'][0]
            session['user'] = int(uid)
            session.permanent = True
            session.remember=True

            first_query = sql_to_df("SELECT first_name FROM dbo.customer_basic WHERE ID = '" + str(session['user']) + "'")
            steps = {'competitors': 'competitors',
                     'company_info': 'company',
                     'audience': 'audience',
                     'product_gen': 'product',
                     'product_list': 'product_2',
                     'awareness': 'salescycle',
                     'goals': 'goals',
                     'history': 'history',
                     'platforms': 'platforms',
                     'past': 'past',
                     'the end': 'index'}

            if first_query['first_name'][0] == None:
                return begin()

            else:
                def call_it(name):
                    print('made it here')
                    return steps[name]

                i = 0
                for step in steps:
                    if step != 'the end':
                        def_query = sql_to_df("SELECT customer_id FROM " + step + " WHERE customer_id = '" + str(session['user']) + "'")
                        print(step)
                        i+=1
                        print(i)
                        if def_query.empty == True:
                            perc_complete = str(i*10)
                            print(perc_complete)
                            cursor = db.cursor()
                            cursor.execute("""UPDATE dbo.customer_basic SET perc_complete = '""" + str(perc_complete) + """' WHERE id = """ + str(session['user']) + """;commit;""")
                            return redirect(url_for(call_it(step)))
                    else:
                        i+=1
                        return redirect(url_for(call_it(step)))

    except IndexError:
        flash('incorrect email or password')
        return logout()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


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
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    query = """INSERT INTO dbo.customer_basic (
                                    email,
                                    password,
                                    account_created,
                                    last_modified)
                VALUES ('""" + POST_USERNAME + """',
                        '""" + POST_PASSWORD + """',
                        '""" + str(st) + """',
                        '""" + str(st) + """'); commit;"""

    cursor.execute(query)

    cursor.close()

    result = sql_to_df("SELECT * from dbo.customer_basic WHERE email = '" + POST_USERNAME + "' AND password = '" + POST_PASSWORD + "'")


    if result['ID'][0] != None:
        session['logged_in'] = True
        session.permanent = True
        uid = result['ID'][0]
        session['user'] = int(uid)
        return begin()


@app.route('/availability', methods=['GET'])
def availability():
    result = sql_to_df('select email from dbo.customer_basic')
    result = result.to_json(orient='records')

    return result



@app.route('/admin')
def admin():

    if not session.get('logged_in'):
        return render_template('admin_view/login.html')
    else:
        results = sql_to_df("SELECT customer_basic.id, customer_basic.company_name, customer_basic.account_created, customer_basic.perc_complete, customer_basic.last_modified, admins.first_name FROM customer_basic, admins WHERE admins.ID = '" + str(session['admin']) + "' ORDER BY company_name ASC")

        #results = results.to_json(orient='records')
        print(results.head())
        # company_name = results['']
        # account_created =
        # perc_complete = 
        # last_modified =

        return render_template('admin_view/admin_index.html', results=results)

@app.route('/admin/<customer_id>')
def company_view(customer_id):

    if not session.get('logged_in'):
        return render_template('admin_view/login.html')
    else:
        load_profile = an.sql_to_df("""SELECT * FROM dbo.customer_basic WHERE id = """ + customer_id)
        load_competitors = an.sql_to_df(""" SELECT * FROM dbo.competitors WHERE customer_id = '""" + customer_id + """'""")
        load_company_info = an.sql_to_df(""" SELECT * FROM dbo.company_info WHERE customer_id = '""" + customer_id + """'""")
        load_audience = an.sql_to_df(""" SELECT * FROM dbo.audience WHERE customer_id = '""" + customer_id + """'""")
        load_goals = an.sql_to_df(""" SELECT * FROM dbo.goals WHERE customer_id = """ + customer_id)
        load_historical_platforms = an.sql_to_df(""" SELECT * FROM dbo.history WHERE customer_id = '""" + customer_id + """'""")
        load_product = an.sql_to_df(""" SELECT * FROM dbo.product_gen WHERE customer_id = '""" + customer_id + """'""")
        #load_product_details = """ SELECT * FROM dbo. WHERE id = """ + customer_id


        return render_template('admin_view/company_view.html', profile = load_profile, competitors = load_competitors, company_info = load_company_info, audience = load_audience, goals = load_goals, historical_platforms = load_historical_platforms, product = load_product)





@app.route('/admin_login', methods=['POST'])
def admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    result = an.sql_to_df("SELECT * from dbo.admins WHERE email = '" + POST_USERNAME + "' AND password = '" + POST_PASSWORD + "'")    

    try:    
        if result['ID'][0] != None:
            session['logged_in'] = True
            uid = result['ID'][0]
            session['admin'] = int(uid)
            session.permanent = True
            session.remember = True
            return redirect(url_for('admin'))

    except IndexError:
        flash('incorrect email or password')
        return redirect(url_for('admin'))


@app.route('/load_admin')
def load_admin():
    results = sql_to_df('SELECT customer_basic.id, customer_basic.company_name, admins.first_name FROM customer_basic, admins WHERE admins.ID = ' + str(session['admin']))

    results = results.to_json(orient='records')

    return results


@app.route('/admin_availability', methods=['GET'])
def admin_availability():
    result = sql_to_df('select email from dbo.admins')
    result = result.to_json(orient='records')

    return result


@app.route('/new_admin')
def new_admin():
    return render_template('admin_view/new.html')


@app.route('/add_admin', methods=['POST'])
def add_admin():
    POST_first_name = str(request.form['first_name'])
    POST_last_name = str(request.form['last_name'])
    POST_USERNAME = str(request.form['email'])
    POST_PASSWORD = str(request.form['password'])

    print(POST_USERNAME + " " + POST_PASSWORD)

    cursor = db.cursor()

    query = """INSERT INTO dbo.admins (
                                    first_name,
                                    last_name,
                                    email,
                                    password)
                VALUES ('""" + POST_first_name + """',
                        '""" + POST_last_name + """',
                        '""" + POST_USERNAME + """',
                        '""" + POST_PASSWORD + """'); commit;"""

    cursor.execute(query)

    cursor.close()

    result = sql_to_df('SELECT * FROM dbo.admins')

    if result['ID'][0] != None:
        return admin()




@app.route('/competitors', methods=['POST','GET'])
def competitors():
    if not request.form:
        print('should work')
    elif request.form:
        POST_first_name = str(request.form['first_name'])
        POST_last_name = str(request.form['last_name'])
        POST_company_name = str(request.form['company_name'])
        POST_revenue = str(request.form['revenue'])
        POST_zip = str(request.form['zip'])
        # POST_city = str(request.form['city'])
        # POST_state = str(request.form['state'])
        POST_stage = str(request.form['one'])
        POST_employees = str(request.form['employees'])

        zips = zipcodes.matching(POST_zip)

        POST_city = zips[0]['city']
        POST_state = zips[0]['state']

        query = """UPDATE dbo.customer_basic 
                    SET first_name = '""" + POST_first_name + """', last_name = '""" + POST_last_name + """', company_name = '""" + POST_company_name + """', revenue = '""" + POST_revenue + """', city = '""" + POST_city + """', state = '""" + POST_state + """', stage = '""" + POST_stage + """', employees = '""" + POST_employees + """', zip = '""" + str(POST_zip) + """'  
                    WHERE dbo.customer_basic.ID = '""" + str(session['user']) + """'; commit;"""

        if POST_first_name:
            cursor = db.cursor()
            cursor.execute(query)
            cursor.close()

            last_modified(str(session['user']))

        else:
            print('nothing to see here')


        print(POST_stage + " " + POST_first_name + " " + POST_last_name + " " + POST_company_name + " " + POST_revenue + " " + POST_city + " " + POST_state)



    if session.get('logged_in'):
        return render_template('intake/competitors.html')
    else:
        return logout()    




@app.route('/competitors/company', methods=['POST', 'GET'])
def company():
    if not request.form:
        print('should work')
    elif request.form:
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
            last_modified(str(session['user']))
        else:
            print('nothing to see here')

    if session.get('logged_in'):
        return render_template('intake/company.html')
    else:
        return logout()  

@app.route('/competitors/company/audience', methods=['POST', 'GET'])
def audience():
    if not request.form:
        print('should work')
    elif request.form:
        POST_b2b = str(request.form['b2b'])
        POST_b2c = str(request.form['b2c'])
        POST_c2c = str(request.form['c2c'])
        POST_other = str(request.form['other'])
        POST_biz_model = str(request.form['biz_model'])
        POST_storefront = str(request.form['storefront'])
        POST_storefront_perc = str(request.form['storefront_percent'])
        POST_direct = str(request.form['direct'])
        POST_direct_perc = str(request.form['direct_percent'])
        POST_online = str(request.form['online'])
        POST_online_perc = str(request.form['online_percent'])
        POST_tradeshows = str(request.form['tradeshows'])
        POST_tradeshows_perc = str(request.form['tradeshows_percent'])
        POST_other = str(request.form['other'])
        POST_other_perc = str(request.form['other_percent'])
        POST_freeform = str(request.form['freeform'])
        POST_freeform = POST_freeform.replace("'", "")
        POST_freeform = POST_freeform.replace('"', "")

        query = """INSERT INTO dbo.company_info
                    (customer_id, selling_to, selling_to_2, selling_to_3, selling_to_4, biz_model, rev_channel_1, rev_channel_2, rev_channel_3, rev_channel_4, rev_channel_5, rev_channel_freeform, storefront_perc, direct_perc, online_perc, tradeshows_perc, other_perc)
                    VALUES ('""" + str(session['user']) + """','""" + POST_b2b + """','""" + POST_b2c + """','""" + POST_c2c + """','""" + POST_other + """','""" + POST_biz_model + """','""" + POST_storefront + """','""" + POST_direct + """','""" + POST_online + """','""" + POST_tradeshows + """','""" + POST_other + """','""" + POST_freeform + """','""" + POST_storefront_perc + """','""" +  POST_direct_perc + """','""" +  POST_online_perc + """','""" +  POST_tradeshows_perc + """','""" +  POST_other_perc + """');commit;"""
        print(query)
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
        last_modified(str(session['user']))
        print('nothing to see here')

    if session.get('logged_in'):
        return render_template('intake/audience.html')
    else:
        return logout()  


@app.route('/competitors/company/audience/product', methods=['POST', 'GET'])
def product():
    if not request.form:
        print('should work')
    elif request.form:

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
        POST_before_freeform = POST_before_freeform.replace("'", "")
        POST_before_freeform = POST_before_freeform.replace('"', "")
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
        POST_after_freeform = POST_after_freeform.replace('"', "")
        POST_after_freeform = POST_after_freeform.replace("'", "")

        query = """INSERT INTO dbo.audience
                    (customer_id, gender, age_group_1, age_group_2, age_group_3, age_group_4, age_group_5, age_group_6, age_group_7, age_group_8, location, why, before_1, before_2, before_3, before_4, before_5, before_6, before_7, before_8, before_9, before_10, before_freeform, after_1, after_2, after_3, after_4, after_5, after_6, after_7, after_8, after_9, after_10, after_freeform)
                    VALUES ('""" + str(session['user']) + """','""" + POST_gender + """','""" + POST_age_group_1 + """','""" + POST_age_group_2 + """','""" + POST_age_group_3 + """','""" + POST_age_group_4 + """','""" + POST_age_group_5 + """','""" + POST_age_group_6 + """','""" + POST_age_group_7 + """','""" + POST_age_group_8 + """','""" + POST_location + """','""" + POST_why + """','""" + POST_before_1 + """','""" + POST_before_2 + """','""" + POST_before_3 + """','""" + POST_before_4 + """','""" + POST_before_5 + """','""" + POST_before_6 + """','""" + POST_before_7 + """','""" + POST_before_8 + """','""" + POST_before_9 + """','""" + POST_before_10 + """','""" + POST_before_freeform + """','""" + POST_after_1 + """','""" + POST_after_2 + """','""" + POST_after_3 + """','""" + POST_after_4 + """','""" + POST_after_5 + """','""" + POST_after_6 + """','""" + POST_after_7 + """','""" + POST_after_8 + """','""" + POST_after_9 + """','""" + POST_after_10 + """','""" + POST_after_freeform + """');commit;"""

        if POST_gender:
            cursor = db.cursor()
            cursor.execute(query)
            cursor.close()
            last_modified(str(session['user']))
        else:
            print('nothing to see here!')

    if session.get('logged_in'):
        return render_template('intake/product.html')
    else:
        return logout()  


@app.route('/competitors/company/audience/product/product_2', methods=['POST', 'GET'])
def product_2():
    if not request.form:
        print('should work')
    elif request.form:
        POST_gen_description = str(request.form['gen_description'])
        POST_gen_description = POST_gen_description.replace("'", "")
        POST_gen_description = POST_gen_description.replace('"', "")
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
        POST_source_freeform = POST_source_freeform.replace("'", "")
        POST_source_freeform = POST_source_freeform.replace('"', "")
        POST_product_1_name = str(request.form['product_1_name'])


        query = """INSERT INTO dbo.product_gen
                    (customer_id,gen_description,quantity,sku,link,segment_1,segment_2,segment_3,segment_4,segment_5,segment_6,segment_7,segment_8,segment_9,segment_10,source_1,source_2,source_3,source_4,source_freeform)
                    VALUES ('""" + str(session['user']) + """' , '""" + POST_gen_description + """','""" + POST_quantity + """','""" + POST_sku + """','""" + POST_link + """','""" + POST_segment_1 + """','""" + POST_segment_2 + """','""" + POST_segment_3 + """','""" + POST_segment_4 + """','""" + POST_segment_5 + """','""" + POST_segment_6 + """','""" + POST_segment_7 + """','""" + POST_segment_8 + """','""" + POST_segment_9 + """','""" + POST_segment_10 + """','""" + POST_source_1 + """','""" + POST_source_2 + """','""" + POST_source_3 + """','""" + POST_source_4 + """','""" + POST_source_freeform + """');commit;"""
           


        if POST_sku:
            print(query)
            cursor = db.cursor()
            cursor.execute(query)
            cursor.close()
            last_modified(str(session['user']))

        else:
            print("seriously...NOTHING TO SEE HERE") 


        if POST_product_1_name:


            req = request.form
            d = pd.DataFrame(list(req.items()))
            d = d[20:]

            product_len = int(request.form['product_len'])

            z = 0
            d1 = {}
            for x, y in d.items():
                d1[str(z)] = y
                z = z+1

            test = list(d.iloc[:,1])
            #print(test)

            q = 0

            while q < product_len:
                if q > 0 and q < product_len:
                    test = test[6:]
                
                query = """INSERT INTO dbo.product_list (customer_id,name,category,cogs,sales_price,qty_sold,est_unique_buyers) VALUES ('""" + str(session['user']) + """','""" + test[0] + """','""" + test[1] + """','""" + test[2] + """','""" + test[3] + """','""" + test[4] + """','""" + test[5] + """');commit;"""
                print(query)
                cursor = db.cursor()
                cursor.execute(query)
                cursor.close()
                q += 1
            last_modified(str(session['user']))

        else:
            print("how many times do I have to tell you?..there's nothing to see here")


    
    # q = 1
    # while q < POST_product_len:
    #     #cursor = db.cursor()
    #     working = "INSERT INTO dbo.product_list (name, category, cogs, sales_price, qty_sold, est_unique_buyers) VALUES ('" + 
    #                                                                                                                                             """name="product_` + i + `"_name"""

    if session.get('logged_in'):
        return render_template('intake/product_2.html')
    else:
        return logout()  

@app.route('/load_product_list', methods=['GET', 'POST'])
def load_product_list():
    query = "SELECT p_id, name, category FROM dbo.product_list WHERE customer_id = " + str(session['user'])

    results = sql_to_df(query)
    results = results.to_json(orient='records')


    return results


@app.route('/product_submit', methods=['POST'])
def product_submit():

    POST_complexity = request.form['complexity']
    POST_price = request.form['price']
    POST_product_or_service = request.form['product_or_service']
    POST_frequency_of_use = request.form['frequency_of_use']
    POST_frequency_of_purchase = request.form['frequency_of_purchase']
    POST_value_prop = request.form['value_prop']
    POST_warranties_or_guarantee = request.form['warranties_or_guarantee']
    POST_warranties_or_guarantee_freeform = request.form['warranties_or_guarantee_freeform']
    POST_warranties_or_guarantee_freeform = POST_warranties_or_guarantee_freeform.replace("'", "")
    POST_warranties_or_guarantee_freeform = POST_warranties_or_guarantee_freeform.replace('"', "")
    POST_num_skus = request.form['num_skus']
    POST_level_of_customization = request.form['level_of_customization']
    POST_pid = str(request.form['p_id'])

    print(POST_complexity + " " + POST_price + " " + POST_product_or_service + " " + POST_frequency_of_use + " " + POST_frequency_of_purchase + " " + POST_value_prop + " " + POST_warranties_or_guarantee + " " + POST_warranties_or_guarantee_freeform + " " + POST_num_skus + " " + POST_level_of_customization + " " + POST_product_or_service)

    query = """UPDATE dbo.product_list
                    SET complexity = '""" + POST_complexity + """', price = '""" + POST_price + """', product_or_service = '""" + POST_product_or_service + """', frequency_of_use = '""" + POST_frequency_of_use + """', frequency_of_purchase = '""" + POST_frequency_of_purchase + """', value_prop = '""" + POST_value_prop + """', warranties_or_guarantee = '""" + POST_warranties_or_guarantee + """', warranty_guarantee_freeform = '""" + POST_warranties_or_guarantee_freeform + """', num_skus = '""" + POST_num_skus + """', level_of_customization = '""" + POST_level_of_customization + """'
                    WHERE p_id = """ + POST_pid + """;commit;"""

    print(query)

    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()
    last_modified(str(session['user']))

    return "success"

@app.route('/competitors/company/audience/product/product_2/salescycle', methods=['GET', 'POST'])
def salescycle():

    if session.get('logged_in'):
        return render_template('intake/salescycle.html')
    else:
        return logout()  



@app.route('/nice', methods=['POST'])
def nice():
    d = request.form
    d = d.to_dict()
    for key, value in d.items():
        if value != "":
            if key[:9] == "awareness":
                query = "INSERT INTO dbo.awareness (customer_id, tactic) VALUES (" + str(session['user']) + ",'" + value + "');commit"
                cursor = db.cursor()
                cursor.execute(query)
                cursor.close()
                print(key + " " + query)
                
            elif key[:10] == "evaluation":
                query = "INSERT INTO dbo.evaluation (customer_id, tactic) VALUES (" + str(session['user']) + ",'" + value + "');commit"
                cursor = db.cursor()
                cursor.execute(query)
                cursor.close()
                print(key + " " + query)
                
            elif key[:10] == "conversion":
                query = "INSERT INTO dbo.conversion (customer_id, tactic) VALUES (" + str(session['user']) + ",'" + value + "');commit"
                cursor = db.cursor()
                cursor.execute(query)
                cursor.close()
                print(key + " " + query)
                
            elif key[:9] == "retention":
                query = "INSERT INTO dbo.retention (customer_id, tactic) VALUES (" + str(session['user']) + ",'" + value + "');commit"
                cursor = db.cursor()
                cursor.execute(query)
                cursor.close()
                print(key + " " + query)
                
            elif key[:8] == "referral":
                query = "INSERT INTO dbo.referral (customer_id, tactic) VALUES (" + str(session['user']) + ",'" + value + "');commit"
                cursor = db.cursor()
                cursor.execute(query)
                cursor.close()
                print(key + " " + query)

    return render_template('intake/nice.html')







#############intake/2###############

@app.route('/goals')
def goals():
    return render_template('intake/2/goals.html')

@app.route('/history', methods=['GET','POST'])
def history():
    if not request.form:
        print('should work')
    elif request.form:
        POST_goal = str(request.form['goal'])
        POST_current_avg = str(request.form['current_avg'])
        POST_target_avg = str(request.form['target_avg'])
        POST_timeframe = str(request.form['timeframe'])

        query = "INSERT INTO dbo.goals (customer_id, goal,current_avg,target_avg,timeframe) VALUES (" + str(session['user']) + ",'" + POST_goal + "', '" + POST_current_avg + "', '" + POST_target_avg + "', '" + POST_timeframe + "');commit;"
        print(query)
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
        last_modified(str(session['user']))
    if session.get('logged_in'):
        return render_template('intake/2/history.html')
    else:
        return logout()  



@app.route('/history/platforms', methods=['GET','POST'])
def platforms():
    if not request.form:
        print('should work')
    elif request.form:
        POST_facebook = str(request.form['facebook'])
        POST_google = str(request.form['google'])
        POST_bing = str(request.form['bing'])
        POST_twitter = str(request.form['twitter'])
        POST_instagram = str(request.form['instagram'])
        POST_yelp = str(request.form['yelp'])
        POST_linkedin = str(request.form['linkedin'])
        POST_amazon = str(request.form['amazon'])
        POST_snapchat = str(request.form['snapchat'])
        POST_youtube = str(request.form['youtube'])
        POST_none = str(request.form['none'])

        query = "INSERT INTO dbo.history (facebook, google, bing, twitter, instagram, yelp, linkedin, amazon, snapchat, youtube, customer_id, none) VALUES ('" + POST_facebook + "', '" + POST_google + "', '" + POST_bing + "', '" + POST_twitter + "', '" + POST_instagram + "', '" + POST_yelp + "', '" + POST_linkedin + "', '" + POST_amazon + "', '" + POST_snapchat + "', '" + POST_youtube + "', " + str(session['user']) + ", '" + POST_none + "');commit;"
        print(query)
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
        last_modified(str(session['user']))
    if session.get('logged_in'):
        return render_template('intake/2/platforms.html')
    else:
        return logout()  



@app.route('/load_history', methods=['GET'])
def load_history():
    results = sql_to_df("SELECT * FROM dbo.history WHERE customer_id = " + str(session['user']))
    results = results.to_json(orient='split')
    return results

@app.route('/history/platforms/past', methods=['GET','POST'])
def past():
    if not request.form:
        print('should work')
    elif request.form:

        req = request.form
        d = pd.DataFrame(list(req.items()))
        # test = list(d.iloc[:,1])
        q = 0

        cursor = db.cursor()
        query = "UPDATE dbo.history SET digital_spend = '" + str(d.iloc[-1,1]) + "' WHERE customer_id = " + str(session['user']) + ";commit;"
        cursor.execute(query)
        cursor.close()
        last_modified(str(session['user']))
        print(d.iloc[-1,1])
        #print(d.iloc[0:3,:])

        s = 0
        f = 3
        while q < (len(request.form) - 1):
            if q%3 == 0:
                this = d.iloc[s:f,:]
                
                # print(this.iloc[0,1])
                # print(this.iloc[1,1])
                # print(this.iloc[2,1])

                query = "INSERT INTO dbo.platforms (customer_id,platform_name,currently_using,results) VALUES (" + str(session['user']) + ", '" + this.iloc[0,1] + "', '" + this.iloc[1,1] + "', " + str(this.iloc[2,1]) + ");commit;"
                cursor = db.cursor()
                cursor.execute(query)
                cursor.close()
                print(query)



            s += 1
            f += 1
            q += 1

    return render_template('intake/2/past.html')

@app.route('/history/platforms/past/done', methods=['GET', 'POST'])
def end_intake():
    POST_history_freeform = str(request.form['history_freeform'])

    query = "UPDATE dbo.history SET history_freeform = '" + POST_history_freeform + "' WHERE customer_id = " + str(session['user']) + ";commit"

    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()
    last_modified(str(session['user']))

    return redirect(url_for('index'))


