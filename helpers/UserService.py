from flask import render_template
import data.db as db
import time
import datetime
import zipcodes



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
		if index == len(iterable):
			return True
		else:
			return False

	def first_action_type(self, action, page='customer_basic'):
		if action == 'insert':
			return "INSERT INTO dbo.%s (" % page
		elif action == 'update':
			return "UPDATE dbo.%s SET " % page

	def second_action_type(self, action, page='customer_basic'):
		if action == 'insert':
			return "VALUES ("
		elif action == 'update':
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
			}
		}

		i = 1
		for it in iterable:
			if chunk != 'second_chunk':
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

		statement = ' WHERE %s = %s;' % (identifier, id_value)
		return statement

	def compile(self, keys, vals, owner_id=None, ownership=False, action='insert', page='customer_basic'):
		core = self.build_core(page, action=action, keys=keys, vals=vals)
		if ownership == True:	
			core += self.ownership_statement(owner_id, table=page)

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

	def insert(self, ownership=False):
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


	def insert_conditional(self, conditional, table='customer_basic'):
		if conditional == "not exists":
			insert_query = self.insert()
			select_query = self.select(table=table)
			update_query = self.update()
			insert_query = """
						IF NOT EXISTS ( %s )
			
						%s

						else

						%s
						
						""" % (select_query, insert_query, update_query)

			return insert_query


class UserService:

	def __init__(self, user_id, table='customer_basic'):
		self.table = table
		self.id = user_id

	def insert(self, commit=False):
		vals, keys = get_args_from_form(data)
		db = DBActions(page=self.table, owner_id=self.id, keys=keys, vals=vals)
		# db.execute(self.db.insert(owernship=True), False, tuple(vals), commit=commit)



class IntakeService(UserService):

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

		db.execute(query, False, vals, commit=True)


	def competitors(data, user, **fields):
		vals, keys = get_args_from_form(data)
		print(vals)

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






