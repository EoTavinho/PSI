# Exercício: Adicionando Cadastro e Listagem de Usuários
# Objetivo: Expandir a aplicação anterior para permitir o cadastro de múltiplos usuários e listar todos os usuários cadastrados, garantindo que apenas usuários logados possam acessar a lista.

from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta' # Necessário para gerenciar sessões

usuarios_registrados = []


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Validar credenciais
        for usuario in usuarios_registrados:
            if usuario['username'] == username and usuario['password'] == password:
                session['username'] = username
                session['funcao'] = usuario['funcao']
                # Criar um cookie para lembrar o usuário
                resposta = make_response(redirect(url_for('dashboard')))
                resposta.set_cookie('username', username, max_age=60*60*24) # Cookie válido por um dia
                return resposta
            
        return render_template('login.html', erro='Usuário ou senha inválidos.')

    # Verificar se o usuário já está logado
    if 'username' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Verificar se o usuário está na sessão
    username = session.get('username')
    if not username:
        return redirect(url_for('login')) # Redirecionar para o login se não estiver logado
    
    return render_template('dashboard.html', username=username)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']
        funcao = request.form['funcao']

        # Verificar se o usuário já existe
        for usuario in usuarios_registrados:
            if usuario['username'] == username:
                return render_template('cadastro.html', erro = 'Usuário ja cadastrado.')

        # Adicionar novo usuário à lista
        usuarios_registrados.append({'username':username, 'password':password, 'nome':nome, 'funcao':funcao})
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))

     # Obter a função do usuário logado
    funcao_usuario = session.get('funcao', 'usuário')

    # Filtrar usuários com base na função do usuário logado
    usuarios_filtrados = [
        usuario for usuario in usuarios_registrados
        if usuario.get('funcao', 'usuário') == funcao_usuario
    ]
    
    return render_template('usuarios.html', usuarios = usuarios_filtrados)
                        

@app.route('/logout', methods=['POST'])
def logout():
    # Remover usuário da sessão
    session.pop('username', None)
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0) # Excluir o cookie
    return resposta
