from app import *
from core_routes import *
from helpers import *
from classes import *
from flask import jsonify
import json


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for('login_page'))

    return wrap

@app.route('/cities', methods=['GET'])
def cities():
    if request.method == "GET":
        with open('data/cities.json') as json_file:  
            data = json.load(json_file)
            return json.dumps(data)

@app.route('/industries', methods=['GET'])
def industries():
    if request.method == 'GET':
        with open('data/industries.json') as json_file:
            data = json.load(json_file)
            return json.dumps(data)

@app.route('/stages', methods=['GET'])
def stages():
    if request.method == 'GET':
        with open('data/salescycle.json') as json_file:
            data = json.load(json_file)
            return json.dumps(data)

def get_first_audience(user):
    try:
        query = f"SELECT persona_name, audience_id FROM dbo.audience WHERE customer_id = {session['user']}"
        names_and_ids, cursor = execute(query, True)
        names_and_ids = cursor.fetchall()
        first_id = names_and_ids[0][1]
        session['first_id'] = first_id
        cursor.close()
        return names_and_ids
    except:
        session['first_id'] = None
        return False



@app.route('/splash', methods=['POST', 'GET'])
def splash():
    prev_step = request.args.get('prev_step')
    next_step = request.args.get('next_step')
    redirect = request.args.get('redirect')
    query = f"SELECT heading, paragraph FROM dbo.splash WHERE after_page = '{next_step}'"
    data, cursor = execute(query, True)
    heading, paragraph = cursor.fetchone()
    heading = heading.replace("`", "'")
    paragraph = paragraph.replace("`", "'")

    cursor.close()
    if redirect:
        return render_template('intake/splash.html', redirect=redirect, prev_step=prev_step, next_step=next_step, heading=heading, paragraph=paragraph)
    else:
        return render_template('intake/splash.html', next_step=next_step, heading=heading, paragraph=paragraph)




@app.route('/competitors', methods=['POST','GET'])
@login_required
def competitors():
    if request.form:

        POST_first_name = str(request.form['first_name'])
        POST_last_name = str(request.form['last_name'])
        POST_company_name = str(request.form['company_name'])
        POST_revenue = str(request.form['revenue'])
        POST_zip = str(request.form['zip'])
        POST_stage = str(request.form['stage'])
        POST_employees = str(request.form['employees'])

        try:
            zips = zipcodes.matching(POST_zip)
            POST_city = zips[0]['city']
            POST_state = zips[0]['state']
        except TypeError:
            POST_city = "not defined"
            POST_state = "not defined"
            POST_zip = "00000"



        query = f"""UPDATE dbo.customer_basic 
                    SET first_name = '{POST_first_name}', last_name = '{POST_last_name}', company_name = '{POST_company_name}', revenue = '{POST_revenue}', city = '{POST_city}', state = '{POST_state}', stage = '{POST_stage}', employees = '{POST_employees}', zip = {str(POST_zip)} 
                    WHERE dbo.customer_basic.ID = '{session['user']}'; commit;"""

        if POST_first_name:
            execute(query, False)

            last_modified(str(session['user']))


    if request.args.get('splash'):
        return render_template('intake/competitors.html')
    else:
        return redirect(url_for("splash", next_step="competitors"))





@app.route('/competitors/company', methods=['POST', 'GET'])
@login_required
def company():
    if request.form:
        POST_industry = str(request.form['industry'])
        POST_comp_1_name = str(request.form['comp_1_name'])
        POST_comp_1_website = str(request.form['comp_1_website'])
        POST_comp_1_type = str(request.form['comp_1_type'])
        POST_comp_2_name = str(request.form['comp_2_name'])
        POST_comp_2_website = str(request.form['comp_2_website'])
        POST_comp_2_type = str(request.form['comp_2_type'])

        if is_started('competitors', session['user']):
            query = f"""UPDATE dbo.competitors
                        SET customer_id = '{str(session['user'])}', industry = '{POST_industry}', comp_1_name = '{POST_comp_1_name}', comp_1_website = '{POST_comp_1_website}', comp_1_type = '{POST_comp_1_type}', comp_2_name = '{POST_comp_2_name}', comp_2_website = '{POST_comp_2_website}', comp_2_type = '{POST_comp_2_type}'
                        WHERE customer_id = '{str(session['user'])}';commit;"""
        else:                
            query = """INSERT INTO dbo.competitors 
                    (customer_id, industry, comp_1_name, comp_1_website, comp_1_type, comp_2_name, comp_2_website, comp_2_type)
                    VALUES ('""" + str(session['user']) + """','""" + POST_industry + """','""" + POST_comp_1_name + """','""" + POST_comp_1_website + """','""" + POST_comp_1_type + """','""" + POST_comp_2_name + """','""" + POST_comp_2_website + """','""" + POST_comp_2_type + """');commit;""" 
        

        if POST_comp_1_name:
            execute(query, False)
            last_modified(str(session['user']))



    if request.form:
        if request.args.get('splash'):
            return render_template('intake/company.html')
        else:
            return redirect(url_for("splash", next_step="company"))
    else:
        return render_template('intake/company.html')


