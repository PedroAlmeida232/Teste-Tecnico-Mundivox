-- Tabela de fases
CREATE TABLE IF NOT EXISTS fases (
    id   SERIAL PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

-- Tabela de equipes
CREATE TABLE IF NOT EXISTS equipes (
    id      SERIAL PRIMARY KEY,
    nome    TEXT    NOT NULL UNIQUE,
    campeao INTEGER NOT NULL DEFAULT 0
);

-- Tabela de partidas
CREATE TABLE IF NOT EXISTS partidas (
    id          SERIAL PRIMARY KEY,
    fase_id     INTEGER NOT NULL REFERENCES fases(id),
    equipe_a    TEXT    NOT NULL,
    equipe_b    TEXT    NOT NULL,
    gols_a      INTEGER NOT NULL,
    gols_b      INTEGER NOT NULL,
    penaltis_a  INTEGER,
    penaltis_b  INTEGER,
    vencedor    TEXT    NOT NULL
);