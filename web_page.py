import pandas as pd
import streamlit as st
from io import BytesIO
import numpy as np
from methods import reading_path as rp
from methods import table_creator as tc

# *PAGE CONFIG -------------------------------------------------------
st.set_page_config(
    page_title="Strumento analitico per Unmatched ⚔️",
    layout="wide",
)

df_percentages=rp.load_data("win_rate")
df_times_played=rp.load_data("n_games")
#----PAGINA ST-----

st.title("Strumento analitico per Unmatched ⚔️")
st.caption(
    "analisi più comoda per i matchup in unmatched" \
    "Data: Tabletop League (tabletopleague.com)"
)

#SIDEBAR
st.sidebar.header("⚙️ dataset's filters")
matchup_category= st.sidebar.multiselect(
            "Scegli una il range di matchup",
            options=["hard winning", "winning", "evenish", "losing", "hard losing"],
            default=["hard winning", "winning", "evenish", "losing", "hard losing"],
)



#just so you can see the simple structure
with st.expander("show the first rows of the dataset"):
    st.dataframe(df_percentages.head())

#comparing the characters
st.subheader("🔍 character comparison")

N_col=st.slider(
    "how many character you want to see at the same time",
    min_value=1,
    max_value=3,
    value=1,
    step=1,
    help="quanti personaggi vuoi vedere al contempo"
)
columns = st.columns(N_col)

selected_characters = []

for i, col in enumerate(columns):
    with col:
        character = st.selectbox(
            f"Choose character {i+1}",
            options=df_percentages["category"].unique(),
            key=f"character_{i}"
        )
        selected_characters.append(character)

with columns[0]:
    # Access the selections
    selected_character = selected_characters[0]
    tc.match_list(selected_char=selected_character, category=matchup_category, df_times_played=df_times_played, win_rate=df_percentages, n_col=1)

if N_col >= 2:
    with columns[1]:
        selected_character2 = selected_characters[1]
        # Access the selections
        selected_character = selected_characters[1]
        tc.match_list(selected_char=selected_character, category=matchup_category, df_times_played=df_times_played, win_rate=df_percentages, n_col=2)
    
if N_col == 3:
    with columns[2]:
        selected_character3 = selected_characters[2]
        # Access the selections
        selected_character = selected_characters[2]
        tc.match_list(selected_char=selected_character, category=matchup_category, df_times_played=df_times_played, win_rate=df_percentages, n_col=3)


#to compare a specific matchup
st.subheader("Matchups")
with st.expander("Matchup comparision"):
    col1,col2=st.columns(2)
    with col1:
        left_char = st.selectbox(
            "choose a character",
            options=df_percentages["category"].unique(),
        )
    with col2:
        right_char=st.selectbox(
        "choose an opponent",
        options=df_percentages.columns[1:]
        )
    
    # find the row corrisponding to the choosen character
    row_index = df_percentages.index[df_percentages["category"] == right_char][0]

    # extracting the value (percent of winrate)
    value = df_percentages.loc[row_index, left_char]
    N_times_played=df_times_played.loc[row_index, left_char]
    if value==-2:
        st.write("this matchup is not in the dataset")
    else:
        color = "red" if value < 50 else "green"

        st.markdown(
            f"<h3 style='color:{color};'>{value}% winrate</h3>"
            f"<p>{N_times_played} times played</p>",
            unsafe_allow_html=True
        )