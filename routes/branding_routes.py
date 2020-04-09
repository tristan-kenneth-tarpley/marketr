from app import app
from flask import render_template, session, redirect
from services.Blog import Blog

@app.route('/')
def index():
	return redirect('https://site.marketr.life')
    # return render_template(
	# 	'branding/index.html',
	# 	logged_in = True if session.get('logged_in') == True else False,
	# 	home=True
	# )


@app.route('/blog')
def blog():
	blog = Blog()
	posts = blog.all_stories()
	# return str(posts)
	return render_template('branding/blog.html', posts=posts)

@app.route('/blog/<slug>')
def article(slug):
	blog = Blog()
	return render_template('branding/post.html', post=blog.single_story(slug))


@app.route('/privacy')
def privacy():
	return render_template('branding/privacy.html')

@app.route('/terms_of_service')
def terms():
	return render_template('branding/terms_of_service.html')

@app.route('/terms_and_conditions')
def terms_and_conditions():
	return render_template('branding/termsandconditions.html')