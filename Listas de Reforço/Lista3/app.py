#Exercício: Criando um Formulário com Flask para Processar Requisições GET e POST
#Objetivo: Aprender a usar formulários em templates Flask, processar dados usando métodos GET e POST, e manipular objetos de requisição com request.

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Pagina Inicial"

@app.route('/formulario', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        nome = request.form.get('nome')
        comentario = request.form.get('comentario')
        return f"Obrigado pelo feedback, {nome}! Comentario Recebido {comentario}"
    return render_template('formulario.html')