@app.route('/competitors/company/audience', methods=['POST', 'GET'])
@login_required
def audience():
    if request.form:
        POST_selling_to = str(request.form['selling_to'])
        POST_biz_model = str(request.form['biz_model'])
        POST_storefront_perc = str(request.form['storefront_perc'])
        POST_direct_perc = str(request.form['direct_perc'])
        POST_online_perc = str(request.form['online_perc'])
        POST_tradeshows_perc = str(request.form['tradeshows_perc'])
        POST_other_perc = str(request.form['other_perc'])
        POST_freeform = str(request.form['rev_channel_freeform'])
        POST_freeform = POST_freeform.replace("'", "")
        POST_freeform = POST_freeform.replace('"', "")



        if is_started('company', session['user']):
            query = f"""UPDATE dbo.company
                        SET customer_id = '{str(session['user'])}', selling_to = '{POST_selling_to}', biz_model = '{POST_biz_model}', rev_channel_freeform = '{POST_freeform}', storefront_perc = '{POST_storefront_perc}', direct_perc = '{POST_direct_perc}', online_perc = '{POST_online_perc}', tradeshows_perc = '{POST_tradeshows_perc}', other_perc = '{POST_other_perc}'
                        WHERE customer_id = '{str(session['user'])}';commit;"""
        else:                
            query = f"""INSERT INTO dbo.company
                    (customer_id, selling_to, biz_model, rev_channel_freeform, storefront_perc, direct_perc, online_perc, tradeshows_perc, other_perc)
                    VALUES ('""" + str(session['user']) + """','""" + POST_selling_to + """','""" + POST_biz_model + """', '""" + POST_freeform + """','""" + POST_storefront_perc + """','""" +  POST_direct_perc + """','""" +  POST_online_perc + """','""" +  POST_tradeshows_perc + """','""" +  POST_other_perc + """');commit;"""

        execute(query, False)
        last_modified(str(session['user']))


    if 'redirect' in request.args:

        names_and_ids = get_first_audience(session['user'])
        if names_and_ids == False:
                # come back
            init_audience(session['user']) 
            first_persona, cursor = execute(f"SELECT TOP 1 audience_id FROM dbo.audience WHERE customer_id = {session['user']}", True)
            first_persona = cursor.fetchone()
            print(first_persona)
            cursor.close()
        else:
            first_persona, cursor = execute(f"SELECT TOP 1 audience_id FROM dbo.audience WHERE customer_id = {session['user']}", True)
            first_persona = cursor.fetchone()
            first_persona = first_persona[0]
            cursor.close()


        me = User(session['user'])
        page = 'audience'
        hide_1 = me.hide(page, 1, 'selling_to')
        
        return render_template('intake/audience.html', persona_id=first_persona, names_and_ids = names_and_ids, hide_1=hide_1)

    else:
        return redirect(url_for("splash", next_step="audience", prev_step="company", redirect=True))





