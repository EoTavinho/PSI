from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta' # Necessário para gerenciar sessões

usuarios_registrados = []

usuarios = {
    'admin': 'senha123',
    'tavinho': 'chama123',
    'digas': 'nabota123',
    'rafael': 'hideonbush'
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Usuário e senha pré-definidos
        # if username == 'admin' and password == 'senha123':
        if username in usuarios and usuarios[username] == password:
            # Salvar usuário na sessão
            session['username'] = username
            # Criar um cookie para lembrar o usuário
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60*60*24) # Cookie válido por um dia
            return resposta
        else:
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

        # Verificar se o usuário já existe
        for usuario in usuarios_registrados:
            if usuario['username'] == username:
                return render_template('cadastro.html', erro = 'Usuário ja cadastrado.')
            
        # Adicionar novo usuário à lista
        usuarios_registrados.append({'username':username, 'password':password, 'nome':nome})
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Remover usuário da sessão
    session.pop('username', None)
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0) # Excluir o cookie
    return resposta
