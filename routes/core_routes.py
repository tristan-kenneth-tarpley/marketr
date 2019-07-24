from app import *
from helpers.helpers import *
from helpers.classes import *
import hashlib
from bleach import clean
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from helpers.LoginHandlers import *


@app.route('/mockup')
@login_required
def mockup():
    return render_template('sandbox.html')


@app.route('/testing')
@login_required
def testing():
    view = request.args.get('view')
    page = Page(session['user'], view, session['user_name'])
    return render_template('layouts/intake_layout.html', page=page)


@app.route('/forgot')
def forgot():
    return render_template('forgot.html', send=True)

@app.route('/forgot/reset', methods=['GET', 'POST'])
def reset():
    POST_USERNAME = clean(request.form['username'])
    query = "SELECT * FROM dbo.customer_basic WHERE email = ?"
    tup = (POST_USERNAME,)
    data, cursor = execute(query, True, tup)

    data = data.fetchone()

    if data != None and request.method=='POST':
        token = s.dumps(POST_USERNAME, salt="password-reset")
        msg = Message('Reset Password', sender='no-reply@marketr.life', recipients=[POST_USERNAME])
        link = url_for('forgot_password', token=token, _external=True)
        msg.body = "Your password reset link is: %s" % (link,)
        mail.send(msg)
        message_sent = "Your password reset link has been sent. If there is an account associated with that email, you should see it any moment."
    else:
        message_sent = "Your password reset link has been sent! If there is an account associated with that email, you should see it any moment."

    return render_template('forgot.html', send=True, message_sent=message_sent)


@app.route('/forgot_password/<token>')
def forgot_password(token):
    email = s.loads(token, salt='password-reset', max_age=3600)
    return render_template("forgot.html", token=token, send=False, conf=False, reset=False)


@app.route('/forgot_password/update_password', methods=['POST', 'GET'])
def update_password():

    token = request.args.get('token')
    email = s.loads(token, salt='password-reset', max_age=3600)
    POST_password = clean(request.form['password'])
    password = sha256_crypt.encrypt(POST_password)

    tup = (password, email)
    query = "UPDATE dbo.customer_basic SET password = ? WHERE email = ?;commit;"

    execute(query, False, tup)

    return render_template('login.html', reset=True)



    

@app.route('/login', methods=['GET', 'POST'])
def customer_login():

    form = forms.CustomerLogin()

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        loginResult, action = UserService.customer_login(form.email.data, form.password.data)
        return UserService.routeLogin(loginResult, action, form=form)

    elif request.method == 'GET':
        session['logged_in'] = False

    return render_template('login.html', form=form)



@app.route("/logout")
@login_required
def logout():

    session['logged_in'] = False
    session.clear()

    if request.args.get('admin'):
        return redirect(url_for('admin_login_view'))
    else:
        return redirect(url_for('index'))


@app.route('/new', methods=['POST', 'GET'])
def new():
    form = forms.CreateCustomer()

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        result = UserService.CreateCustomer(form.email.data, form.password.data, form=form, app=app)
        if result:
            return redirect(url_for("splash", next_step="begin"))
        else:
            return render_template('new.html', form=form, error=error)

    elif request.method == 'GET':
        session['logged_in'] = False
        
    return render_template('new.html', form=form)



