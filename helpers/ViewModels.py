from flask import render_template, redirect, url_for
from data.db import *
import time
import datetime
import zipcodes

class ViewFuncs:

	def view_page(form=None, page=None, coming_home=True, next_page='home', splash=False):

		if splash and not coming_home:
			return render_template('layouts/intake_layout.html', page=page)
		elif coming_home:
			return redirect('/home')
		elif not splash:
			return render_template('layouts/intake_layout.html', page=page, form=form)
		else:
			return redirect(url_for("splash", next_step=next_page))


class IntakeViewModel(ViewFuncs):
	def __init__(self, id, user_name, title=None):
		stage_1 = ['competitors', 'company', 'audience', 'product', 'product_2', 'salescycle']
		stage_2 = ['goals']
		stage_3 = ['history', 'platforms', 'past']
		stage_4 = ['creative']
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
			tup = (self.title,)
			query = """
				SELECT q.*, pages.page_title, pages.page_h1, pages.page_p, answers.*,
						STUFF((SELECT '^' + t.name_h6
									FROM tiles as t
									WHERE t.answer_id = q.answer_id
									FOR XML PATH('')), 1, 1, '') [tiles_name_h6],
						
						STUFF((SELECT '^' + t.name_p
									FROM tiles as t
									WHERE t.answer_id = q.answer_id
									FOR XML PATH('')), 1, 1, '') [tiles_name_p],

						STUFF((SELECT '^' + t.icon_image_filepath
									FROM tiles as t
									WHERE t.answer_id = q.answer_id
									FOR XML PATH('')), 1, 1, '') [icon_file_path],

						STUFF((SELECT '^' + t.name
									FROM tiles as t
									WHERE t.answer_id = q.answer_id
									FOR XML PATH('')), 1, 1, '') [sub_name],

						pages.container_binary
				
						
					FROM dbo.questions as q

				LEFT JOIN pages
					ON q.page_id = pages.page_id

				RIGHT JOIN answers
					ON answers.fk_answer_id = q.answer_id

					

				WHERE pages.page_title = ?
				ORDER BY q.order_on_page

					"""
			data, cursor = execute(query, True, tup)
			data = data.fetchall()
			cursor.close()
			return data

		self.questions = get_copy(self)
		self.header = self.questions[0][15].replace("`", "'")
		self.intro = self.questions[0][16].replace("`", "'")
		self.container = self.questions[0][29]




class Admin_View:
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

















