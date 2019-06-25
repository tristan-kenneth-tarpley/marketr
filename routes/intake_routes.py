from app import *
from routes.core_routes import *
from helpers.helpers import *
from helpers.classes import *
from flask import jsonify
from bleach import clean
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

@app.route('/areas', methods=['GET'])
def cities():
    if request.method == "GET":
        with open('data/areas.json') as json_file:  
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
        tup = (session['user'],)
        query = "SELECT persona_name, audience_id FROM dbo.audience WHERE customer_id = ?"
        names_and_ids, cursor = execute(query, True, tup)
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
    next_step = clean(next_step)
    redirect = request.args.get('redirect')
    tup = (next_step,)
    query = "SELECT heading, paragraph FROM dbo.splash WHERE after_page = ?"
    data, cursor = execute(query, True, tup)
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
        POST_website = clean(request.form['website'])
        POST_first_name = clean(request.form['first_name'])
        POST_last_name = clean(request.form['last_name'])
        POST_company_name = clean(request.form['company_name'])
        POST_revenue = clean(request.form['revenue'])
        POST_zip = clean(request.form['zip'])
        POST_stage = clean(request.form['stage'])
        POST_employees = clean(request.form['employees'])

        try:
            zips = zipcodes.matching(POST_zip)
            POST_city = zips[0]['city']
            POST_state = zips[0]['state']
        except:
            POST_city = "not defined"
            POST_state = "not defined"
            POST_zip = "00000"

        tup = (POST_first_name, POST_last_name, POST_company_name, POST_revenue, POST_city, POST_state, POST_stage, POST_employees, POST_zip, POST_website, session['user'])

        query = """UPDATE dbo.customer_basic 
                    SET first_name = ?, last_name = ?, company_name = ?, revenue = ?, city = ?, state = ?, stage = ?, employees = ?, zip = ?, website = ?
                    WHERE dbo.customer_basic.ID = ?; commit;"""

        if POST_first_name:
            execute(query, False, tup)

            last_modified(str(session['user']))

    if request.args.get('splash') and not request.args.get('coming_home'):
        return render_template('intake/competitors.html')
    elif request.args.get('coming_home'):
        return redirect(url_for('home'))
    elif not request.args.get('splash'):
        return render_template('intake/competitors.html')
    else:
        return redirect(url_for("splash", next_step="competitors"))





@app.route('/competitors/company', methods=['POST', 'GET'])
@login_required
def company():
    if request.form:
        POST_industry = clean(request.form['industry'])
        POST_comp_1_name = clean(request.form['comp_1_name'])
        POST_comp_1_website = clean(request.form['comp_1_website'])
        POST_comp_1_type = clean(request.form['comp_1_type'])
        POST_comp_2_name = clean(request.form['comp_2_name'])
        POST_comp_2_website = clean(request.form['comp_2_website'])
        POST_comp_2_type = clean(request.form['comp_2_type'])

        if is_started('competitors', session['user']):
            tup = (session['user'], POST_industry, POST_comp_1_name, POST_comp_1_website, POST_comp_1_type, POST_comp_2_name, POST_comp_2_website, POST_comp_2_type, session['user'])
            query = """UPDATE dbo.competitors
                        SET customer_id = ?, industry = ?, comp_1_name = ?, comp_1_website = ?, comp_1_type = ?, comp_2_name = ?, comp_2_website = ?, comp_2_type = ?
                        WHERE customer_id = ?;commit;"""
        else:           
            tup = (session['user'], POST_industry, POST_comp_1_name, POST_comp_1_website, POST_comp_1_type, POST_comp_2_name, POST_comp_2_website, POST_comp_2_type)     
            query = """INSERT INTO dbo.competitors 
                    (customer_id, industry, comp_1_name, comp_1_website, comp_1_type, comp_2_name, comp_2_website, comp_2_type)
                    VALUES (?,?,?,?,?,?,?,?);commit;""" 
        

        if POST_comp_1_name:
            execute(query, False, tup)
            last_modified(str(session['user']))



    if request.form:
        if request.args.get('splash'):
            return render_template('intake/company.html')
        elif request.args.get('coming_home'):
            return redirect(url_for('home'))
        else:
            return redirect(url_for("splash", next_step="company"))
    else:
        return render_template('intake/company.html')



