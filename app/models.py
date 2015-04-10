from app import db

class Landlord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(154))
	property_name = db.Column(db.String(140))
	stripe_id = db.Column(db.String(140))
	stripe_key = db.Column(db.String(140))
	tenants = db.relationship('User', backref='landlord', lazy='dynamic')

	def __repr__(self):
		return '<Landlord %r>' % (self.property_name)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(154))
	email = db.Column(db.String(120), index=True, unique=True)
	landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))

	def __repr__(self):
		return '<User %r>' % (self.username)