@app.route('/competitors/company/audience/product', methods=['POST', 'GET'])
@login_required
def product():
    if request.form:

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
        POST_formality = str(request.form['formality'])
        POST_buying_for = str(request.form['buying_for'])
        POST_tech_savvy = str(request.form['tech_savvy'])
        POST_decision_making = str(request.form['decision_making'])
        POST_decision_making = POST_decision_making.replace("'", "")
        POST_details = str(request.form['details'])
        POST_motive = str(request.form['motive'])
        POST_persona_name = str(request.form['persona_name'])

        session['hide'] = False

        if request.form['submit_button'] == '+ ADD ANOTHER PERSONA':
            init_audience(session['user'])
            query = f"SELECT TOP 2 audience_id FROM dbo.audience WHERE customer_id = {session['user']} ORDER BY audience_id desc"
            data, cursor = execute(query, True)
            data = cursor.fetchall()
            next_audience_id = data[0][0]
            current_audience_id = data[1][0]
            session['current_audience_id'] = current_audience_id
            cursor.close()

            query = f"""UPDATE dbo.audience
                        SET formality = '{POST_formality}', buying_for = '{POST_buying_for}', tech_savvy = '{POST_tech_savvy}', decision_making = '{POST_decision_making}', details = '{POST_details}', motive = '{POST_motive}', customer_id = '{session['user']}', gender = '{POST_gender}', age_group_1 = '{POST_age_group_1}', age_group_2 = '{POST_age_group_2}', age_group_3 = '{POST_age_group_3}', age_group_4 = '{POST_age_group_4}', age_group_5 = '{POST_age_group_5}', age_group_6 = '{POST_age_group_6}', age_group_7 = '{POST_age_group_7}', age_group_8 = '{POST_age_group_8}', location = '{POST_location}', why = '{POST_why}', before_1 = '{POST_before_1}', before_2 = '{POST_before_2}', before_3 = '{POST_before_3}', before_4 = '{POST_before_4}', before_5 = '{POST_before_5}', before_6 = '{POST_before_6}', before_7 = '{POST_before_7}', before_8 = '{POST_before_8}', before_9 = '{POST_before_9}', before_10 = '{POST_before_10}', before_freeform = '{POST_before_freeform}', after_1 = '{POST_after_1}', after_2 = '{POST_after_2}', after_3 = '{POST_after_3}', after_4 = '{POST_after_4}', after_5 = '{POST_after_5}', after_6 = '{POST_after_6}', after_7 = '{POST_after_7}', after_8 = '{POST_after_8}', after_9 = '{POST_after_9}', after_10 = '{POST_after_10}', after_freeform = '{POST_after_freeform}', persona_name = '{POST_persona_name}'
                        WHERE customer_id = '{session['user']}' AND audience_id = {current_audience_id}; commit;"""
 
            session['hide'] = True

            execute(query, False)

            return redirect(url_for('audience', redirect=True, hide=session['hide'], persona_id = next_audience_id))

        else:
            query = f"""UPDATE dbo.audience
                        SET customer_id =  '{str(session['user'])}', formality = '{POST_formality}', buying_for = '{POST_buying_for}', tech_savvy = '{POST_tech_savvy}', decision_making = '{POST_decision_making}', details = '{POST_details}', motive = '{POST_motive}', gender = '{POST_gender}', age_group_1 = '{POST_age_group_1}', age_group_2 = '{POST_age_group_2}', age_group_3 = '{POST_age_group_3}', age_group_4 = '{POST_age_group_4}', age_group_5 = '{POST_age_group_5}', age_group_6 = '{POST_age_group_6}', age_group_7 = '{POST_age_group_7}', age_group_8 = '{POST_age_group_8}', location = '{POST_location}', why = '{POST_why}', before_1 = '{POST_before_1}', before_2 = '{POST_before_2}', before_3 = '{POST_before_3}', before_4 = '{POST_before_4}', before_5 = '{POST_before_5}', before_6 = '{POST_before_6}', before_7 = '{POST_before_7}', before_8 = '{POST_before_8}', before_9 = '{POST_before_9}', before_10 = '{POST_before_10}', before_freeform = '{POST_before_freeform}', after_1 = '{POST_after_1}', after_2 = '{POST_after_2}', after_3 = '{POST_after_3}', after_4 = '{POST_after_4}', after_5 = '{POST_after_5}', after_6 = '{POST_after_6}', after_7 = '{POST_after_7}', after_8 = '{POST_after_8}', after_9 = '{POST_after_9}', after_10 = '{POST_after_10}', after_freeform = '{POST_after_freeform}', persona_name = '{POST_persona_name}'
                        WHERE customer_id = '{str(session['user'])}' AND audience_id = {session['current_audience_id']};commit;"""

        if POST_gender:
            execute(query, False)
            last_modified(str(session['user']))


    if 'redirect' in request.args:
        me = User(session['user'])
        page = 'product'
        hide_1 = me.hide(page, 1, 'biz_model')
        hide_2 = me.hide(page, 2, 'biz_model')
        mask_3, mask_3_bool = me.mask(page, 3, 'biz_model')
        mask_4, mask_4_bool = me.mask(page, 4, 'biz_model')
        mask_5, mask_5_bool = me.mask(page, 5, 'biz_model')
        mask_6, mask_6_bool = me.mask(page, 6, 'biz_model')
        mask_7, mask_7_bool = me.mask(page, 7, 'biz_model')
        hide_8 = me.hide(page, 8, 'biz_model')
        hide_9 = me.hide(page, 9, 'biz_model')
        hide_10 = me.hide(page, 10, 'biz_model')
        hide_11 = me.hide(page, 11, 'biz_model')
        mask_12, mask_12_bool = me.mask(page, 12, 'biz_model')
        return render_template('intake/product.html', hide_1=hide_1, hide_2=hide_2, mask_3=mask_3, mask_3_bool=mask_3_bool, mask_4=mask_4, mask_5=mask_5, mask_6=mask_6, mask_7=mask_7, mask_7_bool=mask_7_bool, hide_8=hide_8, hide_9=hide_9, hide_10=hide_10, hide_11=hide_11, mask_12=mask_12,mask_12_bool=mask_12_bool)
    else:
        return redirect(url_for("splash", next_step="product", prev_step="product", redirect=True))




