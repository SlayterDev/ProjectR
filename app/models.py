from app import db
from passlib.apps import custom_app_context as pwd_context

class Landlord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(154))
	property_name = db.Column(db.String(140), index=True, unique=True)
	stripe_id = db.Column(db.String(140))
	stripe_key = db.Column(db.String(140))
	stripe_refresh = db.Column(db.String(140))
	stripe_access = db.Column(db.String(140))
	tenants = db.relationship('User', backref='landlord', lazy='dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_landlord(self):
		return True

	def get_id(self):
		try:
			return unicode(str(self.id)+' l')
		except NameError:
			return str(self.id+' l')

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	def __repr__(self):
		return '<Landlord %r>' % (self.property_name)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(154))
	email = db.Column(db.String(120), index=True, unique=True)
	landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))
	unit = db.Column(db.String(10))

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_landlord(self):
		return False

	def get_id(self):
		try:
			return unicode(str(self.id)+' u')
		except NameError:
			return str(self.id+' u')

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	def __repr__(self):
		return '<User %r>' % (self.username)

class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))
	stripe_charge = db.Column(db.String(140))

	def __repr__(self):
		return '<Transaction %r>' % (self.stripe_charge)
