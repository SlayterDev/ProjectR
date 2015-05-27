from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class SignupUserForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	verifyPass = PasswordField('verifyPass', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])

class SignupLandlordForm(Form):
	email = StringField('email', validators=[DataRequired()])
	property_name = StringField('property_name', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	verifyPass = PasswordField('verifyPass', validators=[DataRequired()])

class LoginLandlordForm(Form):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class LoginUserForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class PropertySelectForm(Form):
	unit = StringField('unit', validators=[DataRequired()])

class VerifyCodeSelectForm(Form):
	code = StringField('code', validators=[DataRequired()])
