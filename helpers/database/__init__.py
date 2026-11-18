import psycopg2
from flask import g

from helpers.application import app
from helpers.enviroment import enviroment

# Pega o nome do banco do .env (com fallback para 'postgres' se não encontrar)
DATABASE = "instituicao_db"


def get_connection():
    # Verifica se a conexão já existe no contexto da requisição atual (Flask 'g')
    db = getattr(g, '_database', None)
    if db is None:
        # Se não existir, cria uma nova e armazena em g._database
        db = g._database = psycopg2.connect(
            host="localhost",
            database=DATABASE,      # Usa a variável carregada do ambiente
            user="postgres",
            password="12345",       # Senha configurada no seu Docker
            port="5435"             # Porta mapeada no Docker
        )
    return db


@app.teardown_appcontext
def close_connection(exception):
    # Fecha a conexão automaticamente ao fim da requisição HTTP
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()