@app.route("/remove/<persona_id>", methods=['GET', 'POST'])
@login_required
def removePersona(persona_id):
    query = "DELETE FROM dbo.audience WHERE audience_id=? and customer_id=?;commit;"
    tup = (persona_id, session['user'])

    execute(query, False, tup)

    return_id = "SELECT TOP 1 audience_id FROM dbo.audience WHERE customer_id = ?"
    tup = (session['user'])
    data, cursor = execute(return_id, True, tup)

    data = cursor.fetchone()
    return_persona = data[0]
    cursor.close()

    return redirect(url_for('audience', redirect=True, persona_id=return_persona))



@app.route('/competitors/company/audience', methods=['POST', 'GET'])
@login_required
def audience():
    if request.form:
        POST_selling_to = clean(request.form['selling_to'])
        POST_biz_model = clean(request.form['biz_model'])
        POST_storefront_perc = clean(request.form['storefront_perc'])
        POST_direct_perc = clean(request.form['direct_perc'])
        POST_online_perc = clean(request.form['online_perc'])
        POST_tradeshows_perc = clean(request.form['tradeshows_perc'])
        POST_other_perc = clean(request.form['other_perc'])
        POST_freeform = clean(request.form['rev_channel_freeform'])
        POST_freeform = POST_freeform.replace("'", "")
        POST_freeform = POST_freeform.replace('"', "")



        if is_started('company', session['user']):
            tup = (session['user'], POST_selling_to, POST_biz_model, POST_freeform, POST_storefront_perc, POST_direct_perc, POST_online_perc, POST_tradeshows_perc, POST_other_perc, session['user'])
            query = """UPDATE dbo.company
                        SET customer_id = ?, selling_to = ?, biz_model = ?, rev_channel_freeform = ?, storefront_perc = ?, direct_perc = ?, online_perc = ?, tradeshows_perc = ?, other_perc = ?
                        WHERE customer_id = ?;commit;"""
        else:             
            tup = (session['user'], POST_selling_to, POST_biz_model, POST_freeform, POST_storefront_perc, POST_direct_perc, POST_online_perc, POST_tradeshows_perc, POST_other_perc)
            query = """INSERT INTO dbo.company
                    (customer_id, selling_to, biz_model, rev_channel_freeform, storefront_perc, direct_perc, online_perc, tradeshows_perc, other_perc)
                    VALUES (?,?,?,?,?,?,?,?,?);commit;"""

        execute(query, False, tup)
        last_modified(str(session['user']))

    if 'persona_id' in request.args:
        session['persona_id'] = request.args.get('persona_id')
    else:
        session['persona_id'] = None

    if 'redirect' in request.args:

        names_and_ids = get_first_audience(session['user'])
        if names_and_ids == False:
        
            init_audience(session['user']) 
            query = "SELECT TOP 1 audience_id FROM dbo.audience WHERE customer_id = ?"
            tup = (session['user'],)
            first_persona, cursor = execute(query, True, tup)
            first_persona = cursor.fetchone()
            cursor.close()

        else:
            tup = (session['user'],)
            query = "SELECT TOP 1 audience_id FROM dbo.audience WHERE customer_id = ?"
            first_persona, cursor = execute(query, True, tup)
            first_persona = cursor.fetchone()
            first_persona = first_persona[0]
            cursor.close()


        me = User(session['user'])
        page = 'audience'
        hide_1 = me.hide(page, 1, 'selling_to')
        
        return render_template('intake/audience.html', persona_id=first_persona, names_and_ids = names_and_ids, hide_1=hide_1)

    elif request.args.get('coming_home'):
        return redirect(url_for('home'))

    elif not request.args.get('splash'):
        names_and_ids = get_first_audience(session['user'])
        if names_and_ids == False:
       
            init_audience(session['user']) 
            query = "SELECT TOP 1 audience_id FROM dbo.audience WHERE customer_id = ?"
            tup = (session['user'],)
            first_persona, cursor = execute(query, True, tup)
            first_persona = cursor.fetchone()
            cursor.close()
        else:
            tup = (session['user'],)
            query = "SELECT TOP 1 audience_id FROM dbo.audience WHERE customer_id = ?"
            first_persona, cursor = execute(query, True, tup)
            first_persona = cursor.fetchone()
            first_persona = first_persona[0]
            cursor.close()

        me = User(session['user'])
        page = 'audience'
        hide_1 = me.hide(page, 1, 'selling_to')
        session['first_persona'] = first_persona
        
        return render_template('intake/audience.html', first_persona=session['first_persona'], persona_id=first_persona, names_and_ids = names_and_ids, hide_1=hide_1)
    else:
        return redirect(url_for("splash", next_step="audience", prev_step="company", redirect=True))