@app.route('/competitors/company/audience/product/product_2', methods=['POST', 'GET'])
@login_required
def product_2():
    if request.form:
        POST_gen_description = str(request.form['gen_description'])
        POST_gen_description = POST_gen_description.replace("'", "")
        POST_gen_description = POST_gen_description.replace('"', "")
        POST_quantity = str(request.form['quantity'])
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


        if is_started('product', session['user']):
            query = f"""UPDATE dbo.product
                        SET gen_description = '{POST_gen_description}',quantity = '{POST_quantity}', link = '{POST_link}',segment_1 = '{POST_segment_1}',segment_2 = '{POST_segment_2}',segment_3 = '{POST_segment_3}',segment_4 = '{POST_segment_4}',segment_5 = '{POST_segment_5}',segment_6 = '{POST_segment_6}',segment_7 = '{POST_segment_7}',segment_8 = '{POST_segment_8}',segment_9 = '{POST_segment_9}',segment_10 = '{POST_segment_10}',source_1 = '{POST_source_1}',source_2 = '{POST_source_2}',source_3 = '{POST_source_3}',source_4 = '{POST_source_4}',source_freeform = '{POST_source_freeform}'
                        WHERE customer_id = {session['user']}"""
        else:
            query = """INSERT INTO dbo.product
                    (customer_id,gen_description,quantity,link,segment_1,segment_2,segment_3,segment_4,segment_5,segment_6,segment_7,segment_8,segment_9,segment_10,source_1,source_2,source_3,source_4,source_freeform)
                    VALUES ('""" + str(session['user']) + """' , '""" + POST_gen_description + """','""" + POST_quantity + """','""" + POST_link + """','""" + POST_segment_1 + """','""" + POST_segment_2 + """','""" + POST_segment_3 + """','""" + POST_segment_4 + """','""" + POST_segment_5 + """','""" + POST_segment_6 + """','""" + POST_segment_7 + """','""" + POST_segment_8 + """','""" + POST_segment_9 + """','""" + POST_segment_10 + """','""" + POST_source_1 + """','""" + POST_source_2 + """','""" + POST_source_3 + """','""" + POST_source_4 + """','""" + POST_source_freeform + """');commit;"""
           


        if POST_link:
            execute(query, False)
            last_modified(str(session['user']))



        if POST_product_1_name:
            req = request.form
            requestList = pd.DataFrame(list(req.items()))
            requestList = requestList[19:]
            print(requestList)

            product_len = int(request.form['product_len'])

            counterOne = 0
            newRequestList = {}
            for x, y in requestList.items():
                newRequestList[str(counterOne)] = y
                counterOne = counterOne+1

            productData = list(requestList.iloc[:,1])

            secondCounter = 0

            while secondCounter < product_len:
                if secondCounter > 0 and secondCounter < product_len:
                    productData = productData[7:]
                print("Product info: " + productData[0] + " " + productData[1] + " " + productData[2] + " " + productData[3] + " " + productData[5] + " " + productData[6])
                query = f"""IF NOT EXISTS (SELECT name FROM dbo.product_list WHERE name = '{productData[0]}' AND customer_id = {session['user']})
                            INSERT INTO dbo.product_list (customer_id,name,category,cogs,sales_price,price_model,qty_sold,est_unique_buyers) VALUES ('{session['user']}','{str(productData[0])}','{str(productData[1])}','{str(productData[2])}','{str(productData[3])}','{str(productData[4])}','{str(productData[5])}','{str(productData[6])}');commit;"""

                execute(query, False)
                secondCounter += 1

            last_modified(str(session['user']))


    me = User(session['user'])
    me.set_biz_model()

    if me.biz_model != 'Affiliate' and me.biz_model != 'Media Provider':
        page = 'product_2'

        hide_1 = me.hide(page,1, 'biz_model')
        hide_2 = me.hide(page,2, 'biz_model')

        return render_template('intake/product_2.html', hide_1=hide_1, hide_2=hide_2)
    else:
        return redirect(url_for('splash', next_step='salescycle'))


