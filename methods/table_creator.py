import streamlit as st 
from methods import filters as f
from io import BytesIO

def match_list(selected_char,category,df_times_played,win_rate,n_col):

    cut_df=f.matchupers(selected_char,category,win_rate)
    cut_df[selected_char] = (cut_df[selected_char]).astype(str) + "%"
    cut_df=cut_df[[cut_df.columns[0], selected_char]]
    df_times_played_temp=df_times_played[selected_char]

    cut_df[selected_char + " (count)"] = df_times_played_temp.loc[cut_df.index]

    st.dataframe(cut_df)
    # Method 1: Use to_excel directly with BytesIO (simpler)

    output = BytesIO()
    download=cut_df[[cut_df.columns[0], selected_char]]
    download[selected_char] = download[selected_char].astype(str) + "%"
    download.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)
    
    st.download_button(
        label="Download Excel",
        data=output,
        file_name="dati.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=n_col
    )