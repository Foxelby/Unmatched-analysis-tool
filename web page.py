from pathlib import Path
import pandas as pd
import streamlit as st
from io import BytesIO
import numpy as np
# *PAGE CONFIG -------------------------------------------------------
st.set_page_config(
    page_title="Strumento analitico per Unmatched ⚔️",
    layout="wide",
)

# *VARS  -------------------------------------------------------------
# Data path
DATA_PATH = Path(r".\data")

df_percentages = pd.read_csv(DATA_PATH / "vrwwh747l.csv")
df_times_played = pd.read_csv(DATA_PATH / "flvjmyf6j.csv")  
#----PAGINA ST-----

st.title("Strumento analitico per Unmatched ⚔️")
st.caption(
    "analisi più comoda per i matchup in unmatched"
)


st.sidebar.header("⚙️ dataset's filters")


matchup_category= st.sidebar.multiselect(
            "Scegli una il range di matchup",
            options=["hard winning", "winning", "evenish", "losing", "hard losing"],
            default=["hard winning", "winning", "evenish", "losing", "hard losing"],
)

# these are the different ranges where a matchup is counted as winning or losing
def matchupers(selected_char):
    cut_df = df_percentages.copy()

    if selected_char not in df_percentages.columns:
        st.warning(f"{selected_char} non trovato nel dataset.")
        return pd.DataFrame()  # ritorna vuoto se il personaggio non c'è

    # Inizializza mask a False
    mask = pd.Series(False, index=df_percentages.index)

    data = df_percentages[[selected_char]]  # solo la colonna del personaggio

    if "hard winning" in matchup_category:
        mask |= (data > 75).any(axis=1)

    if "winning" in matchup_category:
        mask |= ((data > 60) & (data <= 75)).any(axis=1)

    if "evenish" in matchup_category:
        mask |= ((data >= 40) & (data <= 60)).any(axis=1)

    if "losing" in matchup_category:
        mask |= ((data >= 25) & (data < 40)).any(axis=1)

    if "hard losing" in matchup_category:
        mask |= ((data < 25) & (data >0)).any(axis=1)

    return cut_df[mask]



#just so you can see the simple structure
with st.expander("show the first rows of the dataset"):
    st.dataframe(df_percentages.head())


st.subheader("🔍 character comparison")

N_col=st.slider(
    "how many character you want to see at the same time",
    min_value=1,
    max_value=3,
    value=1,
    step=1,
    help="quanti personaggi vuoi vedere al contempo"
)

columns=[]
columns.extend(st.columns(N_col))

#genereating a dataframe with winning or losing matchup of a character, you can do more characters
#simultaneously, you can even download excel files of those dataframes!!!
with columns[0]:
    selected_character = st.selectbox(
            "choose a character, in case of an alt 1.0 use that, its the most recent version",
            options=df_percentages["category"].unique(),
        )
    cut_df=matchupers(selected_character)
    cut_df[selected_character] = (cut_df[selected_character]).astype(str) + "%"
    cut_df=cut_df[[cut_df.columns[0], selected_character]]
    df_times_played_temp=df_times_played[selected_character]

    cut_df[selected_character + " (count)"] = df_times_played_temp.loc[cut_df.index]

    st.dataframe(cut_df)

    # Method 1: Use to_excel directly with BytesIO (simpler)
    output = BytesIO()
    download=cut_df[[cut_df.columns[0], selected_character]]
    download[selected_character] = download[selected_character].astype(str) + "%"
    download.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)
    
    st.download_button(
        label="Download Excel",
        data=output,
        file_name="dati.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if N_col==2 or N_col==3:
    with columns[1]:
        selected_character2 = st.selectbox(
            "choose a character, in case of an alt 1.0 use that, its the most recent version.",
            options=df_percentages["category"].unique(),
        )
        cut_df=matchupers(selected_character2)
        cut_df[selected_character2] = (cut_df[selected_character2]).astype(str) + "%"
        cut_df=cut_df[[cut_df.columns[0], selected_character2]]
        df_times_played_temp=df_times_played[selected_character2]

        cut_df[selected_character2 + " (count)"] = df_times_played_temp.loc[cut_df.index]

        st.dataframe(cut_df)

        # Method 1: Use to_excel directly with BytesIO (simpler)
        output = BytesIO()
        download=cut_df[[cut_df.columns[0], selected_character2]]
        download[selected_character2] = download[selected_character2].astype(str) + "%"
        download.to_excel(output, index=False, engine='xlsxwriter')
        output.seek(0)

        st.download_button(
            label="Download Excel2",
            data=output,
            file_name="dati.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



if N_col==3:
    with columns[2]:
        selected_character3 = st.selectbox(
            "choose a character, in case of an alt 1.0 use that, its the most recent version..",
            options=df_percentages["category"].unique(),
        )
        cut_df=matchupers(selected_character3)

        cut_df[selected_character3] = (cut_df[selected_character3]).astype(str) + "%"
        cut_df=cut_df[[cut_df.columns[0], selected_character3]]
        df_times_played_temp=df_times_played[selected_character3]

        cut_df[selected_character3 + " (count)"] = df_times_played_temp.loc[cut_df.index]

        st.dataframe(cut_df)

            # Method 1: Use to_excel directly with BytesIO (simpler)
        output = BytesIO()
        download=cut_df[[cut_df.columns[0], selected_character3]]
        download[selected_character3] = download[selected_character3].astype(str) + "%"
        download.to_excel(output, index=False, engine='xlsxwriter')
        output.seek(0)

        st.download_button(
            label="Download Excel3",
            data=output,
            file_name="dati.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


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