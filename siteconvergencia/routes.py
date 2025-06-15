from siteconvergencia import app, database
from siteconvergencia.forms import LoginForm, RegisterForm, CriarFichaForm, ExcluirFichaForm
from flask import render_template, url_for, request, flash, redirect, abort
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


@app.route('/ficha/<int:ficha_id>')
@login_required
def ver_ficha(ficha_id):
    # Procura a ficha pelo ID
    ficha = Ficha.query.get_or_404(ficha_id)
    # Garante que o usuário só possa ver as próprias fichas
    if ficha.dono != current_user:
        abort(403) # Código de erro para "Proibido"

    # Cria o formulário de exclusão para ser usado no modal
    form_excluir = ExcluirFichaForm()

    return render_template('ver_ficha.html', ficha=ficha, form_excluir=form_excluir)


@app.route('/ficha/<int:ficha_id>/excluir', methods=['POST'])
@login_required
def excluir_ficha(ficha_id):
    # Busca a ficha ou retorna erro 404
    ficha_para_excluir = Ficha.query.get_or_404(ficha_id)

    # Verifica se o usuário é o dono da ficha
    if ficha_para_excluir.dono != current_user:
        abort(403)  # Proibido

    form_excluir = ExcluirFichaForm()

    # Validação da senha
    if form_excluir.validate_on_submit():
        if current_user.password == form_excluir.password.data:
            # Senha correta, proceder com a exclusão
            try:
                # 1. Deletar a imagem do personagem do servidor
                caminho_imagem = os.path.join(app.root_path, 'static/fotos_personagens',
                                              ficha_para_excluir.foto_personagem)
                if os.path.exists(caminho_imagem) and ficha_para_excluir.foto_personagem != 'default_char.jpg':
                    os.remove(caminho_imagem)

                # 2. Deletar a ficha do banco de dados
                database.session.delete(ficha_para_excluir)
                database.session.commit()

                flash('Ficha excluída com sucesso!', 'alert-success')
                return redirect(url_for('area_usuario'))
            except Exception as e:
                # Em caso de erro, desfaz a transação e informa o usuário
                database.session.rollback()
                flash(f'Ocorreu um erro ao excluir a ficha: {e}', 'alert-danger')
        else:
            # Senha incorreta
            flash('Senha incorreta. A exclusão foi cancelada.', 'alert-danger')
    else:
        # Se o formulário não for válido por algum motivo (ex: campo vazio)
        flash('Ocorreu um erro na validação do formulário. Tente novamente.', 'alert-danger')

    # Se a exclusão falhar, redireciona de volta para a página da ficha
    return redirect(url_for('ver_ficha', ficha_id=ficha_id))