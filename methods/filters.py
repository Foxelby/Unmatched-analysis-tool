# these are the different ranges where a matchup is counted as winning or losing
import streamlit as st
import pandas as pd


def matchupers(selected_char,  matchup_category,win_rate):

    dataset_percent=win_rate
    cut_df = dataset_percent.copy()

    if selected_char not in dataset_percent.columns:
        st.warning(f"{selected_char} non trovato nel dataset.")
        return pd.DataFrame()  # ritorna vuoto se il personaggio non c'è

    # Inizializza mask a False
    mask = pd.Series(False, index=dataset_percent.index)

    data = dataset_percent[[selected_char]]  # solo la colonna del personaggio

    if "hard winning" in matchup_category:
        mask |= (data > 75).any(axis=1)

    if "winning" in matchup_category:
        mask |= ((data > 60) & (data <= 75)).any(axis=1)

    if "evenish" in matchup_category:
        mask |= ((data >= 40) & (data <= 60)).any(axis=1)

    if "losing" in matchup_category:
        mask |= ((data >= 25) & (data < 40)).any(axis=1)

    if "hard losing" in matchup_category:
        mask |= ((data < 25) & (data >=0)).any(axis=1)

    return cut_df[mask]
