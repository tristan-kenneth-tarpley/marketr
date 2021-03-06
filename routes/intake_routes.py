from app import app, session, FlaskForm
from flask import request, render_template, redirect, url_for, flash
import services.helpers as helpers
from flask import jsonify
from bleach import clean
import json
import data.db as db
from services.UserService import IntakeService, UserService
from ViewModels.ViewModels import SplashViewModel, ViewFuncs, ContainerViewModel
from services.SharedService import NotificationsService, GoogleChatService
from services.PaymentsService import PaymentsService
from services.LoginHandlers import login_required
import services.forms as forms
import time
import datetime


@app.route('/areas', methods=['GET'])
def cities():
    with open('data/areas.json') as json_file:  
        data = json.load(json_file)
        return json.dumps(data)

@app.route('/industries', methods=['GET'])
def industries():
    with open('data/industries.json') as json_file:
        data = json.load(json_file)
        return json.dumps(data)


@app.route('/salescycle', methods=['GET'])
def get_salescycle():
    with open('data/salescycle.json') as json_file:
        data = json.load(json_file)
        return json.dumps(data)

def get_first_audience(user):
    try:
        tup = (session['user'],)
        query = "SELECT persona_name, audience_id FROM dbo.audience WHERE customer_id = ?"
        names_and_ids, cursor = db.execute(query, True, tup)
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

    splash_page = SplashViewModel(
        next_step=request.args.get('next_step')
    )
    splash_page.compile_splash()

    return render_template('intake/splash.html',
                            next_step=splash_page.next_step,
                            heading=splash_page.heading,
                            paragraph=splash_page.paragraph)


@app.route('/begin', methods=['GET', 'POST'])
@login_required
def begin():
    form = forms.Profile()
    service = IntakeService(session['user'], 'begin', session['onboarding_complete'])
    
    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.begin(form.data)
            if session['onboarding_complete'] == False:
                payments = PaymentsService(session['email'])
                stripe_id = payments.create_customer()

                session['stripe_id'] = stripe_id
                UserService.UpdateStripeId(session['email'], session['stripe_id'])

                gchat = GoogleChatService()
                gchat.onboarding_started(email=session['email'])

                stripe_info = PaymentsService(session['email'], customer_id=session['stripe_id'])
                stripe_info.modify(company_name=form.company_name.data)

        else:
            service.skip(10)

        if session['onboarding_complete'] == True:
            return redirect(url_for('home', view='profile'))
        else:
            return redirect(url_for('competitors'))

    return ViewFuncs.view_page(user=session['user'],
                            user_name=session['user_name'],
                            form=form,
                            view_page='profile',
                            next_page='competitors',
                            coming_home=request.args.get('home'),
                            splash=request.args.get('splash'),
                            onboarding_complete=session['onboarding_complete'],
                            onboarding= True if session['onboarding_complete'] == False else False)



@app.route('/competitors', methods=['POST','GET'])
@login_required
def competitors():
    form = forms.Competitors()
    service = IntakeService(session['user'], 'competitors', session['onboarding_complete'])


    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.competitors(form.data)
        else:
            service.skip(20)

        if session['onboarding_complete'] == True:
            return redirect(url_for('home', view='competitors'))
        else:
            return redirect(url_for('company'))

    return ViewFuncs.view_page(user=session['user'],
                            user_name=session['user_name'],
                            form=form,
                            view_page='competitors',
                            next_page='company',
                            coming_home=request.args.get('home'),
                            splash=request.args.get('splash'),
                            onboarding_complete=session['onboarding_complete'],
                            onboarding= True if session['onboarding_complete'] == False else False)



@app.route('/competitors/company', methods=['POST', 'GET'])
@login_required
def company():
    form = forms.Company()
    service = IntakeService(session['user'], 'company', session['onboarding_complete'])
    
    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.company(form.data)
        else:
            service.skip(30)

        if session['onboarding_complete'] == True:
            return redirect(url_for('home', view='profile'))
        else:
            return redirect(url_for('audience'))

    return ViewFuncs.view_page(user=session['user'],
                                user_name=session['user_name'],
                                form=form,
                                view_page='company',
                                next_page='audience',
                                coming_home=request.args.get('home'),
                                splash=request.args.get('splash'),
                                onboarding_complete=session['onboarding_complete'],
                                onboarding= True if session['onboarding_complete'] == False else False)





