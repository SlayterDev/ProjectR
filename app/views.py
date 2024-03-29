from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from config import STRIPE_CLIENT_ID, STRIPE_SECRET, STRIPE_PUBLISHABLE, ITEMS_PER_PAGE
from datetime import datetime
from .models import User, Landlord, Transaction
from .forms import SignupUserForm, SignupLandlordForm, LoginLandlordForm, LoginUserForm
from .forms import PropertySelectForm
import requests
import stripe

@lm.user_loader
def load_user(id):
	strings = id.split()

	if strings[1] == 'u':
		return User.query.get(int(strings[0]))
	else:
		return Landlord.query.get(int(strings[0]))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/landlordSignUp', methods=['GET', 'POST'])
def landlordSignUp():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = SignupLandlordForm()
	if form.validate_on_submit():
		landlord = Landlord.query.filter_by(email=form.email.data).first()
		if landlord is not None:
			flash('That email is already registered')
			return redirect(url_for('landlordSignUp'))
		if form.password.data != form.verifyPass.data:
			flash('Password fields do not match')
			return redirect(url_for('landlordSignUp'))

		landlord = Landlord(email=form.email.data, 
							property_name=form.property_name.data)
		landlord.hash_password(form.password.data)
		db.session.add(landlord)
		db.session.commit()
		login_user(landlord, remember=False)
		flash('Signed up and logged in!')
		return redirect(url_for('landlordDashboard'))

	return render_template('LandlordSignUp.html', title='Sign Up',
							form=form)

@app.route('/userSignUp', methods=['GET', 'POST'])
def userSignUp():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	form = SignupUserForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None:
			flash('That username is already taken')
			return redirect(url_for('userSignUp'))
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None:
			flash('That email is already registered')
			return redirect(url_for('userSignUp'))
		if form.password.data != form.verifyPass.data:
			flash('Password fields do not match')
			return redirect(url_for('userSignUp'))
		if len(form.username.data) < 3:
			flash('Username must be at least 3 characters long')
			return redirect(url_for('userSignUp'))
		if len(form.password.data) < 6:
			flash('Password must be at least 6 characters long')
			return redirect(url_for('userSignUp'))

		user = User(username=form.username.data,
					email=form.email.data)
		user.hash_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user, remember=False)
		flash('Signed up and logged in')
		return redirect(url_for('userDashboard'))

	return render_template('UserSignup.html', title='Sign Up',
							form=form)

@app.route('/login')
def login():
	dest = request.args.get('next')

	if dest is None:
		return redirect(url_for('index'))

	if 'landlord' in dest.lower() or 'redirect' in dest.lower():
		return redirect(url_for('loginLandlord'))
	else:
		return redirect(url_for('loginUser'))

@app.route('/loginLandlord', methods=['GET', 'POST'])
def loginLandlord():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	form = LoginLandlordForm()
	if form.validate_on_submit():
		landlord = Landlord.query.filter_by(email=form.email.data).first()
		if landlord is None:
			flash('Invalid email or password')
			return redirect(url_for('loginLandlord'))
		if not landlord.verify_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('loginLandlord'))

		login_user(landlord, remember=False)
		flash('Logged in successfully')
		return redirect(url_for('landlordDashboard'))

	return render_template('LoginLandlord.html', title='Login',
							form=form)

@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():	
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	form = LoginUserForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			flash('Invalid username or password')
			return redirect(url_for('loginUser'))
		if not user.verify_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('loginUser'))

		login_user(user, remember=False)
		flash('Logged in successfully')
		return redirect(url_for('userDashboard'))

	return render_template('LoginUser.html', title='Login',
							form=form)

@app.route('/userDashboard')
@login_required
def userDashboard():
	return render_template('UserDashboard.html', title='Dashboard')

@app.route('/chooseProperty')
@app.route('/chooseProperty/<int:page>')
@login_required
def chooseProperty(page=1):
	properties = Landlord.query.order_by(Landlord.property_name.asc())
	properties = properties.paginate(page, ITEMS_PER_PAGE, False)

	return render_template('ChooseProperty.html', title='Choose Property',
							properties=properties)

