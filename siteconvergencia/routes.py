from siteconvergencia import app, database
from siteconvergencia.forms import LoginForm, RegisterForm
from flask import render_template, url_for, request, flash, redirect
from siteconvergencia.models import Usuarios
from flask_login import login_user
@app.route('/')
def pagina_inicial():
    return render_template('paginainicial.html')


@app.route('/Entrar', methods=['GET', 'POST'])
def entrar():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        usuario = Usuarios.query.filter_by(username=loginform.username.data).first()
        if usuario:
            if loginform.password.data == usuario.password:
                login_user(usuario, remember=loginform.remember.data)
                flash(f'Usuario {loginform.username.data} iniciado com sucesso!', 'alert-success')
                return redirect(url_for('area_usuario'))
    return render_template('entrar.html', loginform=loginform)


@app.route('/CriarConta', methods=['GET', 'POST'])
def criar_conta():
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        usuario = Usuarios(username=registerform.username.data, password=registerform.password.data)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Usuario {registerform.username.data} criado com sucesso!', 'alert-success')
        return redirect(url_for('entrar'))
    return render_template('criarconta.html', registerform=registerform)

@app.route('/AreaUsuario')
def area_usuario():
    return render_template('areausuario.html')
