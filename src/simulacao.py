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

def registrar_fase(nome_fase: str) -> int:
    with conectar() as conn:
        cur = conn.execute(
            "INSERT INTO fases (nome) VALUES (?)", (nome_fase,)
        )
        return cur.lastrowid

def registrar_equipes(equipes: list[str]) -> dict[str, int]:
    ids = {}
    with conectar() as conn:
        for eq in equipes:
            cur = conn.execute(
                "INSERT OR IGNORE INTO equipes (nome) VALUES (?)", (eq,)
            )
            if cur.lastrowid:
                ids[eq] = cur.lastrowid
            else:
                row = conn.execute(
                    "SELECT id FROM equipes WHERE nome = ?", (eq,)
                ).fetchone()
                ids[eq] = row[0]
    return ids

def registrar_partida(
    fase_id: int, equipe_a: str, equipe_b: str,
    gols_a: int, gols_b: int,
    pen_a: Optional[int], pen_b: Optional[int],
    vencedor: str,
) -> None:
    with conectar() as conn:
        conn.execute(
            """
            INSERT INTO partidas
                (fase_id, equipe_a, equipe_b, gols_a, gols_b,
                 penaltis_a, penaltis_b, vencedor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (fase_id, equipe_a, equipe_b, gols_a, gols_b,
             pen_a, pen_b, vencedor),
        )
