from siteconvergencia import app, database
from siteconvergencia.models import Usuarios

with app.app_context():
    database.drop_all()
    database.create_all()

# with app.app_context():
#     usuarios = Usuarios.query.all()
#     primeiro_usuario = Usuarios.query.first()
#     print(primeiro_usuario.username, primeiro_usuario.password)