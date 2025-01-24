from flask import Flask, render_template, session, redirect, url_for, make_response, request

app = Flask(__name__)
app.secret_key = 'chave-secreta' # Necessario para usar sessões

@app.route('/usuario', methods=['GET', 'POST'])
def salvar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        email = request.form['email']
        # Armazenando dados na sessão
        session['nome'] = nome
        session['idade'] = idade
        session['email'] = email
        # Armazenando dados em um cookie com validade de um dia
        resposta = make_response(redirect(url_for('salvar_usuario')))
        resposta.set_cookie('nome', nome, max_age=60*60*24)
        resposta.set_cookie('idade', idade, max_age=60*60*24)
        resposta.set_cookie('email', email, max_age=60*60*24)
    # Recuperando dados da sessão ou cookies
    nome = session.get('nome') or request.cookies.get('nome')
    idade = session.get('idade') or request.cookies.get('idade')
    email = session.get('email') or request.cookies.get('email')
    return render_template('usuario.html', nome=nome, idade=idade, email=email)

@app.route('/sair')
def sair():
    session.pop('nome', None)
    session.pop('idade', None)
    session.pop('email', None)
    resposta = make_response(redirect(url_for('salvar_usuario')))
    resposta.set_cookie('nome', '', max_age=0) # Exclui o cookie
    resposta.set_cookie('idade', '', max_age=0) #Exclui o cookie
    resposta.set_cookie('email', '', max_age=0) #Exclui o cookie
    return resposta