@app.route('/confirm_email/<token>')
def confirm_email(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = s.loads(token, salt='email-confirm', max_age=3600)
    tup = (email,)
    query = "UPDATE dbo.customer_basic SET email_confirmed = 1 WHERE email = ?"
    execute(query, False, tup, commit=True)
    form = forms.CustomerLogin()
    return render_template("login.html", conf=True, form=form)



@app.route('/availability', methods=['GET'])
def availability():
    email = request.args.get('email')
    tup = (email,)
    query = """ SELECT email FROM customer_basic WHERE email = ? """

    data, cursor = execute(query, True, tup)

    data = cursor.fetchall()
    cursor.close()

    if data == []:
        return 'True'
    else:
        return 'False'



########home page###########










@app.route('/delete_asset', methods=['GET'])
@login_required
def delete_asset():
    if request.method == 'GET':
        file_path = request.args.get('file_path')
        tup = (file_path, session['user'])
        query = "DELETE FROM dbo.assets WHERE file_path = ? AND customer_id = ?;commit;"
        execute(query, False, tup)
        if os.path.exists(file_path):
            # name = server_path.rsplit('/', 1)[-1]
            print(file_path)
            os.remove(file_path)
        else:
            name = 'does not exist'
            print(file_path)
            print(name)
        return redirect(url_for('creative'))





@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    # customer_basic
    cust_tup = (session['user'],)
    customer_query = "SELECT company_name, city, state, stage, employees, revenue, first_name, last_name, email, last_modified FROM dbo.customer_basic WHERE id = ?"

    data, cursor = execute(customer_query, True, cust_tup)
    data = data.fetchall()

    company_name = data[0][0]
    city = data[0][1]
    state = data[0][2]
    stage = data[0][3]
    employees = data[0][4]
    revenue = data[0][5]
    primary_first = data[0][6]
    primary_last = data[0][7]
    email = data[0][8]
    last_modified = str(data[0][9])
    last_modified = ''.join(last_modified.split())[:-15].upper()

    cursor.close()

    # company    
    comp_query = "SELECT selling_to, biz_model, storefront_perc, direct_perc, online_perc, tradeshows_perc, other_perc, rev_channel_freeform from dbo.company where customer_id = ?"
    
    data, cursor = execute(comp_query, True, cust_tup)
    data =  data.fetchall()

    selling_to = data[0][0]
    biz_model = data[0][1]
    storefront_perc = data[0][2]
    direct_perc = data[0][3]
    online_perc = data[0][4]
    tradeshows_perc = data[0][5]
    other_perc = data[0][6]
    rev_channel_freeform = data[0][7]

    cursor.close()

    # goal

    goal_query = "SELECT goal, current_avg, target_avg, timeframe from dbo.goals where customer_id = ?"
    
    data, cursor = execute(goal_query, True, cust_tup)
    data = data.fetchall()

    goal = data[0][0]
    goal = goal.lower()
    current_avg = data[0][1]
    target_avg = data[0][2]
    timeframe = data[0][3]

    cursor.close()

    # competitors

    compet_query = "SELECT industry, comp_1_name, comp_1_website, comp_1_type, comp_2_name, comp_2_website, comp_2_type from dbo.competitors where customer_id = ?"
    
    data, cursor = execute(compet_query, True, cust_tup)
    data = data.fetchall()

    industry = data[0][0]
    comp_1_name = data[0][1]
    comp_1_website = data[0][2]
    comp_1_type = data[0][3]
    comp_2_name = data[0][4]
    comp_2_website = data[0][5]
    comp_2_type = data[0][6]

    cursor.close()

    # audience
    audience_query = "SELECT * from dbo.audience where customer_id = %d" % (session['user'],)
    
    audience = sql_to_df(audience_query)
    ages_before_after = clean_audience(session['user'])

    # products
    prod_query = "SELECT quantity, segment_1, segment_2, segment_3, segment_4, segment_5, segment_6, segment_7, segment_8, segment_9, segment_10, source_1, source_2, source_3, source_4, source_freeform from dbo.product where customer_id = ?"

    data, cursor = execute(prod_query, True, cust_tup)
    data = data.fetchall()

    quantity = data[0][0]
    segment_1 = data[0][1]
    segment_2 = data[0][2]
    segment_3 = data[0][3]
    segment_4 = data[0][4]
    segment_5 = data[0][5]
    segment_6 = data[0][6]
    segment_7 = data[0][7]
    segment_8 = data[0][8]
    segment_9 = data[0][9]
    segment_10 = data[0][10]
    source_1 = data[0][11]
    source_2 = data[0][12]
    source_3 = data[0][13]
    source_4 = data[0][14]
    source_freeform = data[0][15]

    segments = [segment_1, segment_2, segment_3, segment_4, segment_5, segment_6, segment_7, segment_8, segment_9, segment_10]
    for segment in segments:
        if segment == " ":
            segments.remove(segment)
    sources = [source_1, source_2, source_3, source_4]
    cursor.close()

    # product_list
    plist_query = "SELECT * from dbo.product_list where customer_id = %d" % (session['user'],)

    product_list = sql_to_df(plist_query)

    # history
    history_query = "SELECT digital_spend, history_freeform from dbo.history where customer_id = ?"
    
    data, cursor = execute(history_query, True, cust_tup)
    data = data.fetchall()
    try:
        digital_spend = data[0][0]
        history_freeform = data[0][1]
    except:
        digital_spend = "n/a"
        history_freeform = "n/a"

    cursor.close()

    # sales cycle
    awareness_query = "SELECT tactic FROM dbo.awareness WHERE customer_id = %d" % (session['user'],)
    awareness = sql_to_df(awareness_query)
    evaluation_query = "SELECT tactic FROM dbo.evaluation WHERE customer_id = %d" % (session['user'],)
    evaluation = sql_to_df(evaluation_query)
    conversion_query = "SELECT tactic FROM dbo.conversion WHERE customer_id = %d" % (session['user'],)
    conversion = sql_to_df(conversion_query)
    retention_query = "SELECT tactic FROM dbo.retention WHERE customer_id = %d" % (session['user'],)
    retention = sql_to_df(retention_query)
    referral_query = "SELECT tactic FROM dbo.referral WHERE customer_id = %d" % (session['user'],)
    referral = sql_to_df(referral_query)

    # platforms
    platforms_query = "SELECT * FROM dbo.platforms where customer_id = %d" % (session['user'],)
    platforms = sql_to_df(platforms_query)

    return render_template('core/home.html', awareness=awareness, evaluation=evaluation, conversion=conversion, retention=retention, referral=referral, platforms=platforms,sources=sources, segments=segments, ages_before_after=ages_before_after, last_modified=last_modified, company_name=company_name,city=city,state=state,stage=stage,employees=employees,revenue=revenue,primary_first=primary_first,primary_last=primary_last,email=email,selling_to=selling_to,biz_model=biz_model,storefront_perc=storefront_perc,direct_perc=direct_perc,online_perc=online_perc,tradeshows_perc=tradeshows_perc,other_perc=other_perc,rev_channel_freeform=rev_channel_freeform,goal=goal,current_avg=current_avg,target_avg=target_avg,timeframe=timeframe,industry=industry,comp_1_name=comp_1_name,comp_1_website=comp_1_website,comp_1_type=comp_1_type,comp_2_name=comp_2_name,comp_2_website=comp_2_website,comp_2_type=comp_2_type,audience=audience,quantity=quantity,segment_1=segment_1,segment_2=segment_2,segment_3=segment_3,segment_4=segment_4,segment_5=segment_5,segment_6=segment_6,segment_7=segment_7,segment_8=segment_8,segment_9=segment_9,segment_10=segment_10,source_1=source_1,source_2=source_2,source_3=source_3,source_4=source_4,source_freeform=source_freeform,product_list=product_list,digital_spend=digital_spend,history_freeform=history_freeform)





# CLIENT_SECRETS_FILE = "client_secret.json"

# # This OAuth 2.0 access scope allows for full read/write access to the
# # authenticated user's account and requires requests to use an SSL connection.
# SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']
# API_SERVICE_NAME = 'ads'
# API_VERSION = 'v2'

# import string
# import random
# def id_generator(size=43, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# redirect_uri = 'https://127.0.0.1:5000/google_test'


# # Initialize the flow using the client ID and secret downloaded earlier.
# flow = OAuth2WebServerFlow(client_id='612075856877-1epe8u6omk3i15hg00aorip67ath8hsb.apps.googleusercontent.com',
#                        client_secret='PummnRa1jDQ4SgI0L3weY3k1',
#                        scope=SCOPES,
#                        redirect_uri=redirect_uri,
#                        access_type='offline')

# @app.route('/auth', methods=['GET', 'POST'])
# def oauth2callback():
    
#     auth_uri = flow.step1_get_authorize_url()

#     return redirect(auth_uri)

# import pprint

# @app.route('/google_test', methods=['GET', 'POST'])
# def google_test():

#     # flow = OAuth2WebServerFlow(client_id='612075856877-1epe8u6omk3i15hg00aorip67ath8hsb.apps.googleusercontent.com',
#                        # client_secret='PummnRa1jDQ4SgI0L3weY3k1',
#                        # scope=SCOPES,
#                        # redirect_uri=redirect_uri)

#     code = request.args.get('code')

#     credentials = flow.step2_exchange(code)
#     pprint.pprint(credentials.__dict__)
#     img = credentials.__dict__['id_token']['picture']

#     http = httplib2.Http()
#     http = credentials.authorize(http)

    


#     return f"""<img src='{img}'><p>{string}</p>"""









