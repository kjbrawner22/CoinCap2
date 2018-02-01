from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from coinmarketcap import Market

app = Flask(__name__)
app.config.from_object(Config)
cap = Market()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models