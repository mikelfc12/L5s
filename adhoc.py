import pandas as pd

raw_data_df = pd.read_csv("raw_data.csv")

raw_data_df = raw_data_df[raw_data_df['Name'] != "Ringer"]

raw_data_df['GW'] = raw_data_df['Team'].str.replace("A", "GW")
raw_data_df['GW'] = raw_data_df['GW'].str.replace("B", "GW")

raw_data_df = raw_data_df[["Name", "GW", "Goals"]]

raw_data_df = raw_data_df.pivot(index='Name', columns="GW", values="Goals").fillna(0).reset_index()

print(raw_data_df.head())

data = {
    'Player': ['Michael Dixon', 'James King', 'Callum Goodyear', 'Daniel Hirst', 'Jacob Stokes'],
    'GW1': [8, 7, 4, 1, 1],
    'GW2': [14, 14, 8, 2, 4],

}