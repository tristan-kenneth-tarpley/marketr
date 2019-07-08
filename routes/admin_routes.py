from app import *
from helpers.helpers import *
from helpers.classes import *
import hashlib
from bleach import clean
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature


@app.route('/admin_login_view')
def admin_login_view():
	return render_template('admin_view/login.html')


@app.route('/admin_login', methods=['POST'])
def admin_login():
	try:
		POST_USERNAME = clean(request.form['username'])
		POST_PASSWORD = clean(request.form['password'])

		tup = (POST_USERNAME,)
		query = "SELECT email, password, ID, first_name, last_name, permissions FROM dbo.admins WHERE email = ?"
		data, cursor = execute(query, True, tup)
		data = cursor.fetchall()
		pw = data[0][1]
		uid = data[0][2]
		admin_first = data[0][3]
		admin_last = data[0][4]
		permissions = data[0][5]
		cursor.close()


		if sha256_crypt.verify(POST_PASSWORD, pw):
			session['logged_in'] = True
			session['admin'] = int(uid)
			session['admin_first'] = admin_first
			session['admin_last'] = admin_last

			if permissions == 'owner':
				session['owner_logged_in'] = True
				session['admin_logged_in'] = True
				session['manager_logged_in'] = True
			elif permissions == 'admin':
				session['owner_logged_in'] = False
				session['admin_logged_in'] = True
				session['manager_logged_in'] = True
			elif permissions == 'manager':
				session['owner_logged_in'] = False
				session['admin_logged_in'] = False
				session['manager_logged_in'] = True

			session.permanent = True
			session.remember = True
			return redirect(url_for('admin'))

		else:
			error = "Invalid credentials. Try again!"
			return render_template("admin_view/login.html", error = error)  

	# except Exception as e:
	except AssertionError:
		error = "Invalid credentials. Try again!"
		return render_template("admin_view/login.html", error = error)  



@app.route('/admin/branch', methods=['GET', 'POST'])
@admin_required
def branch():

    if request.method == 'POST':
        branch_trigger = str(request.form['branch_trigger'])
        branch_trigger_val = str(request.form['branch_trigger_val'])
        branch_action = str(request.form['branch_action'])
        affected_page = str(request.form['affected_page'])
        mask_val = str(request.form['mask_val'])
        default_mask = str(request.form['default_mask'])
        hide_val = request.form['hide_val']
        ind = request.form['ind']

        cursor = db.cursor()
        if branch_action == "hide":
            tup = (branch_trigger, branch_action, affected_page, hide_val, ind, branch_trigger_val)
            query = """INSERT INTO dbo.branches
                        (branch_trigger, branch_action, affected_page, hide_val, ind, branch_trigger_val)
                        VALUES (?,?,?,?,?,?);commit;"""
            execute(query, False, tup)

        elif branch_action == "mask":
            tup = (branch_trigger, branch_action, affected_page, mask_val, default_mask, ind, branch_trigger_val)
            query = """INSERT INTO dbo.branches
                        (branch_trigger, branch_action, affected_page, mask_val, default_mask, ind, branch_trigger_val)
                        VALUES (?,?,?,?,?,?,?);commit;"""
            execute(query, False, tup)
        else:
            return False

    branch_tup = ('affected_page',)
    branches = "SELECT ind, ?, branch_action, branch_trigger_val FROM dbo.branches ORDER BY affected_page ASC"
    branches, cursor = execute(branches, True, branch_tup)
    branches = cursor.fetchall()

    cursor.close()

    return render_template('admin_view/branch.html', branches=branches)

