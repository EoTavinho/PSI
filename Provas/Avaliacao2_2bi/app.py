from flask import Flask, redirect, session, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


def obter_conexao():
    conn = sqlite3.connect('bancodados.db')
    conn.row.factory = sqlite3.Row
    return conn

login_manager = LoginManager()


login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        user = User.get_by_email(matricula)
        if user and user.senha == senha:
            login_user(user)
            return redirect(url_for('dash'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']

        conexao = obter_conexao()
        INSERT = conexao.execute('INSERT INTO usuarios(matricula, email, senha) VALUES (?,?,?)', (matricula, email, senha))
        conexao.commit()
        conexao.close()
        return redirect(url_for('dash'))
    
    return render_template('register.html')

@app.route('/dash')
@login_required
def dash():
    return 'Oi Tavin'


@app.route('/logout', method=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))