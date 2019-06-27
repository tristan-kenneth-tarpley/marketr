from helpers.helpers import *
import time
import datetime
import zipcodes
from data.db import sql_to_df, execute
import pandas as pd


class User:
	def __init__(self, id):
		self.id = id

	def set_biz_model(self):
		self.biz_model = get_biz_model(self.id)
	def set_selling_to(self):
		self.selling_to = get_selling_to(self.id)
	def set_num_products(self):
		self.num_products = get_num_products(self.id)


	def branch(self, action, page, trigger):
		self.set_biz_model()
		self.set_selling_to()
		self.set_num_products()
		
		
		tup = (action, trigger, page)


		if action == 'hide':
		    query = "SELECT ind, hide_val, branch_trigger_val FROM dbo.branches WHERE branch_action = ? AND branch_trigger=? AND affected_page=?"

		    ind_query = "SELECT distinct ind FROM dbo.branches WHERE branch_action = 'hide' AND affected_page = ?"
		    ind_list, cursor = execute(ind_query, True, (page,))
		    ind_list = cursor.fetchall()
		    cursor.close()

		elif action == 'mask':
		    query = "SELECT mask_val, default_mask FROM dbo.branches WHERE branch_action = ? AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=?"

		data, cursor = execute(query, True, tup)
		data = data.fetchall()

		if data:

		    if action == 'hide':
		        i = 0
		        for ind in ind_list:
		            ind_list[i] = ind_list[i][0]
		            i+=1

		        return ind_list, data



	def hide(self, page, index, trigger):
		self.set_biz_model()
		self.set_selling_to()
		self.set_num_products()
		
		if trigger == 'biz_model':
			query ="SELECT hide_val FROM dbo.branches WHERE branch_action = 'hide' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?"
			test_query = query.replace("?", "%s")
			tup = (trigger, self.biz_model, page, index)
			data, cursor = execute(query, True, tup)
		elif trigger == 'selling_to':
			query ="SELECT hide_val FROM dbo.branches WHERE branch_action = 'hide' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?"
			test_query = query.replace("?", "%s")
			tup = (trigger, self.selling_to, page, index)
			data, cursor = execute(query, True, tup)
            

		data = cursor.fetchone()
		try:
			if data[0] == 1:
				cursor.close()
				return True
			else:
				cursor.close()
				return False
		except TypeError:
				print(data)
				return False


	def mask(self, page, index, trigger):
		self.set_biz_model()
		self.set_selling_to()
		self.set_num_products()

		if trigger == 'selling_to':
			tup = (trigger, self.selling_to, page, index)
			data, cursor = execute("SELECT mask_val, default_mask FROM dbo.branches WHERE branch_action = 'mask' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?", True, tup)
		elif trigger == 'biz_model':
			tup = (trigger, self.biz_model, page, index)
			data, cursor = execute("SELECT mask_val, default_mask FROM dbo.branches WHERE branch_action = 'mask' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?", True, tup)

		data = cursor.fetchone()
		
		try:
			mask = data[0]
			default = data[1]
			cursor.close()

			if mask != None:
				return mask, True
			else:
				return default, False
		except TypeError:
			new_data = cursor.execute("SELECT default_mask FROM dbo.branches WHERE branch_action = 'mask' AND branch_trigger=? AND affected_page=? AND ind=?", (trigger, page, index))
			new_data = cursor.fetchone()
			new_data = new_data[0]
			cursor.close()
			return new_data, False



stage_1 = ['competitors', 'company', 'audience', 'product', 'product_2', 'salescycle']
stage_2 = ['goals']
stage_3 = ['history', 'platforms', 'past']
stage_4 = ['creative']
class Page:
	def __init__(self, id, title, user_name):
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


