@app.route('/competitors/company/audience/product', methods=['POST', 'GET'])
@login_required
def product():
    if request.form:

        POST_gender = clean(request.form['gender'])
        POST_age_group_1 = clean(request.form['age_group_1'])
        POST_age_group_2 = clean(request.form['age_group_2'])
        POST_age_group_3 = clean(request.form['age_group_3'])
        POST_age_group_4 = clean(request.form['age_group_4'])
        POST_age_group_5 = clean(request.form['age_group_5'])
        POST_age_group_6 = clean(request.form['age_group_6'])
        POST_age_group_7 = clean(request.form['age_group_7'])
        POST_age_group_8 = clean(request.form['age_group_8'])
        POST_location = clean(request.form['location'])
        POST_why = clean(request.form['why'])
        POST_before_1 = clean(request.form['before_1'])
        POST_before_2 = clean(request.form['before_2'])
        POST_before_3 = clean(request.form['before_3'])
        POST_before_4 = clean(request.form['before_4'])
        POST_before_5 = clean(request.form['before_5'])
        POST_before_6 = clean(request.form['before_6'])
        POST_before_7 = clean(request.form['before_7'])
        POST_before_8 = clean(request.form['before_8'])
        POST_before_9 = clean(request.form['before_9'])
        POST_before_10 = clean(request.form['before_10'])
        POST_before_freeform = clean(request.form['before_freeform'])
        POST_before_freeform = POST_before_freeform.replace("'", "")
        POST_before_freeform = POST_before_freeform.replace('"', "")
        POST_after_1 = clean(request.form['after_1'])
        POST_after_2 = clean(request.form['after_2'])
        POST_after_3 = clean(request.form['after_3'])
        POST_after_4 = clean(request.form['after_4'])
        POST_after_5 = clean(request.form['after_5'])
        POST_after_6 = clean(request.form['after_6'])
        POST_after_7 = clean(request.form['after_7'])
        POST_after_8 = clean(request.form['after_8'])
        POST_after_9 = clean(request.form['after_9'])
        POST_after_10 = clean(request.form['after_10'])
        POST_after_freeform = clean(request.form['after_freeform'])
        POST_after_freeform = POST_after_freeform.replace('"', "")
        POST_after_freeform = POST_after_freeform.replace("'", "")
        POST_formality = clean(request.form['formality'])
        POST_buying_for = clean(request.form['buying_for'])
        POST_tech_savvy = clean(request.form['tech_savvy'])
        POST_decision_making = clean(request.form['decision_making'])
        POST_decision_making = POST_decision_making.replace("'", "")
        POST_details = clean(request.form['details'])
        POST_motive = clean(request.form['motive'])
        POST_persona_name = clean(request.form['persona_name'])

        session['hide'] = False


        if request.form['submit_button'] == '+ ADD ANOTHER PERSONA':
            init_audience(session['user'])
            first_tup = (session['user'],)
            query = "SELECT TOP 2 audience_id FROM dbo.audience WHERE customer_id = ? ORDER BY audience_id desc"
            data, cursor = execute(query, True, first_tup)
            data = cursor.fetchall()
            next_audience_id = data[0][0]
            current_audience_id = data[1][0]
            session['current_audience_id'] = current_audience_id
            cursor.close()
            tup = (POST_formality, POST_buying_for, POST_tech_savvy, POST_decision_making, POST_details, POST_motive, session['user'], POST_gender, POST_age_group_1, POST_age_group_2, POST_age_group_3, POST_age_group_4, POST_age_group_5, POST_age_group_6, POST_age_group_7, POST_age_group_8, POST_location, POST_why, POST_before_1, POST_before_2, POST_before_3, POST_before_4, POST_before_5, POST_before_6, POST_before_7, POST_before_8, POST_before_9, POST_before_10, POST_before_freeform, POST_after_1, POST_after_2, POST_after_3, POST_after_4, POST_after_5, POST_after_6, POST_after_7, POST_after_8, POST_after_9, POST_after_10, POST_after_freeform, POST_persona_name, session['user'], current_audience_id)
            update_query = """UPDATE dbo.audience
                        SET formality = ?, buying_for = ?, tech_savvy = ?, decision_making = ?, details = ?, motive = ?, customer_id = ?, gender = ?, age_group_1 = ?, age_group_2 = ?, age_group_3 = ?, age_group_4 = ?, age_group_5 = ?, age_group_6 = ?, age_group_7 = ?, age_group_8 = ?, location = ?, why = ?, before_1 = ?, before_2 = ?, before_3 = ?, before_4 = ?, before_5 = ?, before_6 = ?, before_7 = ?, before_8 = ?, before_9 = ?, before_10 = ?, before_freeform = ?, after_1 = ?, after_2 = ?, after_3 = ?, after_4 = ?, after_5 = ?, after_6 = ?, after_7 = ?, after_8 = ?, after_9 = ?, after_10 = ?, after_freeform = ?, persona_name = ?
                        WHERE customer_id = ? AND audience_id = ?; commit;"""
 
            session['hide'] = True

            execute(update_query, False, tup)

            return redirect(url_for('audience', redirect=True, hide=session['hide'], persona_id = next_audience_id))

            # if 'persona_id' not in request.args:
            #     persona_id = session['first_persona']
            # else:
            #     persona_id = request.args('persona_id')

            # tup = (session['user'], POST_formality, POST_buying_for, POST_tech_savvy, POST_decision_making, POST_details, POST_motive, POST_gender, POST_age_group_1, POST_age_group_2, POST_age_group_3, POST_age_group_4, POST_age_group_5, POST_age_group_6, POST_age_group_7, POST_age_group_8, POST_location, POST_why, POST_before_1, POST_before_2, POST_before_3, POST_before_4, POST_before_5, POST_before_6, POST_before_7, POST_before_8, POST_before_9, POST_before_10, POST_before_freeform, POST_after_1, POST_after_2, POST_after_3, POST_after_4, POST_after_5, POST_after_6, POST_after_7, POST_after_8, POST_after_9, POST_after_10, POST_after_freeform, POST_persona_name, session['user'], persona_id)
            # query = """UPDATE dbo.audience
            #             SET customer_id =  ?, formality = ?, buying_for = ?, tech_savvy = ?, decision_making = ?, details = ?, motive = ?, gender = ?, age_group_1 = ?, age_group_2 = ?, age_group_3 = ?, age_group_4 = ?, age_group_5 = ?, age_group_6 = ?, age_group_7 = ?, age_group_8 = ?, location = ?, why = ?, before_1 = ?, before_2 = ?, before_3 = ?, before_4 = ?, before_5 = ?, before_6 = ?, before_7 = ?, before_8 = ?, before_9 = ?, before_10 = ?, before_freeform = ?, after_1 = ?, after_2 = ?, after_3 = ?, after_4 = ?, after_5 = ?, after_6 = ?, after_7 = ?, after_8 = ?, after_9 = ?, after_10 = ?, after_freeform = ?, persona_name = ?
            #             WHERE customer_id = ? AND audience_id = ?; commit;"""

            # execute(query, False, tup)
            # last_modified(str(session['user']))

        if session['persona_id'] != None:
            persona_id = session['persona_id']
        else:
            persona_id = session['first_persona']

        tup = (session['user'], POST_formality, POST_buying_for, POST_tech_savvy, POST_decision_making, POST_details, POST_motive, POST_gender, POST_age_group_1, POST_age_group_2, POST_age_group_3, POST_age_group_4, POST_age_group_5, POST_age_group_6, POST_age_group_7, POST_age_group_8, POST_location, POST_why, POST_before_1, POST_before_2, POST_before_3, POST_before_4, POST_before_5, POST_before_6, POST_before_7, POST_before_8, POST_before_9, POST_before_10, POST_before_freeform, POST_after_1, POST_after_2, POST_after_3, POST_after_4, POST_after_5, POST_after_6, POST_after_7, POST_after_8, POST_after_9, POST_after_10, POST_after_freeform, POST_persona_name, session['user'], persona_id)
        query = """UPDATE dbo.audience
                    SET customer_id =  ?, formality = ?, buying_for = ?, tech_savvy = ?, decision_making = ?, details = ?, motive = ?, gender = ?, age_group_1 = ?, age_group_2 = ?, age_group_3 = ?, age_group_4 = ?, age_group_5 = ?, age_group_6 = ?, age_group_7 = ?, age_group_8 = ?, location = ?, why = ?, before_1 = ?, before_2 = ?, before_3 = ?, before_4 = ?, before_5 = ?, before_6 = ?, before_7 = ?, before_8 = ?, before_9 = ?, before_10 = ?, before_freeform = ?, after_1 = ?, after_2 = ?, after_3 = ?, after_4 = ?, after_5 = ?, after_6 = ?, after_7 = ?, after_8 = ?, after_9 = ?, after_10 = ?, after_freeform = ?, persona_name = ?
                    WHERE customer_id = ? AND audience_id = ?; commit;"""
        execute(query, False, tup)
        last_modified(str(session['user']))

    me = User(session['user'])
    page = 'product'

    # masks = me.branch('mask', page, 'biz_model')
    inds, hides = me.branch('hide', page, 'biz_model')
    me.set_biz_model()

    hide_1 = dirty_mask_handler(hides, me.biz_model, 1)
    hide_2 = dirty_mask_handler(hides, me.biz_model, 2)
    hide_8 = dirty_mask_handler(hides, me.biz_model, 8)
    hide_9 = dirty_mask_handler(hides, me.biz_model, 9)
    hide_10 = dirty_mask_handler(hides, me.biz_model, 10)
    hide_11 = dirty_mask_handler(hides, me.biz_model, 11)
    hide_12 = dirty_mask_handler(hides, me.biz_model, 12)
    
    mask_3, mask_3_bool = me.mask(page, 3, 'biz_model')
    mask_4, mask_4_bool = me.mask(page, 4, 'biz_model')
    mask_5, mask_5_bool = me.mask(page, 5, 'biz_model')
    mask_6, mask_6_bool = me.mask(page, 6, 'biz_model')
    mask_7, mask_7_bool = me.mask(page, 7, 'biz_model')
    mask_12, mask_12_bool = me.mask(page, 12, 'biz_model')

    if 'redirect' in request.args:
        return render_template('intake/product.html', hide_1=hide_1, hide_2=hide_2, mask_3=mask_3, mask_3_bool=mask_3_bool, mask_4=mask_4, mask_5=mask_5, mask_6=mask_6, mask_7=mask_7, mask_7_bool=mask_7_bool, hide_8=hide_8, hide_9=hide_9, hide_10=hide_10, hide_11=hide_11, mask_12=mask_12,mask_12_bool=mask_12_bool)

    elif request.args.get('coming_home'):
        return redirect(url_for('home'))

    elif not request.args.get('splash'):
        return render_template('intake/product.html', hide_1=hide_1, hide_2=hide_2, mask_3=mask_3, mask_3_bool=mask_3_bool, mask_4=mask_4, mask_5=mask_5, mask_6=mask_6, mask_7=mask_7, mask_7_bool=mask_7_bool, hide_8=hide_8, hide_9=hide_9, hide_10=hide_10, hide_11=hide_11, mask_12=mask_12,mask_12_bool=mask_12_bool) 

    else:
        return redirect(url_for("splash", next_step="product", prev_step="product", redirect=True))



