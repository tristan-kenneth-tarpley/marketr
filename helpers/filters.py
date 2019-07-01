from app import app

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
	return copy.replace("`", "'")

def tiles_to_array(copy):
	return copy.split("^")

def layout(element):
	same_row = ['100char_limit_max', '30char_limit_max', 'integer', 'currency']

	if element in same_row:
		return True

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
		'platforms': 'past'
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




