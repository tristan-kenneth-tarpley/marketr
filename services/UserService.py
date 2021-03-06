from flask import render_template, session, url_for, redirect
import data.db as db
import time
import datetime
import zipcodes
import json
from passlib.hash import sha256_crypt
from bleach import clean
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from app import app
from services.PaymentsService import PaymentsService

def intake_page_map():
    pages = {
            0: 'begin',
            1: 'competitors',
            2: 'company',
			3: 'audience',
			4: 'home'
            # 3: 'audience',
            # 4: 'product',
            # 5: 'product_2',
            # 6: 'salescycle',
            # 7: 'goals',
            # 8: 'history',
            # 9: 'platforms',
            # 10: 'past',
			# 11: 'home'
            }

    return pages

def encrypt_password(password):
	return sha256_crypt.encrypt(str(password))

def load_last_page(user):
	pages = intake_page_map()
	tup = (user,)
	data, cursor = db.execute('SELECT perc_complete FROM customer_basic WHERE id = ?', True, tup)
	data = cursor.fetchall()
	try:
		data = int(data[0][0]) / 10
	except:
		data = 0

	if data < 4:
		val = data
		session['onboarding_complete'] = False
	else:
		val = 4
		session['onboarding_complete'] = True
	cursor.close()
	return pages[val]

def get_args_from_form(data):
	vals = []
	keys = []
	for key in data:
		if key != 'csrf_token':    
			if key == 'password':
				vals.append(encrypt_password(data[key])) 
			else:
				vals.append(data[key])
			keys.append(key)

	return vals, keys

# def Table(name):
# 	tup = (name,)
# 	query = """select column_name
# 				from INFORMATION_SCHEMA.columns
# 				where table_name = ?"""
# 	data, cursor = db.execute(query, True, tup)
# 	columns = cursor.fetchall()
# 	cursor.close()

# 	col_list = []
# 	for item in columns:
# 		col_list.append(item[0])

# 	return (col_list)






class Build_Sql:

	def is_end(self, index, iterable):
		if index == int(len(iterable)) - 1:
			return True
		else:
			return False

	def first_action_type(self, action, page='customer_basic'):
		if action == 'insert':
			return "INSERT INTO dbo.%s (" % page
		elif action == 'update':
			return "UPDATE dbo.%s SET " % page
		elif action == 'delete':
			return "DELETE FROM dbo.%s " % page

	def second_action_type(self, action, page='customer_basic'):
		if action == 'insert':
			return "VALUES ("
		elif action == 'update':
			return ""
		elif action == 'delete':
			return ""


	def build(self, iterable, action, chunk, opener):
		appends = {
			'insert': {
				'first_chunk': [', ', ') '],
				'second_chunk': ['?, ', '?)']
			},
			'update': {
				'first_chunk': [' = ?, ', ' = ?'],
				'second_chunk': ['', '']
			},
			'delete': {
				'first_chunk': ['', ''],
				'second_chunk': ['', '']
			}
		}

		i = 0
		for it in iterable:
			if chunk != 'second_chunk' and action != 'delete':
				if not self.is_end(i, iterable):
					concat = it + appends[action][chunk][0]
				elif self.is_end(i, iterable):
					concat = it + appends[action][chunk][1]
			else:
				if not self.is_end(i, iterable):
					concat = appends[action][chunk][0]
				elif self.is_end(i, iterable):
					concat = appends[action][chunk][1]

			opener += concat
			i+=1

		return opener
			

	def build_core(self, page, action='insert', keys=None, vals=None):
		first_chunk = self.first_action_type(action, page)
		second_chunk = self.second_action_type(action, page)

		first_chunk = self.build(keys, action, 'first_chunk', first_chunk)
		second_chunk = self.build(vals, action, 'second_chunk', second_chunk)

		return first_chunk + second_chunk


	def ownership_statement(self, id_value, table='customer_basic'):
		if table == 'customer_basic':
			identifier = 'id'
		else:
			identifier = 'customer_id'

		statement = ' WHERE %s = %s' % (identifier, id_value)
		return statement

	def append_condition(self, condition=None):
		return " %s" % condition

	def compile(self, keys, vals, owner_id=None, ownership=False, action='insert', page='customer_basic', condition=None):
		
		if ownership == True and action == 'insert':	
			if action == 'insert':
				keys.append('customer_id')
				vals.append(str(owner_id))

				core = self.build_core(page, action=action, keys=keys, vals=vals)

				if condition != None:
					core += self.append_condition(condition=condition)

				return core

			else:
				core += self.ownership_statement(owner_id, table=page)


		core = self.build_core(page, action=action, keys=keys, vals=vals)
		if condition != None:
			core += self.append_condition(condition=condition)

		return core


