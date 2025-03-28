# Exercício: Utilizando Sessões e Cookies em Flask
# Objetivo: Aprender a gerenciar sessões e cookies para armazenar informações do usuário temporariamente e persistente usando Flask.

from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta' #Necessario para usar sessoes

@app.route('/sessao', methods=['GET', 'POST'])
def iniciar_sessao():
    if request.method == 'POST':
        session['nome'] = request.form['nome'] # Armazena o nome na sessão
        return redirect(url_for('iniciar_sessao'))
    nome = session.get('nome') # Recupera o nome da sessão
    return render_template('sessao.html', nome=nome)

@app.route('/limpar_sessao')
def limpar_sessao():
    session.pop('nome', None) # Remove o nome da sessão
    return redirect(url_for('iniciar_sessao'))

@app.route('/cookie', methods=['GET', 'POST'])
def definir_cookie():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        resposta = make_response(redirect(url_for('definir_cookie')))
        resposta.set_cookie('nome', nome, max_age=60*60*24) # Cookie valido por 1 dia
        resposta.set_cookie('idade', idade, max_age=60*60*24)
        return resposta
    nome = request.cookies.get('nome')
    idade = request.cookies.get('idade')
    return render_template('cookie.html', nome=nome, idade=idade)