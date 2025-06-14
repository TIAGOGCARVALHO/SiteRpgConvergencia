from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'puddyviadao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///convergencia.db'

database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'pagina_inicial'
login_manager.login_message = 'faça login ou crie uma conta para acessar essa página'

from siteconvergencia import routes