#!venv/bin/python3

from app import app, db
from app.models import User, Coin

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Coin': Coin}

app.run(debug=True)