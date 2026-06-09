# Simulador Copa do Mundo 2026

Simulação da fase eliminatória da Copa do Mundo 2026 usando Python e PostgreSQL. O programa sorteia os placares, passa por todas as fases (oitavas até a final, incluindo disputa de 3º lugar) e salva tudo no banco ao final.

## Requisitos

- Python 3.10 ou superior
- PostgreSQL rodando localmente (ou acessível via rede)
- `psycopg2-binary`

```bash
pip install -r requirements.txt
```

## Configuração do banco

Crie o banco de dados antes de rodar:

```sql
CREATE DATABASE copa2026;
```

A conexão usa as seguintes variáveis de ambiente (com os valores padrão abaixo):

| Variável      | Padrão      |
|---------------|-------------|
| `PGHOST`      | `localhost` |
| `PGPORT`      | `5432`      |
| `PGDATABASE`  | `copa2026`  |
| `PGUSER`      | `postgres`  |
| `PGPASSWORD`  | *(vazio)*   |

Se o seu setup for diferente, exporte as variáveis antes de rodar:

```bash
# Linux / macOS
export PGUSER=seu_usuario
export PGPASSWORD=sua_senha

# Windows (PowerShell)
$env:PGUSER = "seu_usuario"
$env:PGPASSWORD = "sua_senha"
```

## Como rodar

```bash
git clone https://github.com/PedroAlmeida232/Teste-Tecnico-Mundivox.git
cd Teste-Tecnico-Mundivox
python src/simulacao.py
```

As tabelas são criadas automaticamente na primeira execução. Cada nova execução apaga os dados anteriores e começa uma simulação do zero.

## Estrutura

```
├── src/
│   └── simulacao.py        # lógica principal
├── sql/
│   ├── schema.sql          # criação das tabelas
│   └── queries.sql         # consultas analíticas de referência
├── examples/
│   ├── gerar_exemplo.py    # script para gerar saída de exemplo
│   └── saida_exemplo.txt   # exemplo de saída completa
└── README.md
```

## Como funciona

Os placares são gerados com pesos que tentam imitar a realidade do futebol (a maioria dos jogos termina com 0 a 2 gols por time). Em caso de empate no tempo normal, vai para pênaltis.

A montagem dos confrontos segue a lógica padrão: o 1º classificado enfrenta o 2º, o 3º enfrenta o 4º, e assim por diante.

Times que estreiam nas oitavas:

```
Brasil × México
Argentina × Equador
França × Polônia
Inglaterra × Senegal
Espanha × Marrocos
Portugal × Suíça
Alemanha × Japão
Holanda × Estados Unidos
```

## Banco de dados

Três tabelas: `fases`, `equipes` e `partidas`. O campo `campeao` na tabela de equipes é marcado como `1` ao fim da simulação.

Para consultar após rodar:

```bash
psql -d copa2026

-- campeão
SELECT nome FROM equipes WHERE campeao = 1;

-- todas as partidas
SELECT f.nome AS fase, equipe_a, gols_a, gols_b, equipe_b, vencedor
FROM partidas p JOIN fases f ON p.fase_id = f.id
ORDER BY p.id;
```

Outras consultas prontas estão em `sql/queries.sql`.

## Exemplo de saída

```
==================================================
  OITAVAS DE FINAL
==================================================
  Brasil                        2 x 0                         Mexico  →  ✓ Brasil
  Argentina                     1 x 2                        Ecuador  →  ✓ Ecuador
  ...

==================================================
CAMPEÃO DA COPA DO MUNDO 2026: POLONIA
==================================================

=-=-=- Estatísticas da Competição -=-=-=

Top 5 artilheiras:
  Polonia                    9 gol(s)
  ...
```

Saída completa em `examples/saida_exemplo.txt`.
