from app import app, cap
from flask import render_template, redirect
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
	title = "Coin Cap | Home"
	return render_template('index.html', coins=cap.ticker(limit=10), title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
	title = "Coin Cap | Log In"
	form = LoginForm()
	if form.validate_on_submit():
		return redirect('/')
	return render_template('login.html', title=title, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		redirect('/')
	return render_template('register.html', form=form)

@app.route('/add-coin')
def add_coin():
	title = "Coin Cap | Add Coin"
	return render_template('add-coin.html', coins=cap.ticker(limit=0), title=title)
