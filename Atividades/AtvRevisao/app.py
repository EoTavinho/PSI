from flask import Flask, render_template, request, url_for
import sqlite3
app = Flask(__name__)

def obter_conexao():
    
    conn = sqlite3.connect('revisao.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vizu')
def vizu():
    conn = obter_conexao()
    cursor = conn.cursor()

    usuarios = cursor.execute('SELECT * FROM usuarios').fetchall()

    conn.close()

    return render_template('vizu.html', usuarios = usuarios)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = obter_conexao()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?,?,?)', (nome, email, senha))

        conn.commit()
        conn.close()
    return render_template('register.html')


