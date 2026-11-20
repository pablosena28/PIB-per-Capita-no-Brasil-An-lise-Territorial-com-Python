"""Preparação e validação da base de PIB per capita."""
from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = ["Territorialidades", "Ano", "PIB per capita"]

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Colunas ausentes: {missing_columns}")
    data = df.copy()
    data["Territorialidades"] = data["Territorialidades"].astype(str).str.strip()
    data["Ano"] = pd.to_numeric(data["Ano"], errors="raise").astype(int)
    data["PIB per capita"] = pd.to_numeric(data["PIB per capita"], errors="raise")
    if data[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("A base contém valores ausentes.")
    if data.duplicated(["Territorialidades", "Ano"]).any():
        raise ValueError("Há duplicatas para o mesmo território e ano.")
    return data.sort_values(["Ano", "Territorialidades"]).reset_index(drop=True)

def state_sample(df: pd.DataFrame) -> pd.DataFrame:
    data = prepare_data(df)
    return data[data["Territorialidades"] != "Brasil"].copy()
