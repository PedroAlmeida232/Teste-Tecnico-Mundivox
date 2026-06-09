"""
Gera o arquivo examples/saida_exemplo.txt com uma saida real da simulacao.
Execute uma vez apos instalar as dependencias:  python gerar_exemplo.py
"""

import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Redireciona DB para pasta temporaria dentro de examples/
import simulacao as sim

sim.DB_PATH = os.path.join(os.path.dirname(__file__), "exemplo.db")
sim.inicializar_banco()
sim.limpar_competicao()

buf = io.StringIO()
sys.stdout = buf
sim.main()
sys.stdout = sys.__stdout__

saida = buf.getvalue()
print(saida)

with open(os.path.join(os.path.dirname(__file__), "saida_exemplo.txt"), "w", encoding="utf-8") as f:
    f.write(saida)

print("examples/saida_exemplo.txt gerado com sucesso.")