class DBActions:
	def __init__(self, table='page', keys=['email', 'password'], vals=['tristan', 'asdf'], owner_id=None):
		self.build = Build_Sql()
		self.owner_id = owner_id
		self.keys = keys
		self.vals = vals
		self.table = table


	def delete(self, condition=None, ownership=True):
		query = self.build.compile(self.keys, self.vals, page=self.table, action='delete', ownership=ownership, owner_id=self.owner_id, condition=condition)
		return query


	def insert(self, ownership=True):
		query = self.build.compile(self.keys, self.vals, page=self.table, action='insert', ownership=ownership, owner_id=self.owner_id)
		return query

	def select(self, ownership=True, table='customer_basic'):
		if table == 'customer_basic':
			ownership_identifier = 'id'
		else:
			ownership_identifier = 'customer_id'

		query = "SELECT * FROM %s WHERE %s = %s" % (table, ownership_identifier, self.owner_id)
		return query


	def update(self):
		query = self.build.compile(self.keys, self.vals, page=self.table, action='update', ownership=True, owner_id=self.owner_id)
		return query


	def insert_conditional(self, conditional, table='customer_basic', conditional_statement=None):
		if conditional == "not exists":
			insert_query = self.insert()
			if conditional_statement == None:
				select_query = self.select(table=table)
			else:
				select_query = conditional_statement
			update_query = self.update()
			insert_query = """
						IF NOT EXISTS ( %s )
			
						%s

						else

						%s
						
						""" % (select_query, insert_query, update_query)

			return insert_query


