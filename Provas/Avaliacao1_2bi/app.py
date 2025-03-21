from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3

DATABASE = 'escola.db'

app = Flask(__name__)

def get_connection():
    # Colocando na variável "conn" a conexão com o banco
    # sqlite3.connect(DATABASE) abre (ou cria, se não existir) o banco de dados e retorna um objeto de conexão.
    conn = sqlite3.connect(DATABASE)
    
    #sqlite3.Row permite acessar os resultados como se fossem dicionários, ou seja, os valores podem ser acessados tanto por índice quanto pelo nome da coluna.
    conn.row_factory = sqlite3.Row

    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listar')
def listar():
    #Pegando a variavel que faz conexão com o BD pela função get_connection (linha 10)
    conn = get_connection()
    #Usando (SELECT *) na tabela "users" do BD
    #Usando a função "fetchall" para pegar todas as colunas da tabela.
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    
    conn.close()
    
    return render_template('listar.html', usuarios = usuarios)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('Coloque seu nome!')
        else:
            # Se o usuario colocar o nome, o else vai rodar,  esse conn = get_connection() serve para representaro BD 
            conn = get_connection()
            #(INSERT INTO usuarios) => (Inserir na tabela usuarios)
            #qual coluna? => (nome)
            #qual o valor? => (?) por que não da pra colocar uma variavel do python direto no comando sqlite
            #logo depois do comando sqlite, coloca os valores em ordem respectiva para as interrogações
            conn.execute('INSERT INTO usuarios (nome) VALUES(?)', (nome,))
            #commit para confirmar e salvar as alterações, igual github
            conn.commit()
            #fechar a conexão, sempre lembrar de fazer
            conn.close()
            return redirect(url_for('listar'))
        
    return render_template('register.html')
    

