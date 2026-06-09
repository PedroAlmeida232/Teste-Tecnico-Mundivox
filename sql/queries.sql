
-- Todas as partidas com nome da fase
SELECT
    f.nome            AS fase,
    p.equipe_a,
    p.gols_a,
    p.gols_b,
    p.equipe_b,
    p.penaltis_a,
    p.penaltis_b,
    p.vencedor
FROM partidas p
JOIN fases f ON p.fase_id = f.id
ORDER BY p.id;


-- Equipe que marcou MAIS gols na competição
SELECT
    equipe,
    SUM(gols) AS total_gols
FROM (
    SELECT equipe_a AS equipe, gols_a AS gols FROM partidas
    UNION ALL
    SELECT equipe_b AS equipe, gols_b AS gols FROM partidas
)
GROUP BY equipe
ORDER BY total_gols DESC
LIMIT 1;


-- Equipe que sofreu MENOS gols na competição
SELECT
    equipe,
    SUM(gols_sofridos) AS total_sofridos
FROM (
    SELECT equipe_a AS equipe, gols_b AS gols_sofridos FROM partidas
    UNION ALL
    SELECT equipe_b AS equipe, gols_a AS gols_sofridos FROM partidas
)
GROUP BY equipe
ORDER BY total_sofridos ASC
LIMIT 1;


-- Quantas partidas foram disputadas em cada fase
SELECT
    f.nome          AS fase,
    COUNT(p.id)     AS total_partidas
FROM partidas p
JOIN fases f ON p.fase_id = f.id
GROUP BY f.nome
ORDER BY f.id;


-- Campeão da competição
SELECT nome AS campeao
FROM equipes
WHERE campeao = 1;


-- Ranking completo de gols marcados
SELECT
    equipe,
    SUM(gols) AS total_gols
FROM (
    SELECT equipe_a AS equipe, gols_a AS gols FROM partidas
    UNION ALL
    SELECT equipe_b AS equipe, gols_b AS gols FROM partidas
)
GROUP BY equipe
ORDER BY total_gols DESC;


-- Partidas decididas nos penaltis
SELECT
    f.nome     AS fase,
    equipe_a,
    equipe_b,
    gols_a,
    gols_b,
    penaltis_a,
    penaltis_b,
    vencedor
FROM partidas p
JOIN fases f ON p.fase_id = f.id
WHERE penaltis_a IS NOT NULL
ORDER BY p.id;


-- Aproveitamento de cada equipe (vitórias / jogos)
SELECT
    e.nome AS equipe,
    COUNT(p.id)                                     AS jogos,
    SUM(CASE WHEN p.vencedor = e.nome THEN 1 ELSE 0 END) AS vitorias,
    ROUND(
        100.0 * SUM(CASE WHEN p.vencedor = e.nome THEN 1 ELSE 0 END)
             / COUNT(p.id), 1
    )                                               AS aproveitamento_pct
FROM equipes e
JOIN partidas p
    ON p.equipe_a = e.nome OR p.equipe_b = e.nome
GROUP BY e.nome
ORDER BY vitorias DESC, jogos ASC;
