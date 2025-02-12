import sqlite3

bancodados = 'bancodados.db'
conn = sqlite3.connect(bancodados)

with open('sqlite.sql') as f:
    conn.executescript(f.read())