@app.route('/competitors/company/audience/product/product_2', methods=['POST', 'GET'])
@login_required
def product_2():
    if request.form:
        POST_gen_description = clean(request.form['gen_description'])
        POST_gen_description = POST_gen_description.replace("'", "")
        POST_gen_description = POST_gen_description.replace('"', "")
        POST_quantity = clean(request.form['quantity'])
        POST_link = clean(request.form['link'])
        POST_segment_1 = clean(request.form['segment_1'])
        POST_segment_2 = clean(request.form['segment_2'])
        POST_segment_3 = clean(request.form['segment_3'])
        POST_segment_4 = clean(request.form['segment_4'])
        POST_segment_5 = clean(request.form['segment_5'])
        POST_segment_6 = clean(request.form['segment_6'])
        POST_segment_7 = clean(request.form['segment_7'])
        POST_segment_8 = clean(request.form['segment_8'])
        POST_segment_9 = clean(request.form['segment_9'])
        POST_segment_10 = clean(request.form['segment_10'])
        POST_source_1 = clean(request.form['source_1'])
        POST_source_2 = clean(request.form['source_2'])
        POST_source_3 = clean(request.form['source_3'])
        POST_source_4 = clean(request.form['source_4'])
        POST_source_freeform = clean(request.form['source_freeform'])
        POST_source_freeform = POST_source_freeform.replace("'", "")
        POST_source_freeform = POST_source_freeform.replace('"', "")
        POST_product_1_name = clean(request.form['product_1_name'])


        if is_started('product', session['user']):
            tup = (POST_gen_description,POST_quantity,POST_link,POST_segment_1,POST_segment_2,POST_segment_3,POST_segment_4,POST_segment_5,POST_segment_6,POST_segment_7,POST_segment_8,POST_segment_9,POST_segment_10,POST_source_1,POST_source_2,POST_source_3,POST_source_4,POST_source_freeform,session['user'])
            query = """UPDATE dbo.product
                        SET gen_description = ?,quantity = ?, link = ?,segment_1 = ?,segment_2 = ?,segment_3 = ?,segment_4 = ?,segment_5 = ?,segment_6 = ?,segment_7 = ?,segment_8 = ?,segment_9 = ?,segment_10 = ?,source_1 = ?,source_2 = ?,source_3 = ?,source_4 = ?,source_freeform = ?
                        WHERE customer_id = ?"""
        else:
            tup = (session['user'], POST_gen_description, POST_quantity, POST_link, POST_segment_1, POST_segment_2, POST_segment_3, POST_segment_4, POST_segment_5, POST_segment_6, POST_segment_7, POST_segment_8, POST_segment_9, POST_segment_10, POST_source_1, POST_source_2, POST_source_3, POST_source_4, POST_source_freeform)
            query = """INSERT INTO dbo.product
                    (customer_id,gen_description,quantity,link,segment_1,segment_2,segment_3,segment_4,segment_5,segment_6,segment_7,segment_8,segment_9,segment_10,source_1,source_2,source_3,source_4,source_freeform)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);commit;"""
           


        if POST_link:
            execute(query, False, tup)
            last_modified(str(session['user']))



        if POST_product_1_name:
            req = request.form
            requestList = pd.DataFrame(list(req.items()))
            requestList = requestList[19:]
            return requestList.to_json(orient='columns')

            # product_len = int(request.form['product_len'])

            # counterOne = 0
            # newRequestList = {}
            # for x, y in requestList.items():
            #     newRequestList[str(counterOne)] = y
            #     counterOne = counterOne+1

            # productData = list(requestList.iloc[:,1])

            # secondCounter = 0

            # while secondCounter < product_len:
            #     if secondCounter > 0 and secondCounter < product_len:
            #         productData = productData[7:]
            #     print("Product info: " + productData[0] + " " + productData[1] + " " + productData[2] + " " + productData[3] + " " + productData[5] + " " + productData[6])
            #     tup = (productData[0], session['user'], session['user'], productData[0], productData[1], productData[2], productData[3], productData[4], productData[5], productData[6])
            #     query = """IF NOT EXISTS (SELECT name FROM dbo.product_list WHERE name = ? AND customer_id = ?)
            #                 INSERT INTO dbo.product_list (customer_id,name,category,cogs,sales_price,price_model,qty_sold,est_unique_buyers) VALUES (?,?,?,?,?,?,?,?);commit;"""

            #     execute(query, False, tup)
            #     secondCounter += 1

            # last_modified(str(session['user']))


    me = User(session['user'])
    me.set_biz_model()

    if request.args.get('coming_home'):
        return redirect(url_for('home'))
    else:
        if me.biz_model != 'Affiliate' and me.biz_model != 'Media Provider':
            page = 'product_2'

            hide_1 = me.hide(page,1, 'biz_model')
            hide_2 = me.hide(page,2, 'biz_model')

            return render_template('intake/product_2.html', hide_1=hide_1, hide_2=hide_2)
        else:
            return redirect(url_for('splash', next_step='salescycle'))


