from app import app

def check_active(val, page):
	if val == page:
		return 'active'
	else:
		return val

def breadcrumb_active(val, level, page):
	if level == 'step':
		if val == page:
			return 'step_active'
		else:
			return ''
	elif level == 'step_name':
		if val == page:
			return "sub_active"
		else:
			return ''

app.jinja_env.filters['check_active'] = check_active
app.jinja_env.filters['breadcrumb_active'] = breadcrumb_active