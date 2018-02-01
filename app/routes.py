from app import app, cap
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, request, flash
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
	title = "Coin Cap | Home"
	return render_template('index.html', coins=cap.ticker(limit=10), title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	title = "Coin Cap | Log In"
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title=title, form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	title="Coin Cap | Register"
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Success! You can login to your new account.')
		return redirect('login')
	return render_template('register.html', form=form, title=title)

@app.route('/add-coin', methods=['GET', 'POST'])
def add_coin():
	title = "Coin Cap | Add Coin"
	return render_template('add-coin.html', coins=cap.ticker(limit=0), title=title)