class UserService:


	def now():
		now = datetime.datetime.now()
		today = now.strftime("%Y-%m-%d %H:%M")
		return today
	def set_spend_rate(customer_id, rate):
		query = "UPDATE customer_basic SET spend_rate = ? where id = ?"
		db.execute(query, False, (rate, customer_id), commit=True)

	def add_balance(customer_id, amount):
		query = "EXEC update_ledger @customer_id = ?, @amount = ?"
		db.execute(query, False, (customer_id, amount), commit=True)
	
	def update_password(current_password, new_password, customer_id):
		pw, cursor = db.execute(
			'SELECT password FROM customer_basic WHERE id = ?',
			True, (customer_id,)
		)
		pw = cursor.fetchone()
		pw = pw[0]

		if sha256_crypt.verify(current_password, pw):
			new_pw = encrypt_password(new_password)
			db.execute(
				'UPDATE customer_basic SET password = ? WHERE id = ?',
				False, (new_pw, customer_id), commit=True
			)
			return True
		else:
			return 'Current password does not match records'

	def update_id(facebook_id=None, google_id=None, twitter_id=None, customer_id=None):
		query = "UPDATE customer_basic SET facebook_id = ?, google_id = ?, twitter_id = ? where id = ?"
		db.execute(query, False, (facebook_id, google_id, twitter_id, customer_id), commit=True)

		
	def update_plan(customer_id, plan_id):
		plan_table = {
			# live mode
			'plan_FfI9OI02wob7Wl': 'ab_binary',
			'plan_FxJImVg8UME2BU':'ad_binary',
            'plan_GDRUIQvA5OEUgK': 'ad_binary',
			'plan_FfIAIrHBJ78YpY': 'almost_free_binary',
			'plan_FxJJZ1sUDZ0550': 'ad_premium',
            'plan_GiHRR96eXXfxQM': 'analytics',
			# test mode
			'plan_Fed1YzQtnto2mT': 'ab_binary',
			'plan_FecAlOmYSmeDK3': 'ad_binary',
			'plan_FeZoBcEgfD35he': 'almost_free_binary'
		}
		if plan_table[plan_id] != 'almost_free_binary':
			query = f"UPDATE customer_basic SET {plan_table[plan_id]} = 1, current_plan = 1, almost_free_binary = null WHERE id = ?"
			#payments = PaymentsService('test@test.com')
			#payments.delete_subscriptions(sub_id=plan_id, customer_id=customer_id)
		elif plan_table[plan_id] == 'analytics':
			query = f"UPDATE customer_basic SET {plan_table[plan_id]} = 1, current_plan = 1 WHERE id = ?"
		elif plan_table[plan_id] == 'ad_binary':
			query = f"UPDATE customer_basic SET {plan_table[plan_id]} = 1, current_plan = 1, analytics = null WHERE id = ?"
		else:
			query = f"UPDATE customer_basic SET {plan_table[plan_id]} = 1, current_plan = 1 WHERE id = ?"
		db.execute(query, False, (customer_id,), commit=True)

	def UpdateStripeId(email, stripe_id):
		query = "UPDATE customer_basic SET stripe_id = ? WHERE email = ?"
		db.execute(query, False, (stripe_id, email), commit=True)

	def CreateSecondaryUser(first_name, last_name, email, password, customer_id):
		password = encrypt_password(password)
		query = f"""INSERT INTO secondary_users (first_name, last_name, email, password, customer_id)
					VALUES (?, ?, ?, ?, ?)
				"""

		db.execute(query, False, (first_name, last_name, email, password, customer_id), commit=True)

	def CreateCustomer(email, password, form=None, app=None):
		password = encrypt_password(password)
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		tup = (email, password, str(st), str(st))
		query = """
				DECLARE @return_value int

				EXEC @return_value =
					dbo.createUser
						@email = ?,
						@password = ?,
						@account_created = ?,
						@last_modified = ?
				SELECT
					'Return Value' = @return_valuE
				"""
		data, cursor = db.execute(query, True, tup)
		data = cursor.fetchone()
		cursor.close()

		if data[0] == 'success':
			app.config.from_pyfile('config.cfg')
			mail = Mail(app)
			s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
			token = s.dumps(email, salt="email-confirm")
			msg = Message('Confirm Email', sender='no-reply@marketr.life', recipients=[email])
			link = url_for('confirm_email', token=token, _external=True)

			msg.body = "Thanks for joining Market(r)! Click on this link to complete your registration: %s" % (link,)

			mail.send(msg)

			return True
		else:
			error = 'Email exists. Please enter a new one.'
			return error

	def routeLogin(result, action, form=None):
		if result == True:
			if action == 'verify_email':
				tup = ("begin",)
				query = "SELECT heading, paragraph FROM dbo.splash WHERE after_page = ?"
				data, cursor = db.execute(query, True, tup)
				del data
				heading, paragraph = cursor.fetchone()
				heading = heading.replace("`", "'")
				paragraph = paragraph.replace("`", "'")

				return render_template('intake/splash.html', next_step='begin', heading=heading, paragraph=paragraph)
			else:
				# return action
				return redirect(url_for(action))

		elif result == False:
			return render_template('login.html', form=form, error=action)

	def confirm_customer(email, token):
		tup = (email,)
		query = "UPDATE dbo.customer_basic SET email_confirmed = 1 WHERE email = ?"
		db.execute(query, False, tup, commit=True)

	def init_profile(time, user):
		init_query = "EXEC init_profile @date = ?, @customer_id = ?"
		db.execute(init_query, False, (time, user), commit=True)

	def init_profile_after_purchase(time, user):
		init_query = "EXEC init_profile_after_purchase @date = ?, @customer_id = ?"
		db.execute(init_query, False, (time, user), commit=True)

	def get_all_account_users(customer_id):
		query = """select first_name, last_name, email from customer_basic
					where id = ?
					union
					select first_name, last_name, email from secondary_users
					where customer_id = ?"""

		data, cursor = db.execute(query, True, (customer_id, customer_id))
		data = cursor.fetchall()
		returned = [{
			'first_name': user[0],
			'last_name': user[1],
			'email': user[2]
		} for user in data]

		return returned

	def customer_login(email, password):
		try:   
			tup = (email,)
			query = """
				select * from all_co_users(?)
				order by id desc
			"""
			data, cursor = db.execute(query, True, tup)
			data = cursor.fetchall()
			cursor.close()

			pw = data[0][1]
			uid = data[0][2]
			email_confirmed = data[0][3]
			first_name = data[0][4]
			last_name = data[0][5]

			if sha256_crypt.verify(password, pw):
				# if email_confirmed == 1:
				session['prev_log_in'] = data[0][6]
				session['logged_in'] = True
				session['customer'] = True
				session['email'] = data[0][0]
				session['user'] = int(uid)
				session['stripe_id'] = data[0][7]
				session['company_name'] = data[0][8]
				session['user_name'] = "%s %s" % (first_name, last_name)
				session.permanent = True
				session.remember = True

				st = UserService.now()
				last_logged_in = """UPDATE customer_basic SET last_logged_in = ? WHERE id = ?"""
				db.execute(last_logged_in, False, (st, int(uid)), commit=True)

				first_query = db.sql_to_df("SELECT first_name FROM dbo.customer_basic WHERE ID = '" + str(session['user']) + "'")

				if first_query['first_name'][0] == None:
					session['onboarding_complete'] = False
					return True, 'begin'
				else:
					step = load_last_page(session['user'])
					return True, step
				# else:
				# 	tup = ("begin",)
				# 	query = "SELECT heading, paragraph FROM dbo.splash WHERE after_page = ?"
				# 	data, cursor = db.execute(query, True, tup)
				# 	heading, paragraph = cursor.fetchone()
				# 	heading = heading.replace("`", "'")
				# 	paragraph = paragraph.replace("`", "'")
				# 	return True, 'verify_email'

			else:
				error = "Invalid credentials. Try again."
				return False, error 

		except Exception as e:
			error = "Invalid credentials. Try again!"
			return False, error

	def parseCursor(data, columns):
		empty_dict = {}
		for i in range(len(data)):
			empty_dict[int(i)] = {}
			for x in range(len(columns)):
				empty_dict[i].update([(columns[x], data[i][x])])

		dumps = json.dumps(empty_dict)

		return json.loads(dumps)

	def remove_product(product_name):
		print(product_name)