@app.route('/load_product_list', methods=['GET', 'POST'])
@login_required
def load_product_list():
    query = "SELECT p_id, name, category FROM dbo.product_list WHERE customer_id = " + str(session['user'])

    results = sql_to_df(query)
    results = results.to_json(orient='records')


    return results


@app.route('/product_submit', methods=['POST'])
@login_required
def product_submit():
    if request.form:
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
        query = """UPDATE dbo.product_list
                    SET complexity = '""" + POST_complexity + """', price = '""" + POST_price + """', product_or_service = '""" + POST_product_or_service + """', frequency_of_use = '""" + POST_frequency_of_use + """', frequency_of_purchase = '""" + POST_frequency_of_purchase + """', value_prop = '""" + POST_value_prop + """', warranties_or_guarantee = '""" + POST_warranties_or_guarantee + """', warranty_guarantee_freeform = '""" + POST_warranties_or_guarantee_freeform + """', num_skus = '""" + POST_num_skus + """', level_of_customization = '""" + POST_level_of_customization + """'
                    WHERE p_id = """ + POST_pid + """;commit;"""

        execute(query, False)
    last_modified(str(session['user']))

    return "success"

@app.route('/competitors/company/audience/product/product_2/salescycle', methods=['GET', 'POST'])
@login_required
def salescycle():
    return render_template('intake/salescycle.html')




@app.route('/nice', methods=['POST', 'GET'])
@login_required
def nice():
    d = request.form
    d = d.to_dict()
    for key, value in d.items():
        if value != "":
            if key[:9] == "awareness":
                stage = "awareness"
                
            elif key[:10] == "evaluation":
                stage = "evaluation"
                
            elif key[:10] == "conversion":
                stage = "conversion"
                
            elif key[:9] == "retention":
                stage = "retention"
                
            elif key[:8] == "referral":
                stage = "referral"

            query = f"""IF NOT EXISTS (SELECT tactic from dbo.{stage} WHERE customer_id = {session['user']} AND tactic = '{value}')
            INSERT INTO dbo.{stage}(customer_id, tactic) values ({session['user']}, '{value}');commit;"""

            execute(query, False)

    return redirect(url_for('splash', next_step='goals'))







#############intake/2###############

@app.route('/goals')
@login_required
def goals():
    me = User(session['user'])
    page = 'goals'
    hide_1 = me.hide(page, 1, 'biz_model')

    return render_template('intake/2/goals.html', hide_1=hide_1)

@app.route('/history', methods=['GET','POST'])
@login_required
def history():
    if request.form:
        POST_goal = str(request.form['goal'])
        POST_current_avg = str(request.form['current_avg'])
        POST_target_avg = str(request.form['target_avg'])
        POST_timeframe = str(request.form['timeframe'])

        if is_started('goals', session['user']):
            query = f"""UPDATE dbo.goals
                        SET customer_id = '{str(session['user'])}', goal = '{POST_goal}', current_avg = '{POST_current_avg}', target_avg = '{POST_target_avg}', timeframe = '{POST_timeframe}'
                        WHERE customer_id = '{str(session['user'])}';commit;"""
        else:                
            query = "INSERT INTO dbo.goals (customer_id, goal,current_avg,target_avg,timeframe) VALUES (" + str(session['user']) + ",'" + POST_goal + "', '" + POST_current_avg + "', '" + POST_target_avg + "', '" + POST_timeframe + "');commit;"

        execute(query, False)
        last_modified(str(session['user']))
    return render_template('intake/2/history.html')




