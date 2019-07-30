from app import app, session
from flask import request, render_template, redirect, url_for, flash
import json
from helpers import forms
import data.db as db
import helpers.helpers as helpers
from helpers.LoginHandlers import admin_required, owner_required, manager_required, account_rep_required
from helpers.AdminService import AdminService, AdminActions, MessagingService, AdminUserService
from helpers.ViewModels import ViewFuncs, AdminViewModel
import hashlib
from bleach import clean
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature


@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():

	form = forms.AdminLogin()

	if ViewFuncs.ValidSubmission(form=form, method=request.method):
		service = AdminService()
		return service.login(form.email.data, form.password.data, form=form)

	elif request.method == 'GET':
		session['owner_logged_in'] = False
		session['admin_logged_in'] = False
		session['manager_logged_in'] = False

	return render_template("admin_view/login.html", form=form)  



@app.route('/admin/<customer_id>')
@admin_required
def company_view(customer_id):


    page = request.args.get('page')
    basics_df = db.sql_to_df("""SELECT * FROM dbo.customer_basic WHERE ID = """ + customer_id)
    company_name = basics_df['company_name'][0]


    if page == "profile":
        load_company = basics_df
        load_company.insert(loc=0, column='is profile', value=True)
    elif page == "audience":
        load_company = db.sql_to_df("""SELECT * FROM dbo.audience WHERE customer_id = %d""" % (customer_id,))
        load_company = load_company.drop(columns=['customer_id', 'age_group_1', 'age_group_2', 'age_group_3', 'age_group_4', 'age_group_5', 'age_group_6', 'age_group_7', 'age_group_8', 'before_1', 'before_2', 'before_3', 'before_4', 'before_5', 'before_6', 'before_7', 'before_8', 'before_9', 'before_10', 'before_freeform', 'after_1', 'after_2', 'after_3', 'after_4', 'after_5', 'after_6', 'after_7', 'after_8', 'after_9', 'after_10', 'after_freeform'])
        audiences_dict = helpers.clean_audience(customer_id)
        columns = list(load_company.columns)
        return render_template('admin_view/company_view.html',columns=columns,audiences=audiences_dict, customer_id=customer_id, company=company_name, page=page, data=load_company)
    elif page == "product":
        load_company = db.sql_to_df("""SELECT gen_description, quantity, link FROM dbo.product WHERE customer_id = %d""" % (customer_id,))
        product_dict = helpers.clean_product(customer_id)

        product_list = db.sql_to_df("""SELECT * FROM dbo.product_list WHERE customer_id = %d""" % (customer_id,))
        product_list = product_list.drop(columns=['customer_id'])
        product_list = helpers.clean_for_display(product_list)

        return render_template('admin_view/company_view.html',product_list=product_list,product_dict=product_dict, customer_id=customer_id, company=company_name, page=page, data=load_company)
    elif page == "notes":
        load_company = db.sql_to_df("""SELECT * from dbo.notes WHERE customer_id = {customer_id} ORDER BY added%d""" % (customer_id,))
    elif page == "salescycle":
        awareness = db.sql_to_df("""SELECT tactic FROM dbo.awareness WHERE customer_id = %d""" % (customer_id,))
        evaluation = db.sql_to_df("""SELECT tactic FROM dbo.evaluation WHERE customer_id = %d""" % (customer_id,))
        conversion = db.sql_to_df("""SELECT tactic FROM dbo.conversion WHERE customer_id = %d""" % (customer_id,))
        retention = db.sql_to_df("""SELECT tactic FROM dbo.retention WHERE customer_id = %d""" % (customer_id,))
        referral = db.sql_to_df("""SELECT tactic FROM dbo.referral WHERE customer_id = %d""" % (customer_id,))

        return render_template('admin_view/company_view.html', customer_id=customer_id, company=company_name, page=page, data='hi', awareness=awareness, evaluation=evaluation, conversion=conversion, retention=retention, referral=referral)
    else:
        load_company = db.sql_to_df("""SELECT * FROM dbo.""" + page + """ WHERE customer_id = """ + str(customer_id))
        load_company.insert(loc=0, column='is_profile', value=False)
    
    load_company = helpers.clean_for_display(load_company)

    return render_template('admin_view/company_view.html', customer_id=customer_id, company=company_name, page=page, data=load_company)


@app.route('/admin/<customer_id>/note', methods=['POST'])
@admin_required
def add_note(customer_id):
    if request.method == 'POST':
        POST_note = clean(request.form['note'])
        # ' = `
        # " = ~
        POST_note = POST_note.replace("'","`")
        POST_note = POST_note.replace('"',"~")
        tup = (customer_id, session['admin_first'], session['admin_last'], POST_note)
        query = "INSERT INTO dbo.notes (customer_id, author, author_last, content) VALUES(?,?,?,?);commit;"
        db.execute(query, False, tup)

    return redirect(url_for('company_view', customer_id=customer_id, page="notes"))




@app.route('/load_admin')
@admin_required
def load_admin():
    results = db.sql_to_df('SELECT customer_basic.id, customer_basic.company_name, admins.first_name FROM customer_basic, admins WHERE admins.ID = ' + str(session['admin']))

    results = results.to_json(orient='records')

    return results


@app.route('/admin_availability', methods=['GET'])
def admin_availability():
    result = db.sql_to_df('select email from dbo.admins')
    result = result.to_json(orient='records')

    return result



