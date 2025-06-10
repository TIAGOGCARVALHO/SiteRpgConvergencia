from siteconvergencia import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id):
    return Usuarios.query.get(int(id))

class Usuarios(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(), nullable=False, unique=True)
    password = database.Column(database.String(), nullable=False)
    foto_perfil = database.Column(database.String(), default="default.jpg")