@app.route('/admin/<customer_id>')
@admin_required
def company_view(customer_id):


    page = request.args.get('page')
    basics_df = an.sql_to_df("""SELECT * FROM dbo.customer_basic WHERE ID = """ + customer_id)
    company_name = basics_df['company_name'][0]


    if page == "profile":
        load_company = basics_df
        load_company.insert(loc=0, column='is profile', value=True)
    elif page == "audience":
        load_company = an.sql_to_df("""SELECT * FROM dbo.audience WHERE customer_id = %d""" % (customer_id,))
        load_company = load_company.drop(columns=['customer_id', 'age_group_1', 'age_group_2', 'age_group_3', 'age_group_4', 'age_group_5', 'age_group_6', 'age_group_7', 'age_group_8', 'before_1', 'before_2', 'before_3', 'before_4', 'before_5', 'before_6', 'before_7', 'before_8', 'before_9', 'before_10', 'before_freeform', 'after_1', 'after_2', 'after_3', 'after_4', 'after_5', 'after_6', 'after_7', 'after_8', 'after_9', 'after_10', 'after_freeform'])
        audiences_dict = clean_audience(customer_id)
        columns = list(load_company.columns)
        return render_template('admin_view/company_view.html',columns=columns,audiences=audiences_dict, customer_id=customer_id, company=company_name, page=page, data=load_company)
    elif page == "product":
        load_company = an.sql_to_df("""SELECT gen_description, quantity, link FROM dbo.product WHERE customer_id = %d""" % (customer_id,))
        product_dict = clean_product(customer_id)

        product_list = an.sql_to_df("""SELECT * FROM dbo.product_list WHERE customer_id = %d""" % (customer_id,))
        product_list = product_list.drop(columns=['customer_id'])
        product_list = clean_for_display(product_list)

        return render_template('admin_view/company_view.html',product_list=product_list,product_dict=product_dict, customer_id=customer_id, company=company_name, page=page, data=load_company)
    elif page == "notes":
        load_company = an.sql_to_df("""SELECT * from dbo.notes WHERE customer_id = {customer_id} ORDER BY added%d""" % (customer_id,))
    elif page == "salescycle":
        awareness = an.sql_to_df("""SELECT tactic FROM dbo.awareness WHERE customer_id = %d""" % (customer_id,))
        evaluation = an.sql_to_df("""SELECT tactic FROM dbo.evaluation WHERE customer_id = %d""" % (customer_id,))
        conversion = an.sql_to_df("""SELECT tactic FROM dbo.conversion WHERE customer_id = %d""" % (customer_id,))
        retention = an.sql_to_df("""SELECT tactic FROM dbo.retention WHERE customer_id = %d""" % (customer_id,))
        referral = an.sql_to_df("""SELECT tactic FROM dbo.referral WHERE customer_id = %d""" % (customer_id,))

        return render_template('admin_view/company_view.html', customer_id=customer_id, company=company_name, page=page, data='hi', awareness=awareness, evaluation=evaluation, conversion=conversion, retention=retention, referral=referral)
    else:
        load_company = an.sql_to_df("""SELECT * FROM dbo.""" + page + """ WHERE customer_id = """ + str(customer_id))
        load_company.insert(loc=0, column='is_profile', value=False)
    
    load_company = clean_for_display(load_company)

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
        execute(query, False, tup)

    return redirect(url_for('company_view', customer_id=customer_id, page="notes"))




@app.route('/load_admin')
@admin_required
def load_admin():
    results = sql_to_df('SELECT customer_basic.id, customer_basic.company_name, admins.first_name FROM customer_basic, admins WHERE admins.ID = ' + str(session['admin']))

    results = results.to_json(orient='records')

    return results


@app.route('/admin_availability', methods=['GET'])
def admin_availability():
    result = sql_to_df('select email from dbo.admins')
    result = result.to_json(orient='records')

    return result



@app.route('/admin')
@login_required
def admin():
    results = sql_to_df("SELECT customer_basic.id, customer_basic.company_name, customer_basic.account_created, customer_basic.perc_complete, customer_basic.last_modified, admins.first_name FROM customer_basic, admins WHERE admins.ID = '" + str(session['admin']) + "' ORDER BY company_name ASC")
    return render_template('admin_view/admin_index.html', sub=False, results=results, owner=session['owner_logged_in'], admin=session['admin_logged_in'], manager=session['manager_logged_in'])


@app.route('/personnel', methods=['POST', 'GET'])
@owner_required
def personnel():
	
	error = request.args.get('error')
	if error:
		flash(error)
	
	page = Admin_View('owner', 'personnel')
	return render_template('layouts/admin_layout.html', page=page, sub=True, owner=session['owner_logged_in'], admin=session['admin_logged_in'], manager=session['manager_logged_in'])


@app.route('/admin/change_password/<a_id>', methods=['POST'])
@owner_required
def change_admin_password(a_id):
	current_password = request.form['current_password']
	new_password = request.form['new_password']

	tup = (a_id,)
	data, cursor = execute('SELECT password FROM dbo.admins WHERE id = ?', True, tup)
	data = cursor.fetchall()
	old_pw = data[0][0]

	if sha256_crypt.verify(current_password, old_pw):
		new_password = sha256_crypt.encrypt(str(new_password))
		tup = (new_password, a_id)
		execute('UPDATE dbo.admins SET password = ? WHERE id = ?;commit;', False, tup)

		return redirect(url_for('personnel'))
	else:
		error = "old password doesn't match records"
		return redirect(url_for('personnel', error=error))

@app.route('/admin/remove/<a_id>', methods=['GET'])
@owner_required
def remove_admin(a_id):
	if int(a_id) != 6:
		tup = (a_id,)
		query = "DELETE FROM dbo.admins WHERE id = ?;commit;"
		execute(query, False, tup)

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
	password = "temp1234"
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

	execute(query, False, tup)

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

	execute(query, False, tup)

	return redirect(url_for('personnel'))



















