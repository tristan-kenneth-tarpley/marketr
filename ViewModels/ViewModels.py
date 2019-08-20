from flask import render_template, redirect, url_for, session
import data.db as db
import time
import datetime
import zipcodes
import pandas as pd
from services.UserService import UserService
from services.SharedService import CoreService, InsightsService
from services.AdminService import AdminService, AdminUserService, MessagingService, TaskService, TacticService
from services.CompetitorService import CompetitorService
import services.forms as forms
import json
import itertools

class SplashViewModel:
	def __init__(self, next_step=None):
		self.next_step = next_step

	def splashes(self):
		return ['begin', 'competitors', 'company', 'audience', 'product', 'salescycle', 'history']
	
	def compile_splash(self):
		tup = (self.next_step,)
		query = "SELECT heading, paragraph FROM dbo.splash WHERE after_page = ?"
		data, cursor = db.execute(query, True, tup)
		del data
		heading, paragraph = cursor.fetchone()
		self.heading = heading.replace("`", "'")
		self.paragraph = paragraph.replace("`", "'")
		cursor.close()


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
		data, cursor = db.execute(query, True, ())
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

			data, cursor = db.execute(query, True, ())
			data = data.fetchall()
			cursor.close()
			return data

		columns = ['q_id', 'page_id', 'page_title', 'page_h1', 'page_p', 'label', 'why_asking_binary', 'why_label', 'what_binary', 'what_label', 'required_binary', 'label_p', 'horizontal_separator_binary', 'container_binary', 'answer_type', 'placeholder', 'a_format', 'html_name', 'route', 'tiles_name_h6', 'tiles_name_p', 'icon_file_path', 'sub_name', 'relevant_tags', 'order_on_page']
		if self.title not in custom:
			self.questions = UserService.parseCursor(get_copy(self), columns)
		else:
			self.questions = None


class AdminViewFuncs:
	def __init__(self, customer_id):
		self.service = AdminService()
		self.customer_id = customer_id
	
	def ValidView(self, validity=False):
		validity = self.service.validate_view(session['admin'], self.customer_id)
		if validity == True or session['owner_logged_in'] == True:
			return True
		else:
			return False



class AdminViewModel:
	def __init__(self,
				permission_level: str,
				page: str,
				user=None,
				admin=None,
				view=None,
				tag_id=None) -> None:

		self.tag_id = tag_id
		self.permission_level = permission_level
		self.page = page
		self.admin_service = AdminService()
		self.admin = admin
		self.view = view
		self.user = user
		self.view_type = 'admin'
		self.admins = self.admin_service.get_admins()
		self.switch(page)()

	def switch(self, case: str) -> None:
		switcher = {
			"personnel": self.personnel,
			"customers": self.customers,
			"home": self.home,
			"acct_mgmt": self.acct_mgmt,
			"tags": self.tags
		}
		return switcher[case]
	
	def tags(self):
		tags = TacticService(tag_id=self.tag_id)
		meta = tags.meta()
		self.total_tags = tags.count()
		self.tactic_id = meta['0']['tactic_id']
		self.tactic_title = meta['0']['title']
		self.tactic_description = meta['0']['description']
		self.image = meta['0']['image']
		self.category = meta['0']['category']

	def acct_mgmt(self):
		service = AdminUserService(self.user, self.admin)
		self.messages = service.messaging.get_messages()
		self.tasks = service.tasks.get_tasks()
		self.task_form = forms.TaskForm()
		self.customer_name = self.admin_service.get_customer_name(self.user)
		insights_service = InsightsService(self.user, admin_id=self.admin, user='admin')
		self.insights = insights_service.fetch()

	def personnel(self) -> None:
		self.data = self.admin_service.get_admin_info()

	def customers(self) -> None:
		if self.permission_level != "owner":
			conditional = " WHERE admin_id = %s" % (self.admin,)
		else:
			conditional = None
		self.data = self.admin_service.get_customers(conditional=conditional)

	def home(self) -> None:
		query = db.sql_to_df("SELECT customer_basic.id, customer_basic.company_name, customer_basic.account_created, customer_basic.perc_complete, customer_basic.last_modified, admins.first_name FROM customer_basic, admins WHERE admins.ID = '" + self.admin + "' ORDER BY company_name ASC")
		self.data = query




