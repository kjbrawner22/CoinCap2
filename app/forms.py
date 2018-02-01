from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired("Both fields are required."), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired("Email field is required."), Email()])
	password = PasswordField('Password', validators=[DataRequired('Password field is required.')])
	password2 = PasswordField('Repeat Password', validators=[DataRequired('Must repeat password.'), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('This email address is already in use.')