import random
import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "copa2026.db")

def conectar() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)

def inicializar_banco() -> None:
    """Cria as tabelas caso ainda nao existam."""
    with conectar() as conn:
        conn.executescript(open(os.path.join(os.path.dirname(__file__),
                                             "..", "sql", "schema.sql")).read())

def limpar_competicao() -> None:
    """Remove todos os dados de uma simulacao anterior."""
    with conectar() as conn:
        conn.executescript("""
            DELETE FROM partidas;
            DELETE FROM equipes;
            DELETE FROM fases;
        """)