class CustomerDataViewModel:
	def __init__(self, customer_id=1, init=False, admin=False) -> None:
		self.customer_id = customer_id
		self.core_service = CoreService(self.customer_id)
		self.admin = admin

		if init == True:
			self.compile_all()
	
	def compile_core(self) -> dict:
		data = self.core_service.customer_core()

		core_data = {}
		columns = [
			'customer_id', 'company_name',
			'first_name', 'last_name',
			'email', 'stage',
			'city', 'state', 'current_plan',
			'selling_to', 'biz_model',
			'rev_channel_freeform', 'storefront_perc',
			'direct_perc', 'online_perc',
			'tradeshows_perc', 'other_perc',
			'industry', 'comp_1_name',
			'comp_1_type', 'comp_1_website',
			'comp_2_name', 'comp_2_type',
			'comp_2_website', 'gen_description',
			'quantity', 'link',
			'segment_1', 'segment_2',
			'segment_3', 'segment_4',
			'segment_5', 'segment_6',
			'segment_7', 'segment_8',
			'segment_9', 'segment_10',
			'source_1', 'source_2',
			'source_3', 'source_4',
			'source_freeform', 'goal',
			'current_avg', 'target_avg',
			'timeframe', 'digital_spend',
			'history_freeform'
		]

		for i in range(len(data)):
			core_data.update([(columns[i], data[i])])

		competitors = CompetitorService()
		
		core_data['competitor_intro_1'] = competitors.intro(core_data.get('comp_1_website'))
		core_data['competitor_intro_2'] = competitors.intro(core_data.get('comp_2_website'))

		return core_data
	
	def compile_products(self) -> dict:
		data = self.core_service.get_products()
		columns = [
			'complexity', 'price',
			'product_or_service', 'frequency_of_use',
			'frequency_of_purchase', 'warranties_or_guarantee',
			'warranty_guarantee_freeform', 'num_skus',
			'level_of_customization', 'customer_id',
			'name', 'category',
			'cogs', 'sales_price',
			'qty_sold', 'est_unique_buyers',
			'p_id', 'price_model',
			'value_prop_1', 'value_prop_2',
			'value_prop_3', 'value_prop_4',
			'value_prop_5'
		]
		product_list = {}
		for i in range(len(data)):
			product_list[i] = {}
			for x in range(len(data[i])):
				product_list[i].update([(columns[x], data[i][x])])

		return product_list

	def compile_audience(self) -> dict:
		data = self.core_service.get_audience()
		columns = [
			'customer_id', 'gender',
			'age_group_1', 'age_group_2',
			'age_group_3', 'age_group_4',
			'age_group_5', 'age_group_6',
			'age_group_7', 'age_group_8',
			'location', 'why',
			'before_1', 'before_2',
			'before_3', 'before_4',
			'before_5', 'before_6',
			'before_7', 'before_8',
			'before_9', 'before_10',
			'before_freeform', 'after_1',
			'after_2', 'after_3',
			'after_4', 'after_5',
			'after_6', 'after_7',
			'after_8', 'after_9',
			'after_10', 'after_freeform',
			'audience_id', 'formality',
			'buying_for', 'tech_savvy',
			'decision_making', 'details',
			'motive', 'persona_name',
			'company_size'
		]
		audience_list = {}
		for i in range(len(data)):
			audience_list[i] = {}
			for x in range(len(data[i])):
				audience_list[i].update([(columns[x], data[i][x])])

		return audience_list

	def compile_platforms(self) -> dict:
		data = self.core_service.get_platforms()
		columns = [
			'platform_id',
			'customer_id',
			'platform_name',
			'currently_using',
			'results'
		]
		platform_list = {}
		for i in range(len(data)):
			platform_list[i] = {}
			for x in range(len(data[i])):
				platform_list[i].update([(columns[x], data[i][x])])

		return platform_list

	def compile_messages(self) -> dict:
		data = self.core_service.get_messages()
		return data

	def compile_tasks(self) -> dict:
		data = self.core_service.get_tasks()
		return data

	def compile_salescycle(self) -> dict:
		data = self.core_service.get_salescycle()
		return_data = {
			'awareness': data[0].split("^") if data[0] else None,
			'evaluation': data[1].split("^") if data[1] else None,
			'conversion': data[2].split("^") if data[2] else None,
			'retention': data[3].split("^") if data[3] else None,
			'referral': data[4].split("^") if data[4] else None
		}

		return return_data

	def compile_google(self) -> dict:
		data = self.core_service.get_google()
		return data

	def compile_tests(self) -> dict:
		data = self.core_service.get_tests()
		return data

	def compile_insights(self) -> dict:
		insights_service = InsightsService(self.customer_id, self.admin)
		return insights_service.fetch()

	def compile_all(self) -> None:
		core = self.compile_core()
		products = self.compile_products()
		audiences = self.compile_audience()
		platforms = self.compile_platforms()
		messages = self.compile_messages()
		self.tasks = self.compile_tasks()
		salescycle = self.compile_salescycle()
		google = self.compile_google()
		insights = self.compile_insights()
		tests = self.compile_tests()
		return_data = {
			'core': core,
			'products': products,
			'audiences': audiences,
			'platforms': platforms,
			'messages': messages,
			'tasks': self.tasks,
			'salescycle': salescycle,
			'google': google,
			'insights': insights,
			'tests': tests
		}

		self.data = return_data



