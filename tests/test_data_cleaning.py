import pandas as pd
import pytest
from src.data_cleaning import prepare_data, state_sample

def sample_data():
    return pd.DataFrame({
        "Territorialidades":["Brasil","Estado A","Brasil","Estado A"],
        "Ano":[2013,2013,2014,2014],
        "PIB per capita":[20.0,10.0,21.0,11.0],
    })

def test_prepare_data_keeps_valid_rows():
    result=prepare_data(sample_data())
    assert len(result)==4
    assert result["Ano"].dtype.kind in {"i","u"}

def test_state_sample_excludes_brazil():
    result=state_sample(sample_data())
    assert "Brasil" not in result["Territorialidades"].tolist()
    assert len(result)==2

def test_prepare_data_rejects_duplicate_territory_year():
    df=pd.concat([sample_data(),sample_data().iloc[[0]]],ignore_index=True)
    with pytest.raises(ValueError):
        prepare_data(df)