@app.route('/submit_product', methods=['POST', 'GET'])
@login_required
def submit_product():
    customer_id = session['user']
    name = request.args.get('name')
    category = request.args.get('category')
    cogs = request.args.get('cogs')
    sales_price = request.args.get('sales_price')
    price_model = request.args.get('price_model')
    qty_sold = request.args.get('qty_sold')
    est_unique_buyers = request.args.get('est_unique_buyers')

    tup = (name, customer_id, customer_id, name, category, cogs, sales_price, price_model, qty_sold, est_unique_buyers)
    query = """IF NOT EXISTS (SELECT name FROM dbo.product_list WHERE name = ? AND customer_id = ?)
                            INSERT INTO dbo.product_list (customer_id,name,category,cogs,sales_price,price_model,qty_sold,est_unique_buyers) VALUES (?,?,?,?,?,?,?,?);commit;"""

    execute(query, False, tup)
    last_modified(session['user'])

    return query


@app.route('/removeProduct/<pid>')
@login_required
def removeProduct(pid):
    query = "DELETE FROM dbo.product_list WHERE p_id=? and customer_id=?"
    tup = (pid, session['user'])

    execute(query, False, tup)
    return redirect(url_for('home'))


@app.route('/load_product_list', methods=['GET', 'POST'])
@login_required
def load_product_list():
    query = "SELECT p_id, name, category FROM dbo.product_list WHERE customer_id = " + str(session['user'])

    results = sql_to_df(query)
    results = results.to_json(orient='records')


    return results


