from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	coins = db.relationship('Coin', backref='holder', lazy='dynamic')

	def __repr__(self):
		return '<User %s>' % self.email

class Coin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(5), index=True, unique=True)
	amount = db.Column(db.Integer, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Coin %s>' % self.symbol