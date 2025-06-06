from siteconvergencia import app, database
from siteconvergencia.models import Usuarios

with app.app_context():
    database.drop_all()
    database.create_all()