@app.route('/competitors/company/audience', methods=['POST', 'GET'])
@login_required
def audience():
    form = forms.Audience()
    service = IntakeService(session['user'], 'audience', session['onboarding_complete'])

    if 'view_id' not in request.args:
        view_id = service.get_persona()
        return redirect(url_for('audience', view_id=view_id, splash=False))


    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.audience(form.data, request.args.get('view_id'))
        else:
            service.skip(40)
  
        if request.form['submit_button'] == '+ save and add another audience':
            next_id = service.get_persona()
            return redirect(url_for('audience', view_id=next_id, splash=False))
        else:
            if not session['onboarding_complete']:
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                UserService.init_profile(st, session['user'])
                google = GoogleChatService()
                google.onboarding_complete(email=session['email'])
                session['onboarding_complete'] = True
                intro = True
            else:
                intro = False
                
            return redirect(url_for('home', view='campaigns', intro=intro))


    return ViewFuncs.view_page(user=session['user'],
                                user_name=session['user_name'],
                                form=form,
                                view_page='audience',
                                next_page='product',
                                coming_home=request.args.get('home'),
                                splash=request.args.get('splash'),
                                onboarding_complete=session['onboarding_complete']
                            )


@app.route('/container', methods=['GET'])
@login_required
def container():
    container = ContainerViewModel(page=request.args.get('page'), user=session['user'])
    return_data = container.GetData()

    return json.dumps(return_data)



@app.route('/competitors/company/audience/product', methods=['GET', 'POST'])
@login_required
def product():
    form = forms.Product()
    service = IntakeService(session['user'], 'product', session['onboarding_complete'])
    
    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.product(form.data)
        else:
            service.skip(50)
        return redirect(url_for('product_2'))

    return ViewFuncs.view_page(user=session['user'],
                                user_name=session['user_name'],
                                form=form,
                                view_page='product',
                                next_page='product_2',
                                coming_home=request.args.get('home'),
                                splash=request.args.get('splash'),
                                onboarding_complete=session['onboarding_complete'])


@app.route('/branch_data', methods=['GET'])
@login_required
def branch_data():
    query = """
            SELECT
                co.selling_to,
                co.biz_model
            FROM company as co

            WHERE co.customer_id = %s
            """ % (session['user'],)
    data,cursor = db.execute(query, True, ())
    data = cursor.fetchone()
    cursor.close()

    return_data = {
        'selling_to': str(data[0]),
        'biz_model': str(data[1])
    }

    return json.dumps(return_data)



@app.route('/competitors/company/audience/product/product_2', methods=['POST', 'GET'])
@login_required
def product_2():
    form = forms.Product_2()
    service = IntakeService(session['user'], 'product_2', session['onboarding_complete'])

    if 'view_id' not in request.args:
        view_id = service.get_product(request.args.get('view_id'))
        return redirect(url_for('product_2', view_id=view_id, splash=False))

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.product_2(form.data, request.args.get('view_id'))
        else:
            service.skip(60)
        
        if request.form['submit_button'] == 'update next product':
            next_id = service.get_product(request.args.get('view_id'))
            return redirect(url_for('product_2', view_id=next_id, splash=False))
        else:
            return redirect(url_for('home', view='profile'))

    return ViewFuncs.view_page(user=session['user'],
                                user_name=session['user_name'],
                                form=form,
                                view_page='product_2',
                                next_page='salescycle',
                                coming_home=request.args.get('home'),
                                onboarding_complete=session['onboarding_complete'],
                                splash=request.args.get('splash'))




@app.route('/competitors/company/audience/product/product_2/salescycle', methods=['GET', 'POST'])
@login_required
def salescycle():

    form = forms.SalesCycle()
    service = IntakeService(session['user'], 'salescycle', session['onboarding_complete'])

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.salescycle(form.data)
        else:
            service.skip(70)
        return redirect(url_for('home', view='profile'))

    return ViewFuncs.view_page(user=session['user'],
                                user_name=session['user_name'],
                                form=form,
                                view_page='salescycle',
                                next_page='nice',
                                coming_home=request.args.get('home'),
                                onboarding_complete=session['onboarding_complete'],
                                splash=request.args.get('splash'))




@app.route('/nice', methods=['POST', 'GET'])
@login_required
def nice():
    return redirect(url_for('splash', next_step='goals'))



