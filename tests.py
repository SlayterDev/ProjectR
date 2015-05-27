#!flask/bin/python

import os
import unittest
import stripe

from config import basedir
from app import app, db
from app.models import User, Landlord
from coverage import coverage

cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_unique_username(self):
		u = User(username='john', email='john@email.com')
		db.session.add(u)
		db.session.commit()
		username = 'john'
		u = User.query.filter_by(username=username).first()
		assert u != None

	def test_token_authentication(self):
		u = User(username='testman', email='testman@email.com')
		u.hash_password('password')
		db.session.add(u)
		db.session.commit()
		assert u.verify_password('password')
		token = u.generate_auth_token()
		assert User.verify_auth_token(token) != None

	def test_verify_string_uniqueness(self):
		l = Landlord(email='place1@email.com', property_name='Place1')
		db.session.add(l)
		db.session.commit()

		l.create_verify_code()
		db.session.add(l)
		db.session.commit()

		l = Landlord(email='place2@email.com', property_name='Place2')
		db.session.add(l)
		db.session.commit()

		l.create_verify_code()
		db.session.add(l)
		db.session.commit()

		l = Landlord(email='place3@email.com', property_name='Place3')
		db.session.add(l)
		db.session.commit()

		l.create_verify_code()
		db.session.add(l)
		db.session.commit()

		verifyCode = l.verify_string
		properties = Landlord.query.filter_by(verify_string=verifyCode).all()
		assert len(properties) == 1

if __name__ == '__main__':
	try:
		unittest.main()
	except:
		pass
	cov.stop()
	cov.save()
	print '\n\nCoverage Report:\n'
	cov.report()
	print 'HTML version: ' + os.path.join(basedir, "tmp/coverage/index.html")
	cov.html_report(directory='tmp/coverage')
	cov.erase()