@app.route('/history/platforms', methods=['GET','POST'])
@login_required
def platforms():
    if request.form:
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

        if is_started('history', session['user']):
            query = f""" UPDATE dbo.goals
                        SET customer_id = {session['user']}, facebook = '{POST_facebook}', google = '{POST_google}', bing = '{POST_bing}', twitter = '{POST_twitter}', instagram = '{POST_instagram}', yelp = '{POST_yelp}', linkedin = '{POST_linkedin}', amazon = '{POST_amazon}', snapchat = '{POST_snapchat}', youtube = '{POST_youtube}', none = '{POST_none}'
                        ;commit;"""
        else:
            query = "INSERT INTO dbo.history (facebook, google, bing, twitter, instagram, yelp, linkedin, amazon, snapchat, youtube, customer_id, none) VALUES ('" + POST_facebook + "', '" + POST_google + "', '" + POST_bing + "', '" + POST_twitter + "', '" + POST_instagram + "', '" + POST_yelp + "', '" + POST_linkedin + "', '" + POST_amazon + "', '" + POST_snapchat + "', '" + POST_youtube + "', " + str(session['user']) + ", '" + POST_none + "');commit;"
        
        execute(query, False)
        last_modified(str(session['user']))

    return render_template('intake/2/platforms.html')




@app.route('/load_history', methods=['GET'])
@login_required
def load_history():
    results = sql_to_df("SELECT * FROM dbo.history WHERE customer_id = " + str(session['user']))
    results = results.to_json(orient='split')
    return results

@app.route('/history/platforms/past', methods=['GET','POST'])
@login_required
def past():
    if request.form:

        req = request.form
        d = pd.DataFrame(list(req.items()))
        q = 0

        query = "UPDATE dbo.history SET digital_spend = '" + str(d.iloc[-1,1]) + "' WHERE customer_id = " + str(session['user']) + ";commit;"
        execute(query, False)
        last_modified(str(session['user']))

        s = 0
        f = 3
        while q < (len(request.form) - 1):
            if q%3 == 0:
                this = d.iloc[s:f,:]

                query = "INSERT INTO dbo.platforms (customer_id,platform_name,currently_using,results) VALUES (" + str(session['user']) + ", '" + this.iloc[0,1] + "', '" + this.iloc[1,1] + "', " + str(this.iloc[2,1]) + ");commit;"
                execute(query, False)



            s += 1
            f += 1
            q += 1

    return render_template('intake/2/past.html')

@app.route('/history/platforms/past/done', methods=['GET', 'POST'])
@login_required
def history_freeform():
    POST_history_freeform = str(request.form['history_freeform'])

    query = "UPDATE dbo.history SET history_freeform = '" + POST_history_freeform + "' WHERE customer_id = " + str(session['user']) + ";commit"

    execute(query, False)
    last_modified(str(session['user']))

    return redirect(url_for('creative'))



photos = UploadSet('photos', IMAGES)
filepath = 'static/uploads/img'

app.config['UPLOADED_PHOTOS_DEST'] = filepath
configure_uploads(app, photos)

@app.route('/creative', methods=['GET', 'POST'])
@login_required
def creative():
    next_query = f"SELECT file_path FROM dbo.assets WHERE customer_id = {session['user']}"
    data, cursor = execute(next_query, True)
    data = cursor.fetchall()
    cursor.close()
    if len(data) > 0:
        data = data
    else:
        data = None

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = filepath + "/" + filename

        query = f"""IF NOT EXISTS (SELECT asset_name from dbo.assets WHERE customer_id = {session['user']} and asset_name = '{filename}')
                        INSERT INTO dbo.assets(customer_id,
                                    asset_name,
                                    asset_type, 
                                    file_path)
                        VALUES ({session['user']}, '{filename}', 'photo', '{path}');commit;"""
        execute(query, False)

        next_query = f"SELECT file_path FROM dbo.assets WHERE customer_id = {session['user']}"
        data, cursor = execute(next_query, True)
        data = cursor.fetchall()

        return render_template('intake/creative.html', images=data)

    return render_template('intake/creative.html', images=data)






######helper routes########


@app.route('/load_past_inputs', methods=['GET'])
@login_required
def load_past_inputs():

    page = request.args.get('page')
    page = page.replace("/", " ")
    *first, page = page.split()

    if page == "audience":
        if request.args.get('persona_id'):
            persona_id = request.args.get('persona_id')
            session['current_audience_id'] = persona_id
        else:
            persona_id = session['first_id']
            session['current_audience_id'] = persona_id
    else:
        persona_id = "0"

    try:
        result = past_inputs(page, session['user'], persona_id)
        result = result.to_json(orient='records')
        return result

    except AttributeError:
        return 'nah'
    except KeyError:
        return 'nah'






