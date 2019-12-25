import os

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
TRANSLATION_CALLBACK = 'https://full-stack-challenge-unbabel.herokuapp.com/translations/'

# these should not be stored here ideally
UNBABEL_API_KEY = '9db71b322d43a6ac0f681784ebdcc6409bb83359'
UNBABEL_API_USERNAME = 'fullstack-challenge'