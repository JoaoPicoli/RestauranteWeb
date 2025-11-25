# test_conn.py
from app import create_app, db
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

with app.app_context():
    try:
        print("Conectando ao banco:", db.engine.url)
        conn = db.engine.connect()
        tables = db.engine.table_names()
        print("Tabelas existentes:", tables)
        conn.close()
    except Exception as e:
        print("Erro ao conectar:", e)