@app.route('/setProperty/<name>', methods=['GET', 'POST'])
@login_required
def setProperty(name):
	landlord = Landlord.query.filter_by(property_name=name).first()

	if landlord is None:
		flash('An error has occured. That property doesn\'t exist')
		return redirect(url_for('chooseProperty'))

	user = g.user
	user.landlord = landlord

	form = PropertySelectForm()
	if form.validate_on_submit():
		user.unit = form.unit.data
		db.session.add(user)
		db.session.commit()

		return redirect(url_for('userDashboard'))


	return render_template('PropertySelect.html', title='Enter Unit Number',
							name=name, form=form)

@app.route('/landlordDashboard')
@login_required
def landlordDashboard():
	tenants = g.user.tenants.order_by(User.unit.asc())

	return render_template('landlordDashboard.html', title='Dashboard',
							tenants=tenants, clientid=STRIPE_CLIENT_ID)

@app.route('/stripeRedirect')
@login_required
def stripeRedirect():
	error = request.args.get('error')
	if error is not None:
		flash('An error has occured')
		return redirect(url_for('landlordDashboard'))

	code = request.args.get('code')
	payload = {
		'grant_type': 'authorization_code',
        'client_id': STRIPE_CLIENT_ID,
        'client_secret': STRIPE_SECRET,
        'code': code
	}

	resp = requests.post('https://connect.stripe.com/oauth/token', 
							params=payload)

	token = resp.json().get('access_token')
	key = resp.json().get('stripe_publishable_key')
	user_id = resp.json().get('stripe_user_id')
	refresh_tok = resp.json().get('refresh_token')
	landlord = g.user
	if not landlord.is_landlord(): # sanity check
		flash('This user can\'t do that')
		return redirect('index')

	landlord.stripe_key = key
	landlord.stripe_id = user_id
	landlord.stripe_access = token
	landlord.stripe_refresh = refresh_tok
	db.session.add(landlord)
	db.session.commit()

	return redirect(url_for('landlordDashboard'))

@app.route('/payrent', methods=['GET', 'POST'])
@login_required
def payrent():
	if g.user.landlord.stripe_id is None:
		flash('This property has not been set up to recieve payments yet.')
		return redirect(url_for('userDashboard'))

	return render_template('Payrent.html', title='Pay Rent',
							key=STRIPE_PUBLISHABLE)

@app.route('/charge', methods=['GET', 'POST'])
@login_required
def charge():
	amount = request.form['amount']
	try:
		amount = int(float(amount)*100) # convert amount to cents
	except ValueError, e:
		flash('Invalid amount entered')
		return redirect(url_for('payrent'))

	if amount < 100:
		flash('You must enter an amount greater than $1.00')
		return redirect(url_for('payrent'))

	token = request.form['stripeToken']
	landlord = g.user.landlord
	if landlord is None:
		flash('An error occured processing your payment')
		return redirect(url_for('userDashboard'))

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
		return render_template('Charge.html', title='Payment Failure',
								error=error)

	# Record charge
	transaction = Transaction(stripe_charge=charge['id'])
	transaction.user_id = g.user.id
	transaction.landlord_id = landlord.id
	transaction.amount = amount
	transaction.date = datetime.utcnow()

	db.session.add(transaction)
	db.session.commit()

	return render_template('Charge.html', title='Payment Successful',
							amount=amount)

@app.route('/showLandlordTransactions')
@app.route('/showLandlordTransactions/<int:page>')
@login_required
def showLandlordTransactions(page=1):
	transactions = g.user.transactions.order_by(Transaction.date.desc())
	transactions = transactions.paginate(page, ITEMS_PER_PAGE, False)

	return render_template('ShowTransactions.html', title='Show Transactions',
							transactions=transactions)

@app.route('/history')
@app.route('/history/<int:page>')
@login_required
def history(page=1):
	transactions = g.user.transactions.order_by(Transaction.date.desc())
	transactions = transactions.paginate(page, ITEMS_PER_PAGE, False)

	return render_template('ShowTransactions.html', title='Payment History',
							transactions=transactions)
