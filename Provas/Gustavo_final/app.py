from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, sessionmaker, Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blabla'

# Configuração do banco de dados
engine = create_engine('sqlite:///blog.db', echo=True)  # O `echo=True` ajuda a depuração
session = Session(bind=engine) #Tirei o Sessionmaker

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)  # Senha deve ser String para armazenar hash
    posts: Mapped[list["Post"]] = relationship(back_populates="autor", cascade="all, delete-orphan")

    @staticmethod
    def find_by_email(email):
        usuario = session.query(User).filter_by(email=email).first() #Tirei o SessionLocal
        return usuario

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id)) #Tirei o SessionLocal

class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    conteudo: Mapped[str] = mapped_column(String, nullable=False)
    autor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    autor: Mapped["User"] = relationship(back_populates="posts")

# Criar tabelas no banco
with app.app_context():
    Base.metadata.create_all(engine)

@app.route('/')
@login_required # Impede q o usuario acesse qqr página sem fazer login através do flask-login
def index():
    posts = session.query(Post).all() #Tirei o SessionLocal
    return render_template('index.html', posts=posts, nome=current_user.nome if current_user.is_authenticated else None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit(): # Baixei o email-validator
        email = form.email.data
        senha = form.senha.data

        usuario = session.query(User).filter_by(email=email).first() #Tirei o SessionLocal

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('index'))
        else:
            flash("Email ou senha incorretos!", "danger")

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit(): #Baixei o email-validator
        nome = form.nome.data
        email = form.email.data
        senha = form.senha.data
        senha_hash = generate_password_hash(senha)

        novo_usuario = User(nome=nome, email=email, senha=senha_hash)
        
        #Tirei o SessionLocal
        session.add(novo_usuario)
        session.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/criar_post', methods=['GET', 'POST'])
@login_required # Impede q o usuario acesse qqr página sem fazer login através do flask-login
def criar_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']

        novo_post = Post(titulo=titulo, conteudo=conteudo, autor_id=current_user.id)
        
        #Tirei o SessionLocal
        session.add(novo_post)
        session.commit()

        flash("Post criado com sucesso!", "success")
        return redirect(url_for('index'))

    return render_template('criar_post.html')

@app.route('/logout')
@login_required # Impede q o usuario acesse qqr página sem fazer login através do flask-login
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))