#############intake/2###############

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():

    form = forms.Goals()
    service = IntakeService(session['user'], 'goals', session['onboarding_complete'])

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.goals(form.data)
        else:
            service.skip(80)
        return redirect(url_for('home', view='profile'))

    return ViewFuncs.view_page(user=session['user'],
                                user_name=session['user_name'],
                                form=form,
                                view_page='goals',
                                next_page='history',
                                coming_home=request.args.get('home'),
                                splash=request.args.get('splash'),
                                onboarding_complete=session['onboarding_complete'])




@app.route('/history', methods=['GET','POST'])
@login_required
def history():
    form = forms.History()
    service = IntakeService(session['user'], 'history', session['onboarding_complete'])

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.history(form.data)
            if form.none.data == 'none':
                service.platforms_null()
                return redirect(url_for('home', view='profile'))
        else:
            service.skip(90)
        return redirect(url_for('platforms'))

    return ViewFuncs.view_page(user=session['user'],
                            user_name=session['user_name'],
                            form=form,
                            view_page='history',
                            next_page='platforms',
                            coming_home=request.args.get('home'),
                            splash=request.args.get('splash'),
                                onboarding_complete=session['onboarding_complete'])

@app.route('/history/platforms', methods=['GET', 'POST'])
@login_required
def platforms():
    form = forms.Platforms()
    service = IntakeService(session['user'], 'platforms', session['onboarding_complete'])

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.platforms(request.form)
        else:
            service.skip(100)
        return redirect(url_for('home', view='profile'))

    return ViewFuncs.view_page(user=session['user'],
                            user_name=session['user_name'],
                            form=form,
                            view_page='platforms',
                            next_page='past',
                            coming_home=request.args.get('home'),
                            splash=request.args.get('splash'),
                                onboarding_complete=session['onboarding_complete'])

@app.route('/get_platforms', methods=['GET'])
@login_required
def get_platforms():
    tup = (session['user'],)
    query = """
            SELECT facebook, google, bing, twitter, instagram, yelp, linkedin, amazon, snapchat, youtube
                FROM history
                WHERE customer_id = ?
            """
    data, cursor = db.execute(query, True, tup)
    data = cursor.fetchone()
    cursor.close()
    return json.dumps(list(data))



@app.route('/history/platforms/past', methods=['GET','POST'])
@login_required
def past():
    form = forms.Past()
    service = IntakeService(session['user'], 'past', session['onboarding_complete'])

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        if request.form['submit_button'] != 'skip':
            service.past(form.data)
        else:
            service.skip(110)
        return redirect(url_for('home', init=True))

    return ViewFuncs.view_page(user=session['user'],
                            user_name=session['user_name'],
                            form=form,
                            view_page='past',
                            next_page='home',
                            coming_home=request.args.get('home'),
                            splash=request.args.get('splash'),
                            onboarding_complete=session['onboarding_complete'])




# photos = UploadSet('photos', IMAGES)
# filepath = 'static/uploads/img'

# app.config['UPLOADED_PHOTOS_DEST'] = filepath
# configure_uploads(app, photos)

# @app.route('/creative', methods=['GET', 'POST'])
# @login_required
# def creative():
#     user_tup = (session['user'],)
#     next_query = "SELECT file_path FROM dbo.assets WHERE customer_id = ?"
#     data, cursor = db.execute(next_query, True, user_tup)
#     data = cursor.fetchall()
#     cursor.close()
#     if len(data) > 0:
#         data = data
#     else:
#         data = None

#     if request.method == 'POST' and 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         path = filepath + "/" + filename
#         tup = (session['user'], filename, session['user'], filename, "photo", path)
#         query = """IF NOT EXISTS (SELECT asset_name from dbo.assets WHERE customer_id = ? and asset_name = ?)
#                         INSERT INTO dbo.assets(customer_id,
#                                     asset_name,
#                                     asset_type, 
#                                     file_path)
#                         VALUES (?, ?, ?, ?);commit;"""
#         db.execute(query, False, tup)

#         next_query = "SELECT file_path FROM dbo.assets WHERE customer_id = ?"
#         data, cursor = db.execute(next_query, True, user_tup)
#         data = cursor.fetchall()

#         return render_template('intake/creative.html', images=data)

#     return render_template('intake/creative.html', images=data)






######helper routes########


@app.route('/load_past_inputs', methods=['GET'])
@login_required
def load_past_inputs():

    page = request.args.get('page')
    page = page.replace("/", " ")
    *first, page = page.split()
    del first

    result = ViewFuncs.past_inputs(page, session['user'], view_id=request.args.get('view_id'))

    if len(result) > 0:
        result = result.to_json(orient='records')
        return result
    else:
        return 'nah, not this time'









