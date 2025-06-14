from siteconvergencia import app, database
from siteconvergencia.models import Usuarios, Ficha # Importe o novo modelo Ficha

with app.app_context(): 
    database.drop_all()
    database.create_all()
    print("Banco de dados recriado com sucesso com as tabelas Usuarios e Ficha.")