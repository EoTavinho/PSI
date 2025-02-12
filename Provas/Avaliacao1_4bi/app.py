from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bercario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mae(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=False)
    idade: Mapped[int] = mapped_column(nullable=False)
    bebes: Mapped[list['Bebe']] = relationship('Bebe', backref='mae', lazy=True)

class Medico(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    crm: Mapped[str] = mapped_column(nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(nullable=False)
    partos: Mapped[list['Parto']] = relationship('Parto', secondary='medico_parto', back_populates='medicos')

class Bebe(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    data_nascimento: Mapped[datetime] = mapped_column(nullable=False)
    peso_nascimento: Mapped[float] = mapped_column(nullable=False)
    altura_nascimento: Mapped[float] = mapped_column(nullable=False)
    mae_id: Mapped[int] = mapped_column(ForeignKey('mae.id'), nullable=False)
    parto_id: Mapped[int] = mapped_column(ForeignKey('parto.id'), nullable=False)

class Parto(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    data_parto: Mapped[datetime] = mapped_column(nullable=False)
    medicos: Mapped[list['Medico']] = relationship('Medico', secondary='medico_parto', back_populates='partos')
    bebes: Mapped[list['Bebe']] = relationship('Bebe', backref='parto', lazy=True)

class MedicoParto(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    medico_id: Mapped[int] = mapped_column(ForeignKey('medico.id'), nullable=False)
    parto_id: Mapped[int] = mapped_column(ForeignKey('parto.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mae', methods=['GET', 'POST'])
def cadastrar_mae():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        idade = int(request.form['idade'])
        nova_mae = Mae(nome=nome, telefone=telefone, idade=idade)
        db.session.add(nova_mae)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastrar_mae.html')

@app.route('/medico', methods=['GET', 'POST'])
def cadastrar_medico():
    if request.method == 'POST':
        nome = request.form['nome']
        crm = request.form['crm']
        telefone = request.form['telefone']
        novo_medico = Medico(nome=nome, crm=crm, telefone=telefone)
        db.session.add(novo_medico)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastrar_medico.html')

@app.route('/parto', methods=['GET', 'POST'])
def registrar_parto():
    if request.method == 'POST':
        data_parto = datetime.strptime(request.form['data_parto'], '%Y-%m-%d').date()
        medicos_ids = request.form.getlist('medicos')
        mae_id = int(request.form['mae_id'])
        nome_bebe = request.form['nome_bebe']
        peso_nascimento = float(request.form['peso_nascimento'])
        altura_nascimento = float(request.form['altura_nascimento'])

        novo_parto = Parto(data_parto=data_parto)
        db.session.add(novo_parto)
        db.session.commit()

        for medico_id in medicos_ids:
            medico_parto = MedicoParto(medico_id=int(medico_id), parto_id=novo_parto.id)
            db.session.add(medico_parto)

        novo_bebe = Bebe(
            nome=nome_bebe,
            data_nascimento=data_parto,
            peso_nascimento=peso_nascimento,
            altura_nascimento=altura_nascimento,
            mae_id=mae_id,
            parto_id=novo_parto.id
        )
        db.session.add(novo_bebe)
        db.session.commit()

        return redirect(url_for('index'))
    maes = Mae.query.all()
    medicos = Medico.query.all()
    return render_template('registrar_parto.html', maes=maes, medicos=medicos)