@app.route('/product_submit', methods=['POST'])
def product_submit():

    # if request.method == 'POST':
    POST_complexity = request.form['complexity']
    POST_price = request.form['price']
    POST_product_or_service = request.form['product_or_service']
    POST_frequency_of_use = request.form['frequency_of_use']
    POST_frequency_of_purchase = request.form['frequency_of_purchase']
    POST_value_prop = request.form['value_prop']
    POST_warranties_or_guarantee = request.form['warranties_or_guarantee']
    POST_warranties_or_guarantee_freeform = clean(request.form['warranties_or_guarantee_freeform'])
    POST_warranties_or_guarantee_freeform = POST_warranties_or_guarantee_freeform.replace("'", "")
    POST_warranties_or_guarantee_freeform = POST_warranties_or_guarantee_freeform.replace('"', "")
    POST_num_skus = request.form['num_skus']
    POST_level_of_customization = request.form['level_of_customization']
    POST_pid = str(request.form['p_id'])
    tup = (POST_complexity, POST_price, POST_product_or_service, POST_frequency_of_use, POST_frequency_of_purchase, POST_value_prop, POST_warranties_or_guarantee, POST_warranties_or_guarantee_freeform, POST_num_skus, POST_level_of_customization, POST_pid)
    query = """UPDATE dbo.product_list
                SET complexity = ?, price = ?, product_or_service = ?, frequency_of_use = ?, frequency_of_purchase = ?, value_prop = ?, warranties_or_guarantee = ?, warranty_guarantee_freeform = ?, num_skus = ?, level_of_customization = ?
                WHERE p_id = ?;commit;"""

    execute(query, False, tup)
    last_modified(str(session['user']))

    test_query(query, tup)

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
            tup = (session['user'], value, session['user'], value)
            query = """IF NOT EXISTS (SELECT tactic from dbo.%s WHERE customer_id = ? AND tactic = ?)
            INSERT INTO dbo.%s (customer_id, tactic) values (?, ?);commit;""" % (stage, stage)

            test_query(query, tup)
            execute(query, False, tup)

    if request.args.get('coming_home'):
        return redirect(url_for('home'))
    else:
        return redirect(url_for('splash', next_step='goals'))







