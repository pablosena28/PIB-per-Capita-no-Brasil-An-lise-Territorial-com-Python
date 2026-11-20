"""Análise territorial do PIB per capita brasileiro entre 2013 e 2016."""
from pathlib import Path
import pandas as pd
from src.data_cleaning import prepare_data, state_sample

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "pib_per_capita_brasil_2013_2016.csv"

def main() -> None:
    raw = pd.read_csv(DATA_PATH)
    df = prepare_data(raw)
    ufs = state_sample(df)
    print("=== VISÃO GERAL ===")
    print(f"Observações: {len(df)}")
    print(f"Territorialidades: {df['Territorialidades'].nunique()}")
    brazil = df[df["Territorialidades"] == "Brasil"].set_index("Ano")["PIB per capita"]
    change = (brazil.loc[2016] / brazil.loc[2013] - 1) * 100
    print(f"Brasil 2013: {brazil.loc[2013]:.2f}")
    print(f"Brasil 2016: {brazil.loc[2016]:.2f}")
    print(f"Variação: {change:.2f}%")
    ranking = ufs[ufs["Ano"] == 2016].sort_values("PIB per capita", ascending=False)
    print("\n=== RANKING 2016 ===")
    print(ranking[["Territorialidades","PIB per capita"]].head(10).to_string(index=False))
    wide = ufs.pivot(index="Territorialidades", columns="Ano", values="PIB per capita")
    wide["variacao_pct"] = (wide[2016] / wide[2013] - 1) * 100
    print("\n=== MAIORES ALTAS ===")
    print(wide["variacao_pct"].sort_values(ascending=False).head(5).round(2))
    print("\n=== MAIORES QUEDAS ===")
    print(wide["variacao_pct"].sort_values().head(5).round(2))

if __name__ == "__main__":
    main()
