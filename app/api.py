from flask import redirect, session, url_for, request, g, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from app import app, db
from .models import User, Transaction, Landlord
from config import STRIPE_CLIENT_ID, STRIPE_SECRET, STRIPE_PUBLISHABLE, ITEMS_PER_PAGE
from datetime import datetime
import requests
import stripe

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
	user = User.verify_auth_token(username_or_token)
	if not user:
		user = User.query.filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

@app.route('/api/resource')
@auth.login_required
def get_resource():
	return jsonify({ 'data': 'Hello, %s!' % g.user.username })

@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii'),
					'landlord': g.user.landlord.property_name,
					'email': g.user.email})

@app.route('/api/landlord')
@auth.login_required
def get_landlord():
	landlord = g.user.landlord.property_name
	return jsonify({'landlord': landlord})

@app.route('/api/charge', methods=['POST'])
@auth.login_required
def apiCharge():
	token = request.json['token']
	amount = request.json['amount']

	if token is None or amount is None:
		return jsonify({'status': 'failure',
						'reason': 'No token or amount provided'})

	landlord = g.user.landlord
	if landlord is None:
		return jsonify({'status': 'failure',
						'reason': 'No landlord set'})

	stripe.api_key = STRIPE_SECRET
	charge = stripe.Charge.create(
			amount=amount,
			currency='usd',
			source=token,
			stripe_account=landlord.stripe_id,
			description=g.user.email,
			application_fee=int(amount*0.01), # 1% fee
			statement_descriptor=landlord.property_name)

	print charge
	if charge['failure_code'] is not None:
		error = str(charge['failure_message']) + ' ' + str(charge['failure_code'])
		return jsonify({'status': 'failure',
						'reason': error})

	# Record charge
	transaction = Transaction(stripe_charge=charge['id'])
	transaction.user_id = g.user.id
	transaction.landlord_id = landlord.id
	transaction.amount = amount
	transaction.date = datetime.utcnow()

	db.session.add(transaction)
	db.session.commit()

	return jsonify({'status': 'success'})
