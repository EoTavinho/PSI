from flask_login import UserMixin
import sqlite3
BANCO = 'bancodados.db'
def obter_conexao():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    id : str
    def __init__(self, id, matricula, email, senha):
        self.id = id
        self.matricula = matricula
        self.email = email
        self.senha = senha