#############intake/2###############

@app.route('/goals')
@login_required
def goals():
    me = User(session['user'])
    page = 'goals'
    hide_1 = me.hide(page, 1, 'biz_model')


    if request.args.get('coming_home'):
        return redirect(url_for('home'))
    else:
        return render_template('intake/2/goals.html', hide_1=hide_1)

@app.route('/history', methods=['GET','POST'])
@login_required
def history():
    if request.form:
        POST_goal = clean(request.form['goal'])
        POST_current_avg = clean(request.form['current_avg'])
        POST_target_avg = clean(request.form['target_avg'])
        POST_timeframe = clean(request.form['timeframe'])

        if is_started('goals', session['user']):
            tup = (session['user'],POST_goal, POST_current_avg, POST_target_avg, POST_timeframe, session['user'])
            query = """UPDATE dbo.goals
                        SET customer_id = ?, goal = ?, current_avg = ?, target_avg = ?, timeframe = ?
                        WHERE customer_id = ?;commit;"""
        else:              
            tup = (session['user'], POST_goal, POST_current_avg, POST_target_avg, POST_timeframe)
            query = "INSERT INTO dbo.goals (customer_id, goal,current_avg,target_avg,timeframe) VALUES (?,?,?,?,?);commit;"

        execute(query, False, tup)
        last_modified(str(session['user']))

        test_query(query, tup)

    if request.args.get('coming_home'):
        return redirect(url_for('home'))
    else:
        return render_template('intake/2/history.html')




