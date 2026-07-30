from pathlib import Path
import pandas as pd

def load_data(file_choice):
    DATA_PATH = Path("./data")

    if file_choice == "win_rate":
        return pd.read_csv(DATA_PATH / "win_rate_percentage.csv")

    elif file_choice == "n_games":
        return pd.read_csv(DATA_PATH / "number_of_games.csv")