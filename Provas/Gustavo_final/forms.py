from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=50, message="O nome deve ter pelo menos 3 caracteres.")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Digite um email válido.")])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message="As senhas devem ser iguais.")])
    submit = SubmitField('Registrar')
