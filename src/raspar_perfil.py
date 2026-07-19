# Puxa o PERFIL de cada jogador da liga, de forma resiliente:
# - busca um por um (so o dado leve, sem carreira pesada)
# - salva o progresso a cada 25 jogadores
# - se um jogador falhar ou a internet cair, ANOTA e segue
# - se rodar de novo, RETOMA de onde parou (pula quem ja foi salvo)

import time
from pathlib import Path

import pandas as pd
import ScraperFC as sfc
from ScraperFC.utils.botasaurus_getters import botasaurus_browser_get_json

LIGA = "England Premier League"
ANO = "25/26"
ARQUIVO = Path("premier_25_26_perfil.parquet")
API = "https://api.sofascore.com/api/v1"

sofascore = sfc.Sofascore()

# --- 1. Pegar a lista de ids da liga (chamada leve e rapida) ---
print(f"Pegando lista de ids de {LIGA} {ANO}...")
ids = sofascore.get_league_player_ids(year=ANO, league=LIGA)
print(f"{len(ids)} jogadores na liga.")

# --- 2. Se ja existe arquivo salvo, carregar e ver quem ja foi (RETOMADA) ---
if ARQUIVO.exists():
    df_existente = pd.read_parquet(ARQUIVO)
    ja_puxados = set(df_existente["id"])
    resultados = df_existente.to_dict("records")
    print(f"Arquivo ja existe com {len(ja_puxados)} jogadores. Vou pular esses e continuar.")
else:
    ja_puxados = set()
    resultados = []
    print("Comecando do zero.")

# --- 3. Percorrer os ids, buscando um por um com protecao ---
falharam = []
for i, player_id in enumerate(ids, start=1):
    if player_id in ja_puxados:
        continue  # ja temos esse, pula

    try:
        dado = botasaurus_browser_get_json(f"{API}/player/{player_id}")
        p = dado["player"]

        # Monta uma linha PLANA, desembrulhando os pacotinhos aninhados.
        # O .get(...) pega o campo com seguranca: se nao existir, devolve None em vez de quebrar.
        pais = p.get("country", {})
        linha = {
            "id": p.get("id"),
            "nome": p.get("name"),
            "primeiro_nome": p.get("firstName"),
            "ultimo_nome": p.get("lastName"),
            "posicao": p.get("position"),
            "posicoes_detalhadas": ", ".join(p.get("positionsDetailed", [])),
            "data_nascimento": p.get("dateOfBirth"),
            "altura": p.get("height"),
            "pe_preferido": p.get("preferredFoot"),
            "pais_nome": pais.get("name"),
            "pais_sigla": pais.get("alpha3"),
            "valor_mercado_eur": p.get("proposedMarketValue"),
        }
        resultados.append(linha)
    except Exception as erro:
        # nao morre: anota quem falhou e segue
        falharam.append(player_id)
        print(f"  Falhou no id {player_id}: {type(erro).__name__}. Seguindo.")
        continue

    # --- 4. Salvar o progresso a cada 25 jogadores ---
    if len(resultados) % 25 == 0:
        pd.DataFrame(resultados).to_parquet(ARQUIVO, index=False)
        print(f"  [{i}/{len(ids)}] progresso salvo ({len(resultados)} jogadores).")

    time.sleep(0.3)  # respira entre um e outro, pra ser gentil com o servidor

# --- Salvamento final ---
pd.DataFrame(resultados).to_parquet(ARQUIVO, index=False)
print(f"\nPronto. {len(resultados)} jogadores salvos em {ARQUIVO}.")
if falharam:
    print(f"{len(falharam)} falharam: {falharam}")
    print("Rode o script de novo pra tentar pegar os que faltaram.")