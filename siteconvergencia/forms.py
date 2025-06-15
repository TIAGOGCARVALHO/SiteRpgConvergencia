from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from siteconvergencia.models import Usuarios

class LoginForm(FlaskForm):
    username = StringField('Insira o seu usuário', validators=[DataRequired()])
    password = PasswordField('Insira a sua senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar dados de usuário')
    submit_login = SubmitField('Confirmar')


class RegisterForm(FlaskForm):
    username = StringField('Crie o seu usuário', validators=[DataRequired()])
    password = PasswordField('Crie a sua senha', validators=[DataRequired(), Length(8, 20)])
    confirm_password = PasswordField('Confirme a sua senha', validators=[DataRequired(), EqualTo('password')])
    submit_register = SubmitField('Finalizar criação de usuario')

    def validate_username(self, username):
        usuario = Usuarios.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Este usuário já existe, insira outro nome ou faça login')


class CriarFichaForm(FlaskForm):
    nome_personagem = StringField('Nome do Personagem', validators=[DataRequired(), Length(min=2, max=50)])
    foto_personagem = FileField('Escolha uma Foto (Opcional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit_criar_ficha = SubmitField('Criar Personagem')


class ExcluirFichaForm(FlaskForm):
    password = PasswordField('Digite sua senha para confirmar', validators=[DataRequired()])
    submit_excluir = SubmitField('Confirmar Exclusão')