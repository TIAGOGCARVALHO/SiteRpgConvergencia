from siteconvergencia import app, database
from siteconvergencia.forms import LoginForm, RegisterForm, CriarFichaForm
from flask import render_template, url_for, request, flash, redirect
from siteconvergencia.models import Usuarios, Ficha
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os

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
                par_next = request.args.get('next')
                if par_next:
                    return redirect(par_next)
                else:
                    return redirect(url_for('area_usuario'))
            else:
                flash('Usuario e/ou senha estão incorretos ou não existem.', 'alert-danger')
        else:
            flash('Usuario e/ou senha estão incorretos ou não existem.', 'alert-danger')

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


def salvar_imagem(imagem):
    # Gera um nome de arquivo aleatório e seguro
    codigo = secrets.token_hex(8)
    # Pega a extensão do arquivo original
    _, extensao = os.path.splitext(imagem.filename)
    # Combina o código aleatório com a extensão para criar o nome final
    nome_arquivo = codigo + extensao
    # Define o caminho completo onde a imagem será salva
    caminho_completo = os.path.join(app.root_path, 'static/fotos_personagens', nome_arquivo)
    # Salva o arquivo no caminho definido
    imagem.save(caminho_completo)
    return nome_arquivo


@app.route('/AreaUsuario')
@login_required
def area_usuario():
    fichas_usuario = Ficha.query.filter_by(id_usuario=current_user.id).all()
    return render_template('areausuario.html', fichas=fichas_usuario)


# ROTA MODIFICADA
@app.route('/criar_ficha', methods=['GET', 'POST'])
@login_required
def criar_ficha():
    form = CriarFichaForm()
    if form.validate_on_submit():
        # Lógica para salvar a foto
        if form.foto_personagem.data:
            nome_imagem = salvar_imagem(form.foto_personagem.data)
        else:
            nome_imagem = 'default_char.jpg' # Usa a imagem padrão se nenhuma for enviada

        # Cria a nova ficha com os dados do formulário
        nova_ficha = Ficha(nome_personagem=form.nome_personagem.data,
                             foto_personagem=nome_imagem,
                             dono=current_user)
        # Adiciona ao banco de dados
        database.session.add(nova_ficha)
        database.session.commit()
        flash(f'Ficha para "{form.nome_personagem.data}" criada com sucesso!', 'alert-success')
        return redirect(url_for('area_usuario'))
    return render_template('criar_ficha.html', form=form)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('pagina_inicial'))