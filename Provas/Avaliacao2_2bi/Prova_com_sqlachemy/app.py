from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        email = request.form.get('email')
        password = request.form.get('password')

        user_exists = User.query.filter((User.matricula == matricula) | (User.email == email)).first()
        if user_exists:
            flash('Matrícula ou e-mail já cadastrados.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(matricula=matricula, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        password = request.form.get('password')

        user = User.query.filter_by(matricula=matricula).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Matrícula ou senha incorretos.')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    exercises = Exercise.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', exercises=exercises)

@app.route('/add_exercise', methods=['GET', 'POST'])
@login_required
def add_exercise():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        new_exercise = Exercise(name=name, description=description, user_id=current_user.id)
        db.session.add(new_exercise)
        db.session.commit()
        flash('Exercício cadastrado com sucesso!')
        return redirect(url_for('dashboard'))

    return render_template('add_exercise.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)