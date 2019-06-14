from helpers.helpers import *
import time
import datetime
import zipcodes
from data.db import db, sql_to_df
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

	def hide(self, page, index, trigger):
		self.set_biz_model()
		self.set_selling_to()
		self.set_num_products()
		cursor = db.cursor()
		if trigger == 'biz_model':
			query ="SELECT hide_val FROM dbo.branches WHERE branch_action = 'hide' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?"
			test_query = query.replace("?", "%s")
			data = cursor.execute(query, (trigger, self.biz_model, page, index))
		elif trigger == 'selling_to':
			query ="SELECT hide_val FROM dbo.branches WHERE branch_action = 'hide' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?"
			test_query = query.replace("?", "%s")
			data = cursor.execute(query, (trigger, self.selling_to, page, index))
            

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
		cursor = db.cursor()
		if trigger == 'selling_to':
			data = cursor.execute("SELECT mask_val, default_mask FROM dbo.branches WHERE branch_action = 'mask' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?", (trigger, self.selling_to, page, index))
		elif trigger == 'biz_model':
			data = cursor.execute("SELECT mask_val, default_mask FROM dbo.branches WHERE branch_action = 'mask' AND branch_trigger=? AND branch_trigger_val = ? AND affected_page=? AND ind=?", (trigger, self.biz_model, page, index))
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





