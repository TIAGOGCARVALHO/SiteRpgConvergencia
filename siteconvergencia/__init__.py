from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = 'puddyviadao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///convergencia.db'

database = SQLAlchemy(app)

from siteconvergencia import routes