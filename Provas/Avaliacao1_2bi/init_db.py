import sqlite3

# abre a conexão
conn = sqlite3.connect('escola.db')
cursor = conn.cursor()
# localização do sql
SCHEMA = 'schema.sql'

# executa as declarações do sql para o banco
with open(SCHEMA) as f:
    cursor.executescript(f.read())

# encerra as operações
conn.commit()
conn.close()