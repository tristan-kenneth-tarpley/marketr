from flask import render_template, redirect, url_for
from data.db import *
import time
import datetime
import zipcodes
from bleach import clean
from helpers.UserService import UserService


class SplashViewModel:
	def __init__(self, prev_step=None, next_step=None, redirect=None):

		self.next_step = clean(next_step)
		self.prev_step = clean(prev_step)
		self.redirect = clean(redirect)

		tup = (self.next_step,)
		query = "SELECT heading, paragraph FROM dbo.splash WHERE after_page = ?"
		data, cursor = execute(query, True, tup)
		heading, paragraph = cursor.fetchone()
		self.heading = heading.replace("`", "'")
		self.paragraph = paragraph.replace("`", "'")
		cursor.close()

	def splashes():
		return ['begin', 'competitors', 'company', 'audience', 'product', 'salescycle', 'history']


class ContainerViewModel:
	def __init__(self, page=None, user=None):
		if page == 'audience':
			self.table = page
		elif page == 'product_2':
			self.table = 'product_list'
		self.user = user
	
	def GetData(self):
		if self.table == 'audience':
			params = ('persona_name', 'audience_id', self.table, self.user)
		elif self.table == 'product_list':
			params = ('name', 'p_id', self.table, self.user)
		
		query = "SELECT %s, %s FROM %s WHERE customer_id = %s" % params
		data, cursor = execute(query, True, ())
		data = cursor.fetchall()

		column_list = ['name', 'id']
		data = UserService.parseCursor(data, column_list)

		return data


class IntakeViewModel:
	def __init__(self, id, user_name, title=None):
		stage_1 = ['competitors', 'company', 'audience', 'product', 'product_2', 'salescycle']
		stage_2 = ['goals']
		stage_3 = ['history', 'platforms', 'past']
		stage_4 = ['creative']
		custom = ['salescycle', 'history', 'platforms']
		self.id = id
		self.title = title
		self.name = user_name

		if self.title in stage_1:
			self.stage = 1
		elif self.title in stage_2:
			self.stage = 2
		elif self.title in stage_3:
			self.stage = 3
		elif self.title in stage_4:
			self.stage = 4
		else:
			self.stage = 0

		def get_copy(self):
			query = """

					SELECT * FROM dbo.everything as e
					WHERE
					e.page_title = '%s'

					and
					(
						EXISTS (select * from should_show(e.relevant_tags, %s))
						OR
						e.relevant_tags IS null
					)

					ORDER BY e.order_on_page
 

					""" % (self.title, self.id)

			data, cursor = execute(query, True, ())
			data = data.fetchall()
			cursor.close()
			return data

		columns = ['q_id', 'page_id', 'page_title', 'page_h1', 'page_p', 'label', 'why_asking_binary', 'why_label', 'what_binary', 'what_label', 'required_binary', 'label_p', 'horizontal_separator_binary', 'container_binary', 'answer_type', 'placeholder', 'a_format', 'html_name', 'route', 'tiles_name_h6', 'tiles_name_p', 'icon_file_path', 'sub_name', 'relevant_tags', 'order_on_page']
		if self.title not in custom:
			self.questions = UserService.parseCursor(get_copy(self), columns)
		else:
			self.questions = None





class AdminViewModel:
	def __init__(self, permission_level, page):
		self.permission_level = permission_level
		self.page = page

		if page == 'personnel':
			tup = ()
			query = 'SELECT first_name, last_name, email, permissions, id, position, phone_num FROM dbo.admins'
			data, cursor = execute(query, True, tup)
			data = data.fetchall()
			cursor.close()
			self.data = data

		elif page == 'customers':
			query = """
				select
					concat(cb.first_name, ' ', cb.last_name) as name,
					cb.email,
					cb.company_name,
					cb.id

				from dbo.customer_basic as cb
			"""
			data, cursor = execute(query, True, ())
			data = data.fetchall()

			if len(data) > 1:
				columns = ['name', 'email', 'company_name', 'customer_id']
				return_data = UserService.parseCursor(data, columns)

			self.data = return_data
			cursor.close()


		elif page == 'home':
			tup = ()
			query = sql_to_df("SELECT customer_basic.id, customer_basic.company_name, customer_basic.account_created, customer_basic.perc_complete, customer_basic.last_modified, admins.first_name FROM customer_basic, admins WHERE admins.ID = '" + str(session['admin']) + "' ORDER BY company_name ASC")
			self.data = query






class ViewFuncs:

	def view_page(user_name=None, user=None, form=None, view_page=None, next_page=None, coming_home=True, splash=False):

		page = IntakeViewModel(user, user_name, title=view_page)
		splashes = SplashViewModel.splashes()

		if view_page in splashes and splash==None:
			return redirect(url_for('splash', next_step=view_page))
		elif coming_home == True:
			return redirect('/home')
		elif view_page not in splashes or splash:
			return render_template("layouts/intake_layout.html", page=page, form=form)
		else:
			return render_template("layouts/intake_layout.html", page=page, form=form)

	def view_admin(page=None, owner=False, admin=False, manager=False, form=None):
		return render_template('layouts/admin_layout.html', page=page, sub=True, owner=owner, admin=admin, manager=manager, form=form)

	def ValidSubmission(form=None, method=None):
		if method == 'POST' and form.validate_on_submit():
			return True
		else:
			return False

	def past_inputs(page, user, view_id=None):
		intake_pages = ['begin', 'competitors', 'company', 'competitors', 'audience', 'product', 'product_2', 'salescycle', 'goals', 'history', 'platforms', 'past', 'creative']
		if page in intake_pages:
			if page == 'begin':
				query = "SELECT first_name, last_name, company_name, revenue, employees, zip, stage, website FROM dbo.customer_basic WHERE ID = %s" % (user,)
				result = sql_to_df(query)
			elif page == 'salescycle':
				awareness = sql_to_df("select distinct tactic from dbo.awareness WHERE customer_id=%d" % (user,))
				awareness.insert(loc=0, column='stage', value='awareness')

				evaluation = sql_to_df("select distinct tactic from dbo.evaluation WHERE customer_id=%d" % (user,))
				evaluation.insert(loc=0, column='stage', value='evaluation')

				conversion = sql_to_df("select distinct tactic from dbo.conversion WHERE customer_id=%d" % (user,))
				conversion.insert(loc=0, column='stage', value='conversion')

				retention = sql_to_df("select distinct tactic from dbo.retention WHERE customer_id=%d" % (user,))
				retention.insert(loc=0, column='stage', value='retention')

				referral = sql_to_df("select distinct tactic from dbo.referral WHERE customer_id=%d" % (user,))
				referral.insert(loc=0, column='stage', value='referral')
				stages = [awareness, evaluation, conversion, retention, referral]

				result = pd.concat(stages)

		    
			elif page == 'audience':
				query = "SELECT * FROM dbo.audience WHERE customer_id = %s and audience_id = %s" % (user, view_id)
				result = sql_to_df(query)


			elif page == 'product_2':
				query = "SELECT * FROM dbo.product_list WHERE customer_id = %d and p_id = %s" % (user,view_id)
				result = sql_to_df(query)
			elif page == 'past':
				query = "SELECT history_freeform FROM dbo.history WHERE customer_id = %d" % (user,)
				result = sql_to_df(query)
			elif page == 'creative':
				result = 'nah'
			elif page == 'splash':
				result = 'nah'
			else:
				query = "SELECT * FROM dbo.%s WHERE customer_id = %d" % (page, user)
				result = sql_to_df(query)


			return result
			
		else:
			return False