class ViewFuncs:


	def view_page(user_name=None, user=None, form=None, view_page=None, next_page=None, coming_home=True, splash=False, onboarding_complete=False):

		page = IntakeViewModel(user, user_name, title=view_page)
		splashVM = SplashViewModel(next_step=view_page)
		splashes = splashVM.splashes()

		print(coming_home)

		if view_page in splashes and splash == None and coming_home == None:
			return redirect(url_for('splash', next_step=view_page))
		elif view_page not in splashes or splash:
			return render_template("layouts/intake_layout.html", onboarding_complete=onboarding_complete, page=page, form=form)
		else:
			return render_template("layouts/intake_layout.html", onboarding_complete=onboarding_complete, page=page, form=form)

	def view_admin(page=None, tag_id=None, owner=False, admin=False, manager=False, form=None, csv_form=None, ab_form=None, insight_form=None):
		return render_template(
			'layouts/admin_layout.html',
			page=page,
			sub=True, owner=owner,
			admin=admin,
			manager=manager,
			form=form,
			csv_form=csv_form,
			ab_form=ab_form,
			insight_form=insight_form,
			tag_id=tag_id
		)

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
				result = db.sql_to_df(query)
			elif page == 'salescycle':
				awareness = db.sql_to_df("select distinct tactic from dbo.awareness WHERE customer_id=%d" % (user,))
				awareness.insert(loc=0, column='stage', value='awareness')

				evaluation = db.sql_to_df("select distinct tactic from dbo.evaluation WHERE customer_id=%d" % (user,))
				evaluation.insert(loc=0, column='stage', value='evaluation')

				conversion = db.sql_to_df("select distinct tactic from dbo.conversion WHERE customer_id=%d" % (user,))
				conversion.insert(loc=0, column='stage', value='conversion')

				retention = db.sql_to_df("select distinct tactic from dbo.retention WHERE customer_id=%d" % (user,))
				retention.insert(loc=0, column='stage', value='retention')

				referral = db.sql_to_df("select distinct tactic from dbo.referral WHERE customer_id=%d" % (user,))
				referral.insert(loc=0, column='stage', value='referral')
				stages = [awareness, evaluation, conversion, retention, referral]

				result = pd.concat(stages)

		    
			elif page == 'audience':
				query = "SELECT * FROM dbo.audience WHERE customer_id = %s and audience_id = %s" % (user, view_id)
				result = db.sql_to_df(query)


			elif page == 'product_2':
				query = "SELECT * FROM dbo.product_list WHERE customer_id = %d and p_id = %s" % (user,view_id)
				result = db.sql_to_df(query)
			elif page == 'past':
				query = "SELECT freeform FROM dbo.past WHERE customer_id = %d" % (user,)
				result = db.sql_to_df(query)
			elif page == 'creative':
				result = 'nah'
			elif page == 'splash':
				result = 'nah'
			else:
				query = "SELECT * FROM dbo.%s WHERE customer_id = %d" % (page, user)
				result = db.sql_to_df(query)


			return result
			
		else:
			return False













