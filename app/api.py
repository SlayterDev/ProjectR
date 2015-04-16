from flask import redirect, session, url_for, request, g, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from app import app
from .models import User

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
	return jsonify({'token': token.decode('ascii')})
