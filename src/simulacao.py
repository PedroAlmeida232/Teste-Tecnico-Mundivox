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

def simular_placar() -> tuple[int, int]:
    """
    Gera um placar aleatorio realista.
    A maioria das partidas termina com poucos gols (media de 2,7 por jogo).
    Em caso de empate, vai para penaltis (5x4 ou 4x3, etc.).
    """
    gols_a = random.choices(range(6), weights=[20, 35, 25, 12, 5, 3])[0]
    gols_b = random.choices(range(6), weights=[20, 35, 25, 12, 5, 3])[0]
    return gols_a, gols_b

def resolver_empate(equipe_a: str, equipe_b: str) -> tuple[str, int, int]:
    """
    Resolve partidas empatadas via penaltis.
    Retorna (vencedor, gols_penaltis_a, gols_penaltis_b).
    """
    while True:
        pen_a = random.randint(3, 5)
        pen_b = random.randint(3, 5)
        if pen_a != pen_b:
            vencedor = equipe_a if pen_a > pen_b else equipe_b
            return vencedor, pen_a, pen_b

def disputar_fase(
    confrontos: list[tuple[str, str]], nome_fase: str
) -> list[str]:
    """
    Realiza todos os jogos de uma fase e retorna a lista de classificados.
    """
    print(f"\n{'='*50}")
    print(f"  {nome_fase.upper()}")
    print(f"{'='*50}")

    fase_id = registrar_fase(nome_fase)
    todas_equipes = [e for par in confrontos for e in par]
    registrar_equipes(todas_equipes)

    classificados = []
    for equipe_a, equipe_b in confrontos:
        gols_a, gols_b = simular_placar()
        if gols_a != gols_b:
            vencedor = equipe_a if gols_a > gols_b else equipe_b
            pen_a = pen_b = None
            resultado_str = f"{gols_a} x {gols_b}"
        else:
            vencedor, pen_a, pen_b = resolver_empate(equipe_a, equipe_b)
            resultado_str = (
                f"{gols_a} x {gols_b} "
                f"(pên. {pen_a} x {pen_b})"
            )
        registrar_partida(
            fase_id, equipe_a, equipe_b,
            gols_a, gols_b, pen_a, pen_b, vencedor,
        )
        print(
            f"  {equipe_a:<22} {resultado_str:^20} {equipe_b:>22}"
            f"  →  ✓ {vencedor}"
        )
        classificados.append(vencedor)
    return classificados

def montar_confrontos(equipes: list[str]) -> list[tuple[str, str]]:
    """
    Monta os pares da proxima fase.
    Segue a logica da FIFA: 1º x 2º, 3º x 4º, etc.
    """
    return [(equipes[i], equipes[i + 1]) for i in range(0, len(equipes), 2)]

def main() -> None:
    inicializar_banco()
    limpar_competicao()

    oitavas_confrontos: list[tuple[str, str]] = [
        ("Brasil",    "Mexico"),
        ("Argentina", "Equador"),
        ("Franca",    "Polonia"),
        ("Inglaterra","Senegal"),
        ("Espanha",   "Marrocos"),
        ("Portugal",  "Suica"),
        ("Alemanha",  "Japao"),
        ("Holanda",   "Estados Unidos"),
    ]

    classificados_oitavas = disputar_fase(oitavas_confrontos, "Oitavas de Final")
    quartas_confrontos    = montar_confrontos(classificados_oitavas)
    classificados_quartas = disputar_fase(quartas_confrontos, "Quartas de Final")
    semi_confrontos       = montar_confrontos(classificados_quartas)

    [campeao] = disputar_fase(
        [(finalistas_e_perdedores[0], finalistas_e_perdedores[1])],
        "Final"
    )

    print(f"\n{'='*50}")
    print(f"CAMPEÃO DA COPA DO MUNDO 2026: {campeao.upper()}")
    print(f"{'='*50}\n")

    with conectar() as conn:
        conn.execute(
            "UPDATE equipes SET campeao = 1 WHERE nome = ?", (campeao,)
        )

    exibir_estatisticas()

def exibir_estatisticas() -> None:
    with conectar() as conn:
        print("=-=-=- Estatísticas da Competição -=-=-=\n")

        # Top 5 artilheiros
        rows = conn.execute("""
            SELECT equipe, SUM(gols) AS total
            FROM (
                SELECT equipe_a AS equipe, gols_a AS gols FROM partidas
                UNION ALL
                SELECT equipe_b AS equipe, gols_b AS gols FROM partidas
            )
            GROUP BY equipe ORDER BY total DESC LIMIT 5
        """).fetchall()
        print("Top 5 artilheiras:")
        for nome, total in rows:
            print(f"  {nome:<22} {total:>3} gol(s)")

        # Melhor defesa
        row = conn.execute("""
            SELECT equipe, SUM(gols_sofridos) AS total
            FROM (
                SELECT equipe_a AS equipe, gols_b AS gols_sofridos FROM partidas
                UNION ALL
                SELECT equipe_b AS equipe, gols_a AS gols_sofridos FROM partidas
            )
            GROUP BY equipe ORDER BY total ASC LIMIT 1
        """).fetchone()
        print(f"\nMelhor defesa: {row[0]} ({row[1]} gol(s) sofrido(s))")

        # Partidas por fase
        rows = conn.execute("""
            SELECT f.nome, COUNT(*) AS qtd
            FROM partidas p JOIN fases f ON p.fase_id = f.id
            GROUP BY f.nome ORDER BY f.id
        """).fetchall()
        print("\nPartidas por fase:")
        for fase, qtd in rows:
            print(f"  {fase:<25} {qtd:>2} partida(s)")