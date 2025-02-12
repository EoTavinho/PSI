from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configura o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

DATABASE = 'database.db'

# Função para obter conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Criação do banco de dados e tabelas se não existirem
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Criação da tabela de exercícios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Inicializa o banco de dados na primeira execução
if not os.path.exists(DATABASE):
    init_db()

# Classe de Usuário para Flask-Login
class User(UserMixin):
    def __init__(self, id, matricula, email, password):
        self.id = id
        self.matricula = matricula
        self.email = email
        self.password = password

    @staticmethod
    def get_by_matricula(matricula):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE matricula = ?', (matricula,)).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['matricula'], user['email'], user['password'])
        return None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['matricula'], user['email'], user['password'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))  # Convertendo user_id para inteiro

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method='sha256')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (matricula, email, password) VALUES (?, ?, ?)',
                         (matricula, email, hashed_password))  # Não hashear o email
            conn.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Matrícula já cadastrada.')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        password = request.form['password']

        user = User.get_by_matricula(matricula)

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Matrícula ou senha incorretos.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_authenticated or current_user.id is None:
        flash('Erro ao carregar o painel. Por favor, faça login novamente.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    exercises = conn.execute('SELECT * FROM exercises WHERE user_id = ?', (current_user.id,)).fetchall()
    conn.close()
    return render_template('dashboard/dashboard.html', exercises=exercises)

@app.route('/add_exercise', methods=['GET', 'POST'])
@login_required
def add_exercise():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO exercises (name, description, user_id) VALUES (?, ?, ?)',
                     (name, description, current_user.id))
        conn.commit()
        conn.close()

        flash('Exercício adicionado com sucesso!')
        return redirect(url_for('dashboard'))

    return render_template('add_exercise.html')

if __name__ == '__main__':
    app.run(debug=True)
