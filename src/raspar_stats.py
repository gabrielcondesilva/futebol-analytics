# Raspagem: puxa do Sofascore e salva o parquet. Rodar so quando precisar de dado novo.
import ScraperFC as sfc
from importlib.metadata import version

sofascore = sfc.Sofascore()

df = sofascore.scrape_player_league_stats(
    year = "25/26",
    league = "England Premier League",
    accumulation = "total",
    selected_positions=["Midfielders"]
)

print("Formato (linhas, colunas):", df.shape)
print(df.head())

df.to_parquet("premier_25_26_meio_total.parquet",index=False)
print("Salvo em premier_25_26_meio_total.parquet")