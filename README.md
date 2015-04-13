# ProjectR
Project R. Shhhhh it's a secret

### Initial Setup

    curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python
    sudo easy_install virtualenv
    git clone https://github.com/SlayterDev/ProjectR.git
    cd ProjectR
    virtualenv flask
    flask/bin/pip install -r requirements.txt
    ./createDB.py
    ./db_upgrade

The application is now setup. To run use `./run.py` and go to http://127.0.0.1:8000

### Development

    git checkout develop
    git pull
    ./db_upgrade
    git checkout -b myFeature
    Do some stuff...
    git add .
    git commit -m "Did stuff"
    git push -u origin myFeature
    
### Test Info

When testing payments, use the following payment info:

    Card #: 4242 4242 4242 4242
    Exp Date: Any time in the future
    CVC: Any 3 digit number
    
When connecting a new landlord to Stripe, there is a link at the top of the page after clicking the 'connect' button that says "Skip this account form". Click that.

