from app import app
import datetime

def check_active(val, page):
	if val == page:
		return 'active'
	else:
		return val

def breadcrumb_active(name, view):
	if view == name:
		return 'page'
	else:
		return ''
		

def remove_first_char(word):
	return word[1:]

def clean_chars(copy):
	return copy.replace("`", "'").replace("\\", "")

def tiles_to_array(copy):
	if copy != None:
		return copy.split("^")
	else:
		return [copy]

def layout(element):
	same_row = ['100char_limit_max', '30char_limit_max', 'integer', 'currency', 'website']

	if element in same_row:
		return True
	else:
		return False

def is_even(num):
	if num % 2 == 0:
		return True
	else:
		return False

def form_route_map(title):
	pages = {
		'profile': 'competitors',
		'competitors': 'company',
		'company': 'audience',
		'audience': 'product',
		'product': 'product_2',
		'product_2': 'salescycle',
		'salescycle': 'nice',
		'goals': 'history',
		'history': 'platforms',
		'platforms': 'past',
		'past': 'home'
	}
	
	return pages[title]


def splash_page(title):
	splashes = ['init_setup', 'competitors', 'company', 'audience', 'product_2', 'salescycle', 'goals']

	if title in splashes:
		return True
	else:
		return False

def tiles(type_in):
	tiles = ['tiles_single_select', 'tiles_multi_select', 'tiles_multi_select_with_%']
	if type_in in tiles:
		return True
	else:
		return False

def perc_array(p):
	names = ['storefront_perc', 'direct_perc', 'online_perc', 'tradeshows_perc', 'other_perc']
	return names

def call_macro(ref):
	return 'hi'

def customPages(page):
	names = ['salescycle', 'history', 'platforms', 'past']
	if page in names:
		return True
	else:
		return False

def not_none(input):
	if input != None and input != "":
		return True
	else:
		return False

def get_first_five(input):
	return input[:4]

def to_date(date):
	return format(datetime.datetime.fromtimestamp(date), '%m/%d/%Y')

def currency(num):
	num = str(num).replace(",", "")
	return "{:,.2f}".format(float(num))

def add_commas(num):
	return "{:,}".format(num)

def capitalize(string):
	return string.capitalize()

def get_date(placeholder):
	date = str(datetime.datetime.utcnow()).replace(" ", "_")
	return date

app.jinja_env.filters['capitalize'] = capitalize
app.jinja_env.filters['to_date'] = to_date
app.jinja_env.filters['remove_first_char'] = remove_first_char
app.jinja_env.filters['check_active'] = check_active
app.jinja_env.filters['breadcrumb_active'] = breadcrumb_active
app.jinja_env.filters['clean_chars'] = clean_chars
app.jinja_env.filters['tiles_to_array'] = tiles_to_array
app.jinja_env.filters['layout'] = layout
app.jinja_env.filters['is_even'] = is_even
app.jinja_env.filters['form_route_map'] = form_route_map
app.jinja_env.filters['splash_page'] = splash_page
app.jinja_env.filters['tiles'] = tiles
app.jinja_env.filters['perc_array'] = perc_array
app.jinja_env.filters['customPages'] = customPages
app.jinja_env.filters['not_none'] = not_none
app.jinja_env.filters['get_first_five'] = get_first_five
app.jinja_env.filters['currency'] = currency
app.jinja_env.filters['add_commas'] = add_commas
app.jinja_env.filters['get_date'] = get_date



