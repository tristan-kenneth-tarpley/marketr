from flask import render_template, session, url_for, redirect
import data.db as db
import time
import datetime
import zipcodes
import helpers.helpers as helpers
import json
from passlib.hash import sha256_crypt
from bleach import clean
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from helpers.LoginHandlers import *


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

def Table(name):
	tup = (name,)
	query = """select column_name
				from INFORMATION_SCHEMA.columns
				where table_name = ?"""
	data, cursor = execute(query, True, tup)
	columns = cursor.fetchall()
	cursor.close()

	col_list = []
	for item in columns:
		col_list.append(item[0])

	return (col_list)



def encrypt_password(password):
	return sha256_crypt.encrypt(str(password))



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

	def last_modified(self):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		tup = (st, user)
		query = """UPDATE dbo.customer_basic
	                SET last_modified = ?
	                WHERE dbo.customer_basic.id = ?"""

		execute(query, False, tup)


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

			msg.body = "Your link is: %s" % (link,)

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
				data, cursor = execute(query, True, tup)
				heading, paragraph = cursor.fetchone()
				heading = heading.replace("`", "'")
				paragraph = paragraph.replace("`", "'")

				return render_template('intake/splash.html', next_step='begin', heading=heading, paragraph=paragraph)
			else:
				return redirect(url_for(action))
		elif result == False:
			return render_template('login.html', form=form, error=action)

	def customer_login(email, password):
		try:   
			tup = (email,)
			query = "SELECT email, password, ID, email_confirmed, first_name, last_name FROM dbo.customer_basic WHERE email = ?"
			data, cursor = db.execute(query, True, tup)
			data = cursor.fetchall()
			cursor.close()

			pw = data[0][1]
			uid = data[0][2]
			email_confirmed = data[0][3]
			first_name = data[0][4]
			last_name = data[0][5]

			if sha256_crypt.verify(password, pw):
				if email_confirmed == 1:
					session['logged_in'] = True
					session['user'] = int(uid)
					session['user_name'] = "%s %s" % (first_name, last_name)
					session.permanent = True
					session.remember = True

					first_query = db.sql_to_df("SELECT first_name FROM dbo.customer_basic WHERE ID = '" + str(session['user']) + "'")

					if first_query['first_name'][0] == None:
						return True, 'begin'
					else:
						step = helpers.load_last_page(session['user'])
						return True, step
				else:
					tup = ("begin",)
					query = "SELECT heading, paragraph FROM dbo.splash WHERE after_page = ?"
					data, cursor = execute(query, True, tup)
					heading, paragraph = cursor.fetchone()
					heading = heading.replace("`", "'")
					paragraph = paragraph.replace("`", "'")
					return True, 'verify_email'

			else:
				error = "Invalid credentials. Try again."
				return False, error 

		# except Exception as e:
		except AssertionError:
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


class IntakeService(UserService):

	def get_persona(user):
		query = """
					EXEC init_audience @customer_id = %s;
					""" % (user,)

		result, cursor = db.execute(query, True, ())
		result = cursor.fetchone()
		cursor.close()

		return str(result[0])

	def get_product(user, view_id=None):

		if view_id != None:
			tup = (user, view_id)
		else:
			tup = (user, 0)

		query = """
				EXEC init_product @customer_id = ?, @view_id = ?;
				"""

		result, cursor = db.execute(query, True, tup)
		result = cursor.fetchone()
		cursor.close()

		return str(result[0])

	def audience(data, user, persona_id):
		vals, keys = get_args_from_form(data)
		db_actions = DBActions(table='audience', keys=keys, vals=vals, owner_id=user)
		query = db_actions.update()
		query += " WHERE audience_id = %s AND customer_id = %s" % (persona_id, user)
		# print(query)
		db.execute(query, False, tuple(vals), commit=True)

	def begin(data, user):
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

		dbactions = DBActions(owner_id=user, table='customer_basic', keys=keys, vals=vals)
		query = dbactions.update()

		print(query)

		db.execute(query, False, vals, commit=True)


	def competitors(data, user, **fields):
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=user, table='competitors', keys=keys, vals=vals)
		query = dbactions.insert_conditional('not exists', table='competitors')
		vals = vals + vals

		db.execute(query, False, vals, commit=True)

	def company(data, user):
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=user, table='company', keys=keys, vals=vals)

		query = dbactions.insert_conditional('not exists', table='company')
		vals = vals + vals

		db.execute(query, False, vals, commit=True)

	def product(data, user):
		vals, keys = get_args_from_form(data)
		product_list = data['product']

		del vals[-1]
		del keys[-1]

		dbactions = DBActions(owner_id=user, table='product', keys=keys, vals=vals)
		query = dbactions.insert_conditional('not exists', table='product')
		vals += vals
		db.execute(query, False, tuple(vals), commit=True)

		for p in product_list:
			p_val, p_key = get_args_from_form(p)
			p_db = DBActions(owner_id=user, table='product_list', keys=p_key, vals=p_val)
			conditional_statement = """SELECT * FROM product_list WHERE name = '%s' and customer_id = %s""" % (p_val[0],user)
			p_query = p_db.insert_conditional('not exists', table='product_list', conditional_statement=conditional_statement)

			p_val += p_val
		

			db.execute(p_query, False, tuple(p_val), commit=True)

	def product_2(data, user, view_id):
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=user, table='product_list', keys=keys, vals=vals)
		query = dbactions.update()
		query += " WHERE customer_id = %s AND p_id = %s" % (user, view_id)

		db.execute(query, False, tuple(vals), commit=True)

	def salescycle(data, user):

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

				stage_tup.extend([user, v]) 

				counter += 1
			else:
				query = base_query + vals
				db.execute(query, False, tuple(stage_tup), commit=True)

	def goals(data, user):
		vals, keys = get_args_from_form(data)

		dbactions = DBActions(owner_id=user, table='goals', keys=keys, vals=vals)

		query = dbactions.insert_conditional('not exists', table='goals')
		vals = vals + vals

		db.execute(query, False, vals, commit=True)



		