def last_modified(id):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
	tup = (st, id)
	query = """UPDATE dbo.customer_basic
				SET last_modified = ?
				WHERE dbo.customer_basic.id = ?"""

	db.execute(query, False, tup, commit=True)




class IntakeService:

	def __init__(self, id, page, onboarding_complete):
		self.id = id
		self.page = page
		self.onboarding_complete = onboarding_complete
		last_modified(id)

	def perc_complete(self, perc):
		# page_list = [
		# 	'begin', 'competitors', 'company',
		# 	'audience', 'product', 'product_details',
		# 	'salescycle', 'goals', 'history',
		# 	'platforms', 'past'
		# ]

		# perc = (page_list.index(self.page) + 1) * 10
		# if self.page != 'salescycle':
		# 	tup = (self.id, perc, self.page)
		# else: 
		# 	tup = (self.id, perc, 'awareness')
		if self.onboarding_complete == False:
			if perc:
				tup = (perc, self.id)
				query = """
						UPDATE customer_basic
							SET perc_complete = ? where id = ?
						"""

				db.execute(query, False, tup, commit=True)
		else:
			if not perc:
				tup = (self.id, self.id)
				query = """
						UPDATE customer_basic
							SET perc_complete = (
								select (perc_complete + 10)
								from customer_basic where id = ?
							) where id = ?
						"""

				db.execute(query, False, tup, commit=True)
	
	def skip(self, perc):
		self.perc_complete(perc)

	def get_persona(self):
		query = """
				EXEC init_audience @customer_id = %s;
				""" % (self.id,)

		result, cursor = db.execute(query, True, ())
		result = cursor.fetchone()
		cursor.close()

		return str(result[0])

	def get_product(self, view_id):

		if view_id != None:
			tup = (self.id, view_id)
		else:
			tup = (self.id, 0)

		query = """
				EXEC init_product @customer_id = ?, @view_id = ?;
				"""

		result, cursor = db.execute(query, True, tup)
		result = cursor.fetchone()
		cursor.close()

		return str(result[0])

	def audience(self, data, persona_id):
		self.perc_complete(40)
		vals, keys = get_args_from_form(data)
		db_actions = DBActions(table='audience', keys=keys, vals=vals, owner_id=self.id)
		query = db_actions.update()
		query += " WHERE audience_id = %s AND customer_id = %s" % (persona_id, self.id)
		# print(query)
		db.execute(query, False, tuple(vals), commit=True)

	def begin(self, data):
		self.perc_complete(10)

		vals, keys = get_args_from_form(data)

		try:
			zip_code = vals[4]
			zips = zipcodes.matching(zip_code)
			city = zips[0]['city']
			state = zips[0]['state']
		except:
			city = "not defined"
			state = "not defined"
			zip_code = "00000"

		new_vals = [city, state]
		vals += new_vals
		new_keys = ['city', 'state']
		keys += new_keys

		dbactions = DBActions(owner_id=self.id, table='customer_basic', keys=keys, vals=vals)
		query = dbactions.update()
		query += " WHERE id = %s" % (self.id,)

		db.execute(query, False, vals, commit=True)


	def competitors(self, data):
		self.perc_complete(20)
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=self.id, table='competitors', keys=keys, vals=vals)
		query = dbactions.insert_conditional('not exists', table='competitors')
		query += ' WHERE customer_id = %s' % (self.id)
		vals = vals + vals

		db.execute(query, False, tuple(vals), commit=True)

	def company(self, data):
		self.perc_complete(30)
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=self.id, table='company', keys=keys, vals=vals)
		query = dbactions.insert_conditional('not exists', table='company')
		query += ' WHERE customer_id = %s' % (self.id)
		vals = vals + vals

		db.execute(query, False, tuple(vals), commit=True)

	def product(self, data):
		self.perc_complete(None)
		vals, keys = get_args_from_form(data)
		product_list = data['product']

		del vals[-1]
		del keys[-1]

		dbactions = DBActions(owner_id=self.id, table='product', keys=keys, vals=vals)
		query = dbactions.insert_conditional('not exists', table='product')
		query += ' WHERE customer_id = %s' % (self.id)
		vals += vals
		db.execute(query, False, tuple(vals), commit=True)

		for p in product_list:
			p_val, p_key = get_args_from_form(p)
			p_db = DBActions(owner_id=self.id, table='product_list', keys=p_key, vals=p_val)
			conditional_statement = """SELECT * FROM product_list WHERE name = '%s' and customer_id = %s""" % (p_val[0],self.id)
			p_query = p_db.insert_conditional('not exists', table='product_list', conditional_statement=conditional_statement)

			p_val += p_val
		

			db.execute(p_query, False, tuple(p_val), commit=True)

	def product_2(self, data, view_id):
		self.perc_complete(None)
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=self.id, table='product_list', keys=keys, vals=vals)
		query = dbactions.update()
		query += " WHERE customer_id = %s AND p_id = %s" % (self.id, view_id)

		db.execute(query, False, tuple(vals), commit=True)

	def salescycle(self, data):
		self.perc_complete(None)

		def Merge(dict1, dict2):
			del dict1['csrf_token']
			del dict2['csrf_token']

			res = {**dict1, **dict2} 
			return res 

		awareness = Merge(data['awareness_left'], data['awareness_right'])
		evaluation = Merge(data['evaluation_left'], data['evaluation_right'])
		conversion = Merge(data['conversion_left'], data['conversion_right'])
		retention = Merge(data['retention_left'], data['retention_right'])
		referral = Merge(data['referral_left'], data['referral_right'])
		
		stages = [awareness, evaluation, conversion, retention, referral]

		stage_map = {
			0: 'awareness',
			1: 'evaluation',
			2: 'conversion',
			3: 'retention',
			4: 'referral'
		}


		for i in range(len(stages)):
			stage_val, stage_key = get_args_from_form(stages[i])

			base_query = """
						INSERT INTO %s 
						(customer_id, tactic)
						VALUES
						
						""" % (stage_map[i],)
			stage_tup = []
			vals = ""
			not_null = []

			for val in stage_val:
				if val != '':
					not_null.append(val)

			counter = 0
			for v in not_null:
				if counter != (int(len(not_null)) - 1):
					vals += "(?,?),"
				else:
					vals += "(?,?)"

				stage_tup.extend([self.id, v]) 
				counter += 1
			else:
				query = base_query + vals
				if vals:
					db.execute(query, False, tuple(stage_tup), commit=True)

	def goals(self, data):
		self.perc_complete(None)
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=self.id, table='goals', keys=keys, vals=vals)

		query = dbactions.insert_conditional('not exists', table='goals')
		query += ' WHERE customer_id = %s' % (self.id)
		vals = vals + vals

		db.execute(query, False, vals, commit=True)

	def history(self, data):
		self.perc_complete(None)
		
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=self.id, table='history', keys=keys, vals=vals)

		query = dbactions.insert_conditional('not exists', table='history')
		query += ' WHERE customer_id = %s' % (self.id)
		vals = vals + vals

		db.execute(query, False, vals, commit=True)

	def platforms_null(self):
		query = "INSERT INTO platforms (customer_id, platform_name) VALUES (?, 'none')"
		db.execute(query, False, (self.id,), commit=True)

	def platforms(self, data):
		self.perc_complete(None)
		for i in range(int(data.get("platform_length"))):

			keys = ['platform_name', 'currently_using', 'results']
			vals = [data.get('platform[' + str(i) + ']'),
					data.get('currently_using[' + str(i) + ']'),
					data.get('results[' + str(i) + ']')]

			dbactions = DBActions(owner_id=self.id, table='platforms', keys=keys, vals=vals)
			conditional_statement = "SELECT platform_name FROM platforms WHERE customer_id = %s AND platform_name = '%s'" % (self.id, data.get('platform[' + str(i) + ']'),)
			query = dbactions.insert_conditional('not exists', table='platforms', conditional_statement=conditional_statement)
			query += " WHERE customer_id = %s and platform_name = '%s'" % (self.id, data.get('platform[' + str(i) + ']'))
			vals += vals
			db.execute(query, False, vals, commit=True)

	def past(self, data):
		self.perc_complete(None)
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=self.id, table='past', keys=keys, vals=vals)
		query = dbactions.insert_conditional('not exists', table='past')
		query += " WHERE customer_id = %s" % (self.id,)
		vals += vals

		db.execute(query, False, vals, commit=True)






		












