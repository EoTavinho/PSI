from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo ao Flask"

@app.route('/sobre')
def sobre():
    return "Esta é a página Sobre"

@app.route('/saudacao/<nome>')
def saudacao(nome):
    return f'Ola, {nome}! Bem-vindo ao Flask!'
