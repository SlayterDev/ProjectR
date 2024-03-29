import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'There-is-poison-in-the-punchbowl'

STRIPE_CLIENT_ID = 'ca_6261GjKW6utegioVEL6MQL4u9lDYAG0Y'
STRIPE_SECRET = 'sk_test_Q6ot8IbSOOA93Kox65OuxK7D'
STRIPE_PUBLISHABLE = 'pk_test_sCKWz16ZwHzNJD0QI8b9EUfF'

# mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['projectrlog@gmail.com']

ITEMS_PER_PAGE = 10