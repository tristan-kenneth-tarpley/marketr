from app import *
from core_routes import *
from helpers import *


@app.route('/splash', methods=['POST', 'GET'])
def splash():

    text = "test splash"
    next_page = request.args.get('next_step')

    return render_template('intake/splash.html', next_step=next_page, text=text)



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

        if POST_comp_1_name:
            cursor = db.cursor()
            cursor.execute(query)
            cursor.close()
            last_modified(str(session['user']))
        else:
            print('nothing to see here')

    if session.get('logged_in'):
        if request.form:
            return redirect(url_for('splash', next_step='competitors/company'))
        else:
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



@app.route('/nice', methods=['POST', 'GET'])
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

    return redirect(url_for('splash', next_step='/goals'))







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
