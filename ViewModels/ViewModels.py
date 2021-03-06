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
from services.TacticsService import TacticsService
from services.AdSpend import GetRec
from services.Blog import Blog
import services.forms as forms
import json
import itertools
from services.PaymentsService import PaymentsService

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
						NOT EXISTS (select * from should_show(e.relevant_tags, %s))
						OR
						e.relevant_tags IS null
					)

					ORDER BY e.order_on_page
 

					""" % (self.title, self.id)

			data, cursor = db.execute(query, True, ())
			data = data.fetchall()
			cursor.close()
			return data

		columns = ['q_id', 'page_id', 'page_title', 'page_h1', 'page_p', 'label', 'why_asking_binary', 'why_label', 'what_binary', 'what_label', 'required_binary', 'label_p', 'horizontal_separator_binary', 'container_binary', 'answer_type', 'placeholder', 'a_format', 'html_name', 'route', 'tiles_name_h6', 'tiles_name_p', 'icon_file_path', 'sub_name', 'relevant_tags', 'order_on_page', 'q_group']
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
			"tags": self.tags,
			"campaigns": self.campaigns,
			"None": True
		}
		return switcher[case]

	def campaigns(self):
		query = "select facebook_id, google_id, twitter_id from customer_basic where id = ?"
		data, cursor = db.execute(query, True, (self.user,))
		data = cursor.fetchone()

		meta = self.admin_dashboard()
		self.accounts = {
			'facebook_id': data[0],
			'google_id': data[1],
			'twitter_id': data[2],
			'meta': self.admin_dashboard()
		}
	
	def tags(self):
		tags = TacticService(tag_id=self.tag_id)
		meta = tags.meta()
		self.total_tags = tags.count()
		self.tactic_id = meta['0']['tactic_id']
		self.tactic_title = meta['0']['title']
		self.tactic_description = meta['0']['description']
		self.image = meta['0']['image']
		self.category = meta['0']['category']

	def admin_dashboard(self):
		query = 'SELECT * from admin_dashboard(?)'
		returned, cursor = db.execute(query, True, (self.user,))
		returned = cursor.fetchone()

		if returned[2]:
			num_campaigns = returned[5]
			plan = f'{num_campaigns} active campaigns'
		elif returned[3]:
			plan = 'Almost free'
		elif returned[4]:
			plan = 'Ads Premium'
		else:
			plan = 'No Active Plan'
			temp_data = None

		_return = {
			'funds_remaining': returned[0],
			'spend_rate': returned[1],
			'plan': plan,
			'num_campaigns': returned[5],
			'data_synced': True if returned[6] else False,
			'phone': returned[7],
			'email': returned[8],
			'analytics': returned[9],
			'company_name': returned[10],
			'real_customer': returned[11]
		}

		return _return

	def acct_mgmt(self):
		service = AdminUserService(self.user, self.admin)
		messages = service.messaging.get_messages()
		tasks = service.tasks.get_tasks()
		self.task_form = forms.TaskForm()
		self.customer_name = self.admin_service.get_customer_name(self.user)
		insights_service = InsightsService(self.user, admin_id=self.admin, user='admin')
		insights = insights_service.fetch()

		returned = self.admin_dashboard()
		
		self.data = {
			'tasks': tasks,
			'insights': insights,
			'messages': messages,
			'customer': returned
		}

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
		query = "select * from compile_home_page(?)"
		core_data, cursor = db.execute(query, True, (self.customer_id,))
		core_data = cursor.fetchone()
		return_dict = {} #anchor2
		for i in range(len(core_data)):
			return_dict[i] = core_data[i]

		return return_dict
	
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
		try:
			return_data = {
				'awareness': data[0].split("^") if data[0] else None,
				'evaluation': data[1].split("^") if data[1] else None,
				'conversion': data[2].split("^") if data[2] else None,
				'retention': data[3].split("^") if data[3] else None,
				'referral': data[4].split("^") if data[4] else None
			}
		except KeyError:
			return_data = {
				'awareness',
				'evaluation',
				'conversion',
				'retention',
				'referral'
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

	
	def compile_tactics(self) -> dict:
		tactics = TacticsService(self.customer_id)
		return tactics.get()

	def compile_all(self) -> None:
		core = self.compile_core()
		core_data = core
		core_values = eval(core[0])

		def clean_salescycle(row):
			if row:
				core = eval(row)
			else:
				return None
			base = core['salescycle'][0]
			struct = {
				'awareness': base.get('awareness').split('^') if base.get('awareness') else "",
				'evaluation': base.get('evaluation').split('^') if base.get('evaluation') else "",
				'conversion': base.get('conversion').split('^') if base.get('conversion') else "",
				'retention': base.get('retention').split('^') if base.get('retention') else "",
				'referral': base.get('referral').split('^') if base.get('referral') else ""
			}
			return struct
		
		return_data = {
			'core': core_values,
			'products': eval(core_data[1]) if core_data[1] else "",
			'audiences': eval(core_data[2]) if core_data[2] else "",
			'platforms': eval(core_data[3]) if core_data[3] else "",
			'messages': eval(core_data[4]) if core_data[4] else "",
			'tasks': eval(core_data[5]) if core_data[5] else "",
			'google': eval(core_data[6]) if core_data[6] else "",
			'tests': eval(core_data[7]) if core_data[7] else "",
			'salescycle': clean_salescycle(core_data[8]),
			'insights': eval(core_data[9]) if core_data[9] else "",
			'temp_ad_data': eval(core_data[10]) if core_data[10] else None,
			'achievements': eval(core_data[11]) if core_data[11] else None,
			'all_tactics': eval(core_data[12]) if core_data[12] else None,
			'rewards': eval(core_data[13]) if core_data[13] else None,
			'spend_rec': eval(core_data[14] if core_data[14] else None),
			'recommendations': eval(core_data[15]) if core_data[15] else None
		}

		self.data = return_data



class ViewFuncs:


	def view_page(user_name=None, user=None, form=None, view_page=None, next_page=None, coming_home=True, splash=False, onboarding_complete=False, onboarding=False):

		page = IntakeViewModel(user, user_name, title=view_page)
		splashVM = SplashViewModel(next_step=view_page)
		splashes = splashVM.splashes()


		if view_page in splashes and splash == None and coming_home == None:
			return redirect(url_for('splash', next_step=view_page))
		elif view_page not in splashes or splash:
			return render_template("layouts/intake_layout.html", onboarding=onboarding, onboarding_complete=onboarding_complete, page=page, form=form)
		else:
			return render_template("layouts/intake_layout.html", onboarding=onboarding, onboarding_complete=onboarding_complete, page=page, form=form)

	def view_admin(page=None, tag_id=None, owner=False, admin=False, manager=False, form=None, temp_form=None, csv_form=None, ab_form=None, insight_form=None):
		return render_template(
			'layouts/admin_layout.html',
			page=page,
			sub=True, owner=owner,
			admin=admin,
			manager=manager,
			form=form,
			csv_form=csv_form,
			temp_form=temp_form,
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



class SettingsViewModel:
	def __init__(self, email, customer_id=None, stripe_id=None, root=True, sub_id=None):
		self.customer_id = customer_id
		self.stripe_id = stripe_id
		self.root = root
		self.sub_id = sub_id
		self.stripe_obj = PaymentsService(email, customer_id=stripe_id)
		self.compile()

	def get_stripe(self):
		self.plans = self.stripe_obj.fetch_plans()
		self.invoices = self.stripe_obj.invoices()

	def get_customer_data(self):
		query = "SELECT * FROM settings_view(?)"
		data, cursor = db.execute(query, True, (self.customer_id,))
		data = cursor.fetchone()
		self.customer = {
			'first_name': data[0],
			'current_plan': False if not data[1] else True,
			'almost_free': False if not data[2] else True,
			'ad_mid': False if not data[3] else True,
			'ad_premium': False if not data[4] else True,
			'funds_remaining': data[5],
			'spend_rate': data[6],
			'analytics': data[7]
		}

	def subscription(self):
		data = self.stripe_obj.get_plan_meta(self.sub_id)
		self.plan_meta = {
			'amount': (data['plan']['amount']/100) if data['plan']['amount'] else 0,
			'start_date': data.get('start_date') if data.get('start_date') else 0,
			'canceled_at': data.get('canceled_at') if data['canceled_at'] else 0,
			'cancel_at': data.get('cancel_at') if data['cancel_at'] else 0
		}

	def compile(self):
		self.get_stripe()
		self.get_customer_data()

		if self.root == False:
			self.subscription()
			upcoming_invoices = self.stripe_obj.upcoming_invoices()
			past_invoices = self.stripe_obj.invoices(sub_num=self.sub_id)

			self.upcoming_invoices = {
				'amount': (upcoming_invoices['data'][0]['amount']/100),
				'start': upcoming_invoices['data'][0]['period']['start'],
				'end': upcoming_invoices['data'][0]['period']['end']
			}
			invoices = {}
			for i in range(len(past_invoices['data'])):
				invoices[i] = {
					'id': past_invoices['data'][i]['id'],
					'amount_due': (past_invoices['data'][i]['amount_due']/100),
					'status': 'paid' if past_invoices['data'][i]['amount_due'] == past_invoices['data'][i]['amount_paid'] else 'open',
					'due': past_invoices['data'][i]['created']
				}
			self.past_invoices = invoices
			

class AdAuditViewModel:
	def __init__(self, admin_id=None, customer_id=None):
		self.admin_id = admin_id
		self.user = customer_id

	def history(self):
		pass





class TacticViewModel:
	def __init__(self, tactic_id):
		self.tactic_id = tactic_id
	
	def compile(self):
		query = "SELECT title, description, tactic_id FROM tactics WHERE tactic_id = ?"
		data, cursor = db.execute(query, True, (self.tactic_id,))
		data = cursor.fetchone()
		self.data = {
			'title': data[0],
			'description': data[1],
			'id': data[2]
		}

class TacticOfTheDay:
	def __init__(self, customer_id):
		self.customer_id = customer_id

	def get(self):
		query = """EXEC get_tactics @customer_id = ?"""
		data, cursor = db.execute(query, True, (self.customer_id,))
		data = cursor.fetchone()
		returned = {
			'title': data[0] if data else None,
			'description': data[1] if data else None,
			'id': data[2] if data else None
		}
		return returned


class CompetitorViewModel:
	def __init__(self, customer_id=None):
		self.customer_id = customer_id

	def get_meta(self):
		query = "SELECT comp_1_name, comp_1_website, comp_1_type, comp_2_name, comp_2_website, comp_2_type FROM competitors WHERE customer_id = ?"
		data, cursor = db.execute(query, True, (self.customer_id,))
		data = cursor.fetchone()
		returned = {
			'comp_1_name': data[0],
			'comp_1_website': data[1],
			'comp_1_type': data[2],
			'comp_2_name': data[3],
			'comp_2_website': data[4],
			'comp_2_type': data[5]
		}
		return returned

	def get(self, service):
		def clean_urls(struct):
			def clean(val):
				struct[val] = struct[val].replace('\\', '').replace('http://', '').replace('/','').replace('https://','')

			clean_list = ['comp_1_website', 'comp_2_website']
			for url in clean_list:
				clean(url)
				

		core_values = self.get_meta()
		clean_urls(core_values)

		try:
			core_values.update([('competitor_intro_1', service.intro(core_values.get('comp_1_website')))])
		except:
			core_values.update([('competitor_intro_1', "")])
		try:
			core_values.update([('competitor_intro_2', service.intro(core_values.get('comp_2_website')))])
		except:
			core_values.update([('competitor_intro_2', "")])

		return core_values

