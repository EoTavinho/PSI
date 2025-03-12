from flask import Flask, render_template, request, redirect, make_response, url_for

app = Flask(__name__)

mensagens = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']

        if nome:
            resposta = make_response(redirect(url_for('mensagem')))
            resposta.set_cookie('nome', nome, max_age=60*60*24)
            return resposta

        return render_template('login.html', erro='Usuario incorreto')
    
    return render_template('login.html')

@app.route('/mensagem', methods=['GET', 'POST'])
def mensagem():
    nome = request.cookies.get('nome')

    if not nome:
        return redirect(url_for('login'))

    if request.method == 'POST':
        mensagem = request.form['mensagem']
        if mensagem: # Verifica se a mensagem não está vazia
            # Adiciona a mensagem à lista como um dicionário
            mensagens.append({'usuario':nome, 'texto': mensagem})


    # Filtra as mensagens do usuário atual
    mensagens_usuario = [msg['texto'] for msg in mensagens if msg['usuario'] == nome]
    return render_template('mensagem.html', nome=nome, mensagens=mensagens_usuario)
    