@app.route('/history/platforms', methods=['GET','POST'])
@login_required
def platforms():
    if request.form:
        POST_facebook = clean(request.form['facebook'])
        POST_google = clean(request.form['google'])
        POST_bing = clean(request.form['bing'])
        POST_twitter = clean(request.form['twitter'])
        POST_instagram = clean(request.form['instagram'])
        POST_yelp = clean(request.form['yelp'])
        POST_linkedin = clean(request.form['linkedin'])
        POST_amazon = clean(request.form['amazon'])
        POST_snapchat = clean(request.form['snapchat'])
        POST_youtube = clean(request.form['youtube'])
        POST_none = clean(request.form['none'])

        if is_started('history', session['user']):
            tup = (session['user'], POST_facebook, POST_google, POST_bing, POST_twitter, POST_instagram, POST_yelp, POST_linkedin, POST_amazon, POST_snapchat, POST_youtube, POST_none)
            query = """ UPDATE dbo.history
                        SET customer_id = ?, facebook = ?, google = ?, bing = ?, twitter = ?, instagram = ?, yelp = ?, linkedin = ?, amazon = ?, snapchat = ?, youtube = ?, none = ?
                        ;commit;"""
        else:
            tup = (POST_facebook, POST_google, POST_bing, POST_twitter, POST_instagram, POST_yelp, POST_linkedin, POST_amazon, POST_snapchat, POST_youtube, session['user'], POST_none)
            query = "INSERT INTO dbo.history (facebook, google, bing, twitter, instagram, yelp, linkedin, amazon, snapchat, youtube, customer_id, none) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);commit;"
        
        print(query)
        execute(query, False, tup)
        last_modified(str(session['user']))


    if request.args.get('coming_home'):
        return render_template('intake/2/platforms.html', home=True)
    else:
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

        tup = (d.iloc[-1,1], session['user'])
        query = "UPDATE dbo.history SET digital_spend = ? WHERE customer_id = ?;commit;"
        execute(query, False, tup)
        last_modified(str(session['user']))

        s = 0
        f = 3
        while q < (len(request.form) - 1):
            if q%3 == 0:
                this = d.iloc[s:f,:]
                tup = (session['user'], this.iloc[0,1], this.iloc[1,1], this.iloc[2,1])

                check_tup = (session['user'], this.iloc[0,1])
                check = "SELECT * FROM dbo.platforms WHERE customer_id = ? and platform_name = ?"
                check_check = "SELECT * FROM dbo.platforms WHERE customer_id = %d and platform_name = %s" % (session['user'], this.iloc[0,1])
                print(check_check)

                data, cursor = execute(check, True, check_tup)

                data = cursor.fetchone()

                cursor.close()
                if data == None:
                    print(True)
                    query = "INSERT INTO dbo.platforms (customer_id,platform_name,currently_using,results) VALUES (?,?,?,?);commit;"
                    execute(query, False, tup)

                else:
                    update_tup = (session['user'], this.iloc[0,1], this.iloc[1,1], this.iloc[2,1], this.iloc[0,1])
                    query = "UPDATE dbo.platforms SET customer_id = ?, platform_name = ?, currently_using = ?, results = ? WHERE platform_name = ?;commit;"
                    execute(query, False, update_tup)



            s += 1
            f += 1
            q += 1

    if request.args.get('coming_home'):
        return redirect(url_for('home'))
    else:
        return render_template('intake/2/past.html')

@app.route('/history/platforms/past/done', methods=['GET', 'POST'])
@login_required
def history_freeform():
    POST_history_freeform = clean(request.form['history_freeform'])
    tup = (POST_history_freeform, session['user'])
    query = "UPDATE dbo.history SET history_freeform = ? WHERE customer_id = ?;commit"

    execute(query, False, tup)
    last_modified(str(session['user']))


    if request.args.get('coming_home'):
        return redirect(url_for('home'))
    else:
        return redirect(url_for('creative'))



photos = UploadSet('photos', IMAGES)
filepath = 'static/uploads/img'

app.config['UPLOADED_PHOTOS_DEST'] = filepath
configure_uploads(app, photos)

@app.route('/creative', methods=['GET', 'POST'])
@login_required
def creative():
    user_tup = (session['user'],)
    next_query = "SELECT file_path FROM dbo.assets WHERE customer_id = ?"
    data, cursor = execute(next_query, True, user_tup)
    data = cursor.fetchall()
    cursor.close()
    if len(data) > 0:
        data = data
    else:
        data = None

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = filepath + "/" + filename
        tup = (session['user'], filename, session['user'], filename, "photo", path)
        query = """IF NOT EXISTS (SELECT asset_name from dbo.assets WHERE customer_id = ? and asset_name = ?)
                        INSERT INTO dbo.assets(customer_id,
                                    asset_name,
                                    asset_type, 
                                    file_path)
                        VALUES (?, ?, ?, ?);commit;"""
        execute(query, False, tup)

        next_query = "SELECT file_path FROM dbo.assets WHERE customer_id = ?"
        data, cursor = execute(next_query, True, user_tup)
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