@app.route('/admin')
@manager_required
def admin():
    results = db.sql_to_df("SELECT customer_basic.id, customer_basic.company_name, customer_basic.account_created, customer_basic.perc_complete, customer_basic.last_modified, admins.first_name FROM customer_basic, admins WHERE admins.ID = '" + str(session['admin']) + "' ORDER BY company_name ASC")
    page = AdminViewModel('owner', 'home', admin=str(session['admin']))
    return render_template('admin_view/admin_index.html', page=page, sub=False, results=results, owner=session['owner_logged_in'], admin=session['admin_logged_in'], manager=session['manager_logged_in'])


@app.route('/personnel', methods=['POST', 'GET'])
@owner_required
def personnel():
	
	error = request.args.get('error')
	if error:
		flash(error)
	
	page = AdminViewModel(session['permissions'], 'personnel')
	return render_template('layouts/admin_layout.html', page=page, sub=True, owner=session['owner_logged_in'], admin=session['admin_logged_in'], manager=session['manager_logged_in'])


@app.route('/customers', methods=['GET', 'POST'])
@admin_required
def customers():
	form = forms.AddRep()
	page = AdminViewModel(session['permissions'], 'customers', admin=session['admin'])
	return ViewFuncs.view_admin(
								page=page,
								owner=session['owner_logged_in'],
								admin=session['admin_logged_in'],
								manager=session['manager_logged_in'],
								form=form
								)

@app.route('/customers/<customer_id>', methods=['POST', 'GET'])
@admin_required

def acct_mgmt(customer_id):
	service = AdminService()
	validity = service.validate_view(session['admin'], customer_id)

	if validity == True or session['owner_logged_in'] == True:		
		session['account_rep'] = True
		page = AdminViewModel(
			session['permissions'],
			'acct_mgmt',
			admin=session['admin'],
			user=customer_id,
			view="dashboard"
		)

		return ViewFuncs.view_admin(
			page=page,
			owner=session['owner_logged_in'],
			admin=session['admin_logged_in'],
			manager=session['manager_logged_in'],
			form=None
		)
	else:
		session['account_rep'] = False
		return "You don't have permissions!"











@app.route('/customers/<customer_id>/add_rep', methods=['POST'])
def add_rep(customer_id):
	actions = AdminActions(session['admin'], debug=False)
	actions.add_rep(request.form, customer_id)
	return redirect(url_for('customers'))







@app.route('/account_reps/<customer_id>', methods=['GET'])
@owner_required
def account_reps(customer_id):
	ar_query = """
		select
			(a.first_name + ' ' + a.last_name) as name,
			a.id,
			ar.customer_id,
			cb.company_name

		from admins as a

		left join customer_account_reps as ar
		on ar.admin_id = a.id

		left join customer_basic as cb
		on cb.id = ar.customer_id
	"""

	data, cursor = db.execute(ar_query, True, ())
	data = cursor.fetchall()

	reps = {}
	i = 0
	while i < len(data):
		reps[i] = {
			'name': data[i][0],
			'admin_id': data[i][1],
			'customer_id': data[i][2],
			'company_name': data[i][3]
		}
		i+=1

	return json.dumps(reps)


@app.route('/admin/change_password/<a_id>', methods=['POST'])
@owner_required
def change_admin_password(a_id):
	service = AdminService()
	return service.update_password(a_id, request.form['new_password'], request.form['current_password'])

@app.route('/admin/remove', methods=['POST'])
@owner_required
def remove_admin():
	a_id = request.args.get('a_id')
	if int(a_id) != 6:
		tup = (request.args.get('a_id'),)
		query = "DELETE FROM dbo.admins WHERE id = ?;commit;"
		db.execute(query, False, tup)

	return redirect(url_for('personnel'))

@app.route('/admin/add_user/<a_id>', methods=['POST'])
@owner_required
def add_admin(a_id):
	POST_first_name = clean(request.form['first_name'])
	POST_last_name = clean(request.form['last_name'])
	POST_USERNAME = clean(request.form['email'])
	# POST_PASSWORD = clean(request.form['password'])
	POST_PERMISSIONS = clean(request.form['permissions'])
	POST_PHONE = request.form['phone']
	POST_POSITION = clean(request.form['position'])
	password = sha256_crypt.encrypt("temp1234")
    # password = sha256_crypt.encrypt(str(POST_PASSWORD))

	tup = (POST_first_name, POST_last_name, POST_USERNAME, password, POST_PERMISSIONS, POST_PHONE, POST_POSITION)
	query = """INSERT INTO dbo.admins (
	                                first_name,
	                                last_name,
	                                email,
	                                password,
	                                permissions,
	                                phone_num,
	                                position)
	            VALUES (?,
	                    ?,
	                    ?,
	                    ?,
	                    ?,
	                    ?,
	                    ?); commit;"""

	db.execute(query, False, tup)

	return redirect(url_for('personnel'))




@app.route('/admin/update/<a_id>', methods=['POST'])
@owner_required
def update_admin(a_id):

	POST_first_name = clean(request.form['first_name'])
	POST_last_name = clean(request.form['last_name'])
	POST_USERNAME = clean(request.form['email'])
	POST_PERMISSIONS = clean(request.form['permissions'])
	POST_PHONE = request.form['phone']
	POST_POSITION = clean(request.form['position'])

	tup = (POST_first_name, POST_last_name, POST_USERNAME, POST_PERMISSIONS, POST_PHONE, POST_POSITION, a_id)

	query = """

		UPDATE dbo.admins SET first_name = ?, last_name = ?, email = ?, permissions = ?, phone_num = ?, position = ?

		WHERE id = ?; commit;

	"""

	db.execute(query, False, tup)

	return redirect(url_for('personnel'))

















