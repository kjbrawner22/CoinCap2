from operator import itemgetter
from app import app, cap
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, request, flash
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, AddCoinForm
from app.models import User, Coin

#home endpoint
@app.route('/index')
@app.route('/')
def index():
	title = "Coin Cap | Home"
	return render_template('index.html', coins=cap.ticker(limit=10), title=title)

#login endpoint
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('portfolio'))
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
			next_page = url_for('portfolio')
		return redirect(next_page)
	return render_template('login.html', title=title, form=form)

#logout endpoint
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

#register endpoint
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('portfolio'))
	title = "Coin Cap | Register"
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Success! You can login to your new account.')
		return redirect('login')
	return render_template('register.html', form=form, title=title)

#portfolio endpoint
@app.route('/portfolio')
@login_required
def portfolio():
	title = "Coin Cap | Portfolio"
	coins = []
	for coin in current_user.coins:
		c = cap.ticker(currency=coin.name)[0]
		#change rank attribute to house an int for sorting of coins
		c['rank'] = int(c['rank'])
		if c is not None:
			c['amount'] = coin.amount
			coins.append(c)
	coins.sort(key=itemgetter('amount', 'rank'))
	return render_template('portfolio.html', coins=coins, title=title)

@app.route('/add-coin', methods=['GET', 'POST'])
@login_required
def add_coin():
	title = "Coin Cap | Add Coin"
	coin_dict = {}
	for c in cap.ticker(limit=0):
		coin_dict['%s (%s)' % (c['name'], c['symbol'])] = c['id']
	form = AddCoinForm()
	if form.validate_on_submit():
		if form.search.data in coin_dict.keys():
			c = Coin(name=coin_dict[form.search.data], amount=0.0, holder=current_user)
			db.session.add(c)
			db.session.commit()
			flash('Coin added!')
			return redirect(url_for('portfolio'))
		else:
			flash('Please choose a valid option.')
			return redirect(url_for('portfolio'))
	return render_template('add-coin.html', coins=coin_dict.keys(), form=form, title=title)

@app.route('/delete-coin/<coin_id>')
@login_required
def delete_coin(coin_id):
	for coin in current_user.coins:
		if coin_id == coin.name:
			db.session.delete(coin)
			db.session.commit()
			#return right away in case of duplicate coin
			return redirect(url_for('portfolio'))
	return redirect(url_for('portfolio'))

@app.route('/portfolio/<coin_id>')
@login_required
def coin(coin_id):
	c = cap.ticker(currency=coin_id)
	#check if API returns valid coin(see 'coinmarketcap.com/api')
	if type(c) is list:
		c = c[0]
		title = "Coin Cap | %s" % c['name']
		for coin in current_user.coins:
			if c == coin.name:
				c['amount'] = coin.amount
		return render_template('coin.html', coin=c, title=title)
	else:
		#returned an error response
		flash('Unknown coin name.')
		return redirect(url_for('portfolio'))