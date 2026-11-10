import os
import sqlite3
from contextlib import closing
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

database = os.getenv("DB_NAME")
if not database:
    raise RuntimeError("DB_NAME não está definido no arquivo .env ou no ambiente.")

schema_path = PROJECT_DIR / "schema.sql"
if not schema_path.is_file():
    raise FileNotFoundError(f"Arquivo de esquema não encontrado: {schema_path}")

schema = schema_path.read_text(encoding="utf-8")
with closing(sqlite3.connect(database)) as connection:
    connection.executescript(schema)
    connection.commit()
