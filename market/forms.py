from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, ValidationError
from market.models import User, Item


class RegistrationForm(FlaskForm):

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('username already taken')

	def validate_email_address(self, email_address):
		user = User.query.filter_by(email_address=email_address.data).first()
		if user:
			raise ValidationError('an account already exist with this email address')


	username = StringField(label='username', validators=[Length(min=3, max=15)])
	email_address = StringField(label='email', validators=[Email()])
	password = PasswordField(label='password', validators=[Length(min=6)])
	confirm_password = PasswordField(label='password', validators=[EqualTo('password')])
	submit = SubmitField(label='submit')


class LoginForm(FlaskForm):
	email_address = StringField(label='email', validators=[Email()])
	password = PasswordField(label='password')
	submit = SubmitField(label='submit')

class PurchaseItemForm(FlaskForm):
	submit = SubmitField(label='purchase item')

class SellItemForm(FlaskForm):
	submit = SubmitField(label='sell item')




	