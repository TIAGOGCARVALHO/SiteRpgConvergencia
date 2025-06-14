from siteconvergencia import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id):
    return Usuarios.query.get(int(id))

class Usuarios(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(), nullable=False, unique=True)
    password = database.Column(database.String(), nullable=False)
    foto_perfil = database.Column(database.String(), default="default.jpg")
    # Adicionando o relacionamento com as fichas
    fichas = database.relationship('Ficha', backref='dono', lazy=True)

# NOVA CLASSE ADICIONADA
class Ficha(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_personagem = database.Column(database.String(), nullable=False)
    foto_personagem = database.Column(database.String(), default='default_char.jpg')
    # Chave estrangeira para ligar a ficha ao usuário
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)