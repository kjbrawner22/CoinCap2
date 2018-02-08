import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = b'\x07\xdb9\x9a\xd1\x8f%m\xfe\xfb\xfa}Q\xc9G\x7f\xef5mS